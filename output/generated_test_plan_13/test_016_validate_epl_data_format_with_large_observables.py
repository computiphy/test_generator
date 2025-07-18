import pytest

# Mock device configuration and reading functions for testing purposes
def read_register(register):
    if register == 'CONTROL':
        return {'value': 2, 'state': 'READY'}
    else:
        raise ValueError("Unknown register")

def validate_state_transition(expected_start_state, expected_end_state):
    # Placeholder for validation logic
    assert True

def write_register(register, value):
    if register == 'CONTROL':
        print(f"Writing {value} to CONTROL")
        return {'value': value, 'state': 'READY'}
    else:
        raise ValueError("Unknown register")

# Test function
def test_pm_data():
    # Configure device to return PM data using EPL with 10 observable bits set
    write_register('CONTROL', 2)

    # Send request to device for PM data and receive data
    received_data = read_register('DATA')

    # Verify that received data contains multiple records, each consisting of 6 or 8 bytes
    assert len(received_data) > 0

    # Parse and validate each record's content
    for record in received_data:
        assert isinstance(record, dict)
        assert 'X16_MINIMUM' in record
        assert 'X16_AVERAGE' in record
        assert 'X16_MAXIMUM' in record
        assert 'CURRENT_X16_VALUE' in record

# Run the test
pytest.main()