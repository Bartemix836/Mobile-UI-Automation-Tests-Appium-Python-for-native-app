import configparser
import pytest
import os

def load_test_files(config_path='test_cases_selection.ini'):
    # Load the configuration file
    config = configparser.ConfigParser()
    config.read(config_path)

    test_files = []

    # Check if the 'tests' section exists
    if 'tests' in config.sections():
        for test_file, flag in config.items('tests'):
            flag = flag.strip().upper() if flag.strip() else 'N'  # Default to "N" if variable is empty
            config.set('tests', test_file, flag)  # Save the updated value to the config

            # Check if the test should be run (marked with 'T')
            if flag == 'T':
                test_files.append(os.path.join('tests', 'regression', test_file.strip()))

    # Save the modified configuration file
    with open(config_path, 'w') as configfile:
        config.write(configfile)

    return test_files


if __name__ == '__main__':
    # Load selected tests from the configuration file
    selected_tests = load_test_files()

    # If tests were selected, run them
    if selected_tests:
        pytest.main(selected_tests + ['--alluredir=reports'])
    else:
        print(
            "No tests to run. Make sure the test_selection.ini file specifies which tests to execute.")
