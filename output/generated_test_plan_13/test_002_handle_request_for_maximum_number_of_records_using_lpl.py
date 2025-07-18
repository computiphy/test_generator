import pytest

# Define test function
def test_pm_data_request():
    # Setup step: Configure device to return up to 15 records using LPL with multiple observable bits set
    configure_device(15, ['BIT1', 'BIT2', 'BIT3'])

    # Step: Send request to device for PM data with the maximum number of records requested
    response = send_pm_data_request()

    # Verify that the received data length matches the total number of available records (up to 15)
    assert len(response) == 15

    # Parse received data and validate that all records are present, with valid values
    for record in response:
        validate_record(record)

# Predefined firmware functions
def configure_device(max_records, observable_bits):
    wait_for_state('READY', 3000)
    monitor_link_status(5000)
    validate_state_transition('INIT', 'READY')
    # Simulate configuring device to return up to max_records with specified observable bits
    pass

def send_pm_data_request():
    # Simulate sending request and returning response data
    return [f"Record {i}" for i in range(15)]

def validate_record(record):
    # Simulate validating record contains valid values
    assert "Valid Value" in record, f"Invalid record: {record}"

# Run the test
pytest.main()