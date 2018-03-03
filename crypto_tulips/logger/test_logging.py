from . import crypt_logger
import os.path
import pytest

def test_critical_logger():
    file_name = "crypto_tulips/logs/critical.log"
    critical_file_message = "TESTING FOR CRITICAL LOGGER"
    crypt_logger.Logger.log(critical_file_message, 20, crypt_logger.LoggingLevel.CRITICAL)
    print("Testing to see if file exist....")
    assert os.path.isfile(file_name) == True
    print("Testing to see if content is correct")
    status = open_file_check_content(file_name, critical_file_message)
    assert status == True

def open_file_check_content(filename, content_to_check):
    log_file = open(filename)
    logged_status = False
    for content in log_file:
        if content_to_check in content:
            logged_status = True
            break

    return logged_status

def test_error_logger():
    file_name = "crypto_tulips/logs/errors.log"
    error_file_message = "TESTING FOR ERROR LOGGER"
    crypt_logger.Logger.log(error_file_message, 20, crypt_logger.LoggingLevel.ERROR)
    print("Testing to see if file exist....")
    assert os.path.isfile(file_name) == True
    print("Testing to see if content is correct")
    status = open_file_check_content(file_name, error_file_message)
    assert status == True

def test_info_logger():
    file_name = "crypto_tulips/logs/info.log"
    info_file_message = "TESTING FOR INFO LOGGER"
    crypt_logger.Logger.log(info_file_message, 20, crypt_logger.LoggingLevel.INFO)
    print("Testing to see if file exist....")
    assert os.path.isfile(file_name) == True
    print("Testing to see if content is correct")
    status = open_file_check_content(file_name, info_file_message)
    assert status == True

def test_debug_logger():
    file_name = "crypto_tulips/logs/debug.log"
    debug_file_message = "TESTING FOR DEBUG LOGGER"
    crypt_logger.Logger.log(debug_file_message, 20, crypt_logger.LoggingLevel.DEBUG)
    print("Testing to see if file exist....")
    assert os.path.isfile(file_name) == True
    print("Testing to see if content is correct")
    status = open_file_check_content(file_name, debug_file_message)
    assert status == True