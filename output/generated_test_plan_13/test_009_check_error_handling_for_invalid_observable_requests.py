import requests
import pytest

@pytest.mark.parametrize("observable_bit", ["INVALID_BIT", "NON_EXISTENT_BIT"])
def test_send_request_with_invalid_observable(observable_bit):
    # Prepare URL and headers
    url = "http://device_endpoint/api"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer your_access_token"
    }

    # Send the request with an invalid observable bit set
    response = requests.post(url, json={"observable_bit": observable_bit}, headers=headers)

    # Verify that the device returns an error response (status code 400)
    assert response.status_code == 400

    # Check error message for expected content indicating invalid observable
    error_message = response.json().get("error_message")
    assert "invalid" in error_message, f"Expected 'invalid' in error message but got: {error_message}"

    # Additional verification steps can be added as needed