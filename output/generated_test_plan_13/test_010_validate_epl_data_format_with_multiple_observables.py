import pytest

def test_pm_data_collection():
    # Check if device is ready after initialization
    validate_state_transition('INIT', 'READY')

    # Configure EPL to return PM data with 3 observable bits set
    read_register('CONTROL', value=0x80)

    # Send request for PM data
    send_request()

    # Verify that received data contains multiple records
    assert len(received_data) > 1

    # Parse and validate each record's content
    for record in received_data:
        if len(record) == 6 or len(record) == 8:
            # Validate the format of X16 (X16 minimum/average/max/current value)
            validate_x16_record(record)

def send_request():
    # Code to send request to device for PM data
    pass

def read_register(register, value=0x0):
    # Code to read a register from the device with optional value
    pass

def validate_state_transition(old_state, new_state):
    # Code to validate that the device has transitioned to a specific state
    pass

def monitor_link_status(timeout=5000):
    # Code to monitor link status and wait for a timeout if necessary
    pass

def validate_x16_record(record):
    # Code to validate an X16 record, checking its minimum/average/max/current values
    pass

# Example usage of the test function
if __name__ == "__main__":
    pytest.main([__file__])