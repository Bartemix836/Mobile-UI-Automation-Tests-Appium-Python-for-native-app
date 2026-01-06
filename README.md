📱 Mobile UI Test Automation Framework (Android)

End-to-end mobile UI test automation framework for native Android applications.
Built with Python 3.10 and Appium, featuring reusable action modules, gesture handling, configurable test selection via .ini files, and Allure reporting.
Tests are executed on physical Android devices as well as Android Studio emulators.

🛠 Tech Stack

  Python 3.10
  
  Appium
  
  Pytest
  
  Allure Reports
  
  Android (physical devices & emulators)

▶️ Running Tests

  1️⃣ Prerequisites
  
    Python 3.10
    
    Appium Server running
    
    Android SDK installed
    
    Connected physical Android device or running Android Studio emulator
    
    Allure CLI installed
  
  2️⃣ Install dependencies
    pip install -r requirements.txt
  
  3️⃣ Select tests to execute
  
    Edit the file:
    
    test_cases_selection.ini
    
  
  Mark tests with:
  
    T – test will be executed
    
    any other value / empty – test will be skipped
    
  Example:
  
    [tests]
    test_TC_01_run_app.py = T
    test_TC_02_change_view.py = N
  
  4️⃣ Run selected tests
  
    Execute the runner script:
    
    python run_selected_R_tests.py
    
    
    This script:
    
    reads test selection from test_cases_selection.ini
    
    runs only marked tests
    
    automatically clears/reset the .ini file after execution
    
    generates Allure result files
  
  📊 Generate and View Allure Report
  allure serve reports
  
  
  This command generates and opens the interactive Allure report in your browser.
  
  ✅ Key Features
  
    Native Android UI automation
    
    Physical devices & emulators support
    
    Config-based test selection (.ini)
    
    Reusable core actions and assertions
    
    Gesture handling (swipes, scrolls, system actions)
    
    Allure test reporting
