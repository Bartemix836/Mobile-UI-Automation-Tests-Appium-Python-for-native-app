import time
import subprocess
import re
from typing import Optional, Tuple

from appium import webdriver
from appium.options.android import UiAutomator2Options

# ---------------------------------------------------------------------------
# Global throttling state
# ---------------------------------------------------------------------------
last_activity_time = time.time()
request_counter = 0
request_window_start = time.time()
last_request_time = 0

# Throttling configuration
MIN_INTERVAL_BETWEEN_REQUESTS = 0.35  # ~171 requests/minute


def update_activity_time():
    """Track last user/action activity timestamp."""
    global last_activity_time
    last_activity_time = time.time()


def count_request(throttle_log: bool = True):
    """
    Simple throttling for calls that may hit ADB/Appium. Keeps per-minute counter
    and enforces a minimum interval between subsequent calls.
    """
    global request_counter, request_window_start, last_request_time

    now = time.time()
    elapsed_since_last = now - last_request_time

    # Enforce a minimum request interval
    if elapsed_since_last < MIN_INTERVAL_BETWEEN_REQUESTS:
        sleep_time = MIN_INTERVAL_BETWEEN_REQUESTS - elapsed_since_last
        print(f"[Throttle] ⏳ Wait {sleep_time:.3f}s, not to exceed the limit.")
        time.sleep(sleep_time)

    last_request_time = time.time()

    # Reset counter each minute
    if now - request_window_start > 60:
        request_counter = 0
        request_window_start = now

    request_counter += 1
    print(f"[Request] #{request_counter} in the current 1-minute window")

    # Log to device every 50th request (and after 200)
    if throttle_log and (request_counter % 50 == 0 or request_counter > 200):
        subprocess.run(
            ["adb", "shell", "log", "-t", "AppiumThrottle", f"Request #{request_counter} in current minute"],
            check=False,
        )

    if request_counter > 200:
        print(f"[Throttle] ⚠️ EXCEEDED 200 requests/min — current: {request_counter}")
        subprocess.run(
            ["adb", "shell", "log", "-t", "AppiumThrottle",
             f"⚠️ THROTTLE: exceeded 200 requests/min — current: {request_counter}"],
            check=False,
        )


# ---------------------------------------------------------------------------
# ADB helpers
# ---------------------------------------------------------------------------

def _run_adb(cmd_args: list, timeout: int = 5000) -> Tuple[int, str, str]:
    """
    Run adb and return (returncode, stdout, stderr). Timeout in ms.
    """
    try:
        proc = subprocess.run(
            cmd_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout / 1000,
            check=False,
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except subprocess.TimeoutExpired:
        return 124, "", "TimeoutExpired"


def _extract_activity_from_component_line(line: str, app_package: str) -> Optional[str]:
    """
    Tries to extract fully-qualified activity name from a variety of formats:
      - 'com.pkg/fully.qualified.Activity'
      - 'com.pkg/.Activity'
      - 'fully.qualified.Activity'
      - '.Activity'
      - or noisy lines
    Returns fully-qualified activity (e.g. 'com.pkg.MainActivity') or None.
    """
    line = line.strip()

    # 1) Full '<package>/<activity>' form
    if "/" in line:
        pkg, act = line.split("/", 1)
        pkg = pkg.strip()
        act = act.strip()
        if not pkg:
            return None
        if act.startswith("."):
            # '.MainActivity' => 'com.pkg.MainActivity'
            return f"{pkg}{act}"
        if "." in act:
            # already fully-qualified
            return act
        # 'MainActivity' => qualify with package
        return f"{pkg}.{act}"

    # 2) Only activity present (fully qualified or dot-prefixed)
    if line.startswith("."):
        return f"{app_package}{line}"
    if re.match(r"^[a-zA-Z_]\w*(\.[A-Za-z0-9_]\w*)+$", line):
        # looks like fully qualified already
        return line

    # 3) Only package present → nothing usable
    if line == app_package:
        return None

    return None


def resolve_launcher_activity(app_package: str, device_name: str = "emulator-5554") -> Optional[str]:
    """
    Resolve an exported LAUNCHER activity for the given app package.
    Strategy:
      A) 'cmd package resolve-activity --brief' with MAIN + LAUNCHER intent
      B) Fallback: parse 'dumpsys window' (mCurrentFocus)
      C) Fallback: 'dumpsys package <pkg>' — find MAIN+LAUNCHER intents
    Returns fully-qualified activity name (e.g. 'com.pkg.MainActivity') or None.
    """
    # --- A) resolve-activity with MAIN/LAUNCHER ---
    rc, out, err = _run_adb([
        "adb", "-s", device_name, "shell", "cmd", "package", "resolve-activity",
        "--brief", "-a", "android.intent.action.MAIN",
        "-c", "android.intent.category.LAUNCHER", app_package
    ])
    if rc == 0 and out:
        for line in out.splitlines():
            act = _extract_activity_from_component_line(line, app_package)
            if act:
                print(f"[Resolve] cmd package MAIN/LAUNCHER -> {line} -> {act}")
                return act
        print(f"[Resolve] cmd package MAIN/LAUNCHER returned but unparsable: {out!r}")
    else:
        print(f"[Resolve] cmd package MAIN/LAUNCHER failed (rc={rc}): {err or out}")

    # --- B) Fallback: mCurrentFocus ---
    rc, out, err = _run_adb(["adb", "-s", device_name, "shell", "dumpsys", "window"])
    if rc == 0 and out:
        for line in out.splitlines():
            if "mCurrentFocus" in line and app_package in line and "/" in line:
                # e.g. mCurrentFocus=Window{... u0 com.pkg/com.pkg.Activity}
                comp_part = line
                if "u0 " in line:
                    comp_part = line.split("u0 ", 1)[-1]
                elif "=" in line:
                    comp_part = line.split("=", 1)[-1]
                act = _extract_activity_from_component_line(comp_part, app_package)
                if act:
                    print(f"[Resolve] mCurrentFocus -> {comp_part.strip()} -> {act}")
                    return act
        print(f"[Resolve] mCurrentFocus fallback returned but no match for {app_package}")
    else:
        print(f"[Resolve] mCurrentFocus failed (rc={rc}): {err or out}")

    # --- C) Fallback: dumpsys package (parse MAIN/LAUNCHER) ---
    rc, out, err = _run_adb(["adb", "-s", device_name, "shell", "dumpsys", "package", app_package])
    if rc == 0 and out:
        lines = out.splitlines()
        for i, line in enumerate(lines):
            if "action=android.intent.action.MAIN" in line:
                # Look ahead a few lines for LAUNCHER category and an activity name
                window = lines[i:i+12]
                if any("category=android.intent.category.LAUNCHER" in l for l in window):
                    for w in window:
                        if "/" in w and app_package in w:
                            # Try component at the end of the line
                            comp_token = w.split()[-1]
                            act = _extract_activity_from_component_line(comp_token, app_package)
                            if act:
                                print(f"[Resolve] dumpsys package (component) -> {w.strip()} -> {act}")
                                return act
                        # Or name=fully.qualified.Activity
                        m = re.search(r"name=([A-Za-z_][\w\.]+)", w)
                        if m:
                            act = m.group(1)
                            act = f"{app_package}{act}" if act.startswith(".") else act
                            print(f"[Resolve] dumpsys package (name=) -> {w.strip()} -> {act}")
                            return act
        print(f"[Resolve] dumpsys package found no MAIN/LAUNCHER mapping for {app_package}")
    else:
        print(f"[Resolve] dumpsys package failed (rc={rc}): {err or out}")

    # Nothing found
    return None


# ---------------------------------------------------------------------------
# Driver creation (Appium 2 / W3C)
# ---------------------------------------------------------------------------

def create_driver():
    """
    Creates and returns an Appium driver for Android (UiAutomator2) with
    robust timeouts suitable for emulators and apps with splash/redirects.
    Dynamically resolves the exported LAUNCHER activity to avoid
    SecurityException for non-exported internal activities.
    """
    app_package = "com.okinc.okex.gp"
    device_name = "emulator-5554"

    # Resolve LAUNCHER (exported) activity; if not found, let Appium auto-resolve
    launcher_activity = resolve_launcher_activity(app_package, device_name=device_name)

    cap = {
        # W3C capabilities (Appium 2 -> use appium: prefix for Appium-specific keys)
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": device_name,

        "appium:appPackage": app_package,
        # Set only if resolved. If None, Appium will try to find a valid launcher.
        **({"appium:appActivity": launcher_activity} if launcher_activity else {}),

        # Session behaviour
        "appium:noReset": True,
        "appium:fullReset": False,
        "appium:newCommandTimeout": 300,
        "appium:disableWindowAnimation": True,

        # Key timeouts for stability (UIA2 + emulator)
        "appium:adbExecTimeout": 120000,
        "appium:uiautomator2ServerInstallTimeout": 120000,
        "appium:uiautomator2ServerLaunchTimeout": 120000,
        "appium:appWaitActivity": "*",      # tolerate splash/redirect
        "appium:appWaitDuration": 60000,    # 60s

        # Helpful extras
        "appium:autoGrantPermissions": True,
        "appium:enablePerformanceLogging": True,
        "appium:adbShellEnabled": True,
    }

    options = UiAutomator2Options().load_capabilities(cap)

    # Prefer 127.0.0.1 over 'localhost' (IPv6/proxy surprises)
    url = "http://127.0.0.1:4723"
    driver = webdriver.Remote(command_executor=url, options=options)
    driver.implicitly_wait(10)
    time.sleep(1.0)  # short breath for UIA2 stabilization

    switch_to_app_if_running(driver, app_package)
    update_activity_time()

    return driver


# ---------------------------------------------------------------------------
# App process helpers
# ---------------------------------------------------------------------------

_cached_ps_result = None
_last_ps_check_time = 0


def app_is_running(driver, app_package: str, cache_duration: int = 10) -> bool:
    """
    Checks if a given app package has a running process on the device.
    Uses 'mobile: shell' (requires Appium server started with --relaxed-security).
    Caches 'ps -A' output for cache_duration (seconds).
    """
    global _cached_ps_result, _last_ps_check_time
    try:
        now = time.time()
        if _cached_ps_result is None or now - _last_ps_check_time > cache_duration:
            count_request()
            output = driver.execute_script(
                "mobile: shell",
                {
                    "command": "ps",
                    "args": ["-A"],   # full process list (Android 8+)
                    "timeout": 5000,  # ms
                },
            )
            # mobile:shell returns STDOUT as string; ensure it's a string
            _cached_ps_result = output if isinstance(output, str) else str(output)
            _last_ps_check_time = now

        for line in _cached_ps_result.splitlines():
            if app_package in line:
                return True
    except Exception as e:
        print(f"Failed to check the application: {e}")
    return False


def switch_to_app_if_running(driver, app_package: str):
    """
    If the app process exists, activate it; otherwise start it.
    """
    if app_is_running(driver, app_package):
        print(f"Application {app_package} is running in the background. Switching...")
        count_request()
        driver.activate_app(app_package)
    else:
        print(f"Application {app_package} is not running. Starting it...")
        count_request()
        driver.activate_app(app_package)
