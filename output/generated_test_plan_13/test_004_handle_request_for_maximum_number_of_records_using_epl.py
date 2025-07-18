import pytest

@pytest.mark.parametrize("max_records", [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
def test_pm_data_length(device, max_records):
    # Configure device to return up to 'max_records' records
    device.write_register('CONTROL', max_records)

    # Send request for PM data with the maximum number of records requested
    response = device.send_request('PM_DATA')

    # Verify that the received data length matches the total number of available records (up to 100)
    assert len(response) == min(max_records, 100), f"Expected at most 100 records but got {len(response)}"

    # Parse received data and validate that all records are present, with valid values
    for record in response:
        # Assuming each record is a dictionary or tuple with fields like 'id', 'value'
        assert isinstance(record, (dict, tuple))
        assert 'id' in record
        assert 'value' in record

    print(f"Test passed: Received {len(response)} records as expected.")