import requests

def test_invalid_epl_page_configuration():
    # Ensure device is in INIT state and ready for operations
    validate_state_transition('INIT', 'READY')
    
    # Perform a read operation to attempt an invalid EPL page configuration
    response = requests.get('http://device/api/invalid-epl-page')
    
    # Verify that the response status code indicates an error (e.g., 400)
    assert response.status_code == 400, "Expected status code 400 for invalid EPL page"
    
    # Check the content of the error message to ensure it includes expected content
    expected_error_message = "Invalid EPL page configuration"
    error_message = response.json().get('error', '')
    assert expected_error_message in error_message, f"Expected error message: {expected_error_message}, but got: {error_message}"
    
    # Monitor link status to verify the device's readiness
    monitor_link_status(5000)