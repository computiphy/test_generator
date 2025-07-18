import pytest

def test_large_request_error():
    # Setup for the test, ensuring the device is ready and connected
    monitor_link_status(5000)
    wait_for_state('READY', 3000)

    # Prepare a large number of records (e.g., 100 records)
    large_data = [f"record{i}" for i in range(1, 101)]

    try:
        # Attempt to send the request with the large data
        read_register('CONTROL', data=large_data)
        pytest.fail("The device did not return an error response")

    except Exception as e:
        # Check if the error message indicates limitations on EPL data size
        assert str(e).startswith("Error code: 400") or "Error code: 429" in str(e), \
               f"Unexpected error: {str(e)}"

# Run pytest to execute this test
pytest.main()