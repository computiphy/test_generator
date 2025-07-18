import pytest

@pytest.mark.parametrize("max_records", [120])
def test_pm_data(max_records):
    # Configure device to return up to 120 records using LPL with multiple observable bits set
    read_register('CONTROL', value=0x240)

    # Send request to device for PM data with the maximum number of records requested
    response = send_request('READ_PM_DATA', max_records=max_records)
    
    # Verify that the received data length matches the total number of available records (up to 120)
    assert len(response) <= max_records, "Received more data than expected"
    
    # Parse received data and validate that all records are present, with valid values
    for record in response:
        # Check if each record is a valid type or contains expected fields
        assert isinstance(record, dict), f"Invalid record format: {record}"
        # Add specific validation checks based on your PM data structure

# Helper functions for testing
def send_request(command, max_records=None):
    # Simulate sending a request and receiving a response
    if command == 'READ_PM_DATA':
        # This function should simulate reading from the device and return records
        # For demonstration, we'll just mock the data
        if max_records is None:
            max_records = 120
        return [{'id': i} for i in range(max_records)]
    else:
        raise ValueError(f"Unsupported command: {command}")

def read_register(register_name, value=None):
    # Simulate reading from a register
    # This function should return the current value of the register
    if value is not None:
        # Simulate writing to a register
        pass
    return {'CONTROL': 0x240}  # Mocked return value for demonstration