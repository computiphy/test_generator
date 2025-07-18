import pytest
from datetime import datetime

# Mock device and observable configuration
class Device:
    def __init__(self):
        self.observable_bits = 8  # Example number of observable bits
        self.pm_data = None

    def read_register(self, register_name):
        # Simulate reading a control register to get observable data length
        if register_name == 'CONTROL':
            return self.observable_bits

    def monitor_link_status(self, timeout):
        # Simulate monitoring link status for the specified timeout (5000 ms)
        return True

def test_pm_data_received():
    device = Device()
    assert validate_state_transition('INIT', 'READY')
    assert device.monitor_link_status(5000)

    observable_bits = device.read_register('CONTROL')
    expected_length = observable_bits * 6 or observable_bits * 8
    response = send_request_to_device()
    
    # Check if the received data length matches the expected length
    assert len(response.data) == expected_length, "Received data length does not match expectation."

    # Parse and validate each record in the response
    for i, record in enumerate(response.records):
        # Validate that each record has 6 or 8 bytes (X16 minimum/average/max/current value)
        if observable_bits == 8:
            assert len(record) == 8, f"Record {i} is not 8 bytes."
        else:
            assert len(record) == 6, f"Record {i} is not 6 bytes."

# Function to simulate sending a request and returning the response
def send_request_to_device():
    # Mock response data with records of different lengths based on observable_bits
    if device.observable_bits == 8:
        return Response(data=[b'12345678', b'90ABCDEF'], records=[b'0123456', b'0123456'])
    else:
        return Response(data=[b'123456', b'7890'], records=[b'0123456'])

# Mock response class to simulate the structure of received data
class Response:
    def __init__(self, data, records):
        self.data = data
        self.records = records

# Test fixture for initializing the device and observable bits
@pytest.fixture(scope="module")
def setup_device():
    device = Device()
    yield device

# Test case using the setup fixture
def test_pm_data_received_with_fixture(setup_device):
    device = setup_device
    assert validate_state_transition('INIT', 'READY')
    assert device.monitor_link_status(5000)

    observable_bits = device.read_register('CONTROL')
    expected_length = observable_bits * 6 or observable_bits * 8
    response = send_request_to_device()
    
    # Check if the received data length matches the expected length
    assert len(response.data) == expected_length, "Received data length does not match expectation."

    # Parse and validate each record in the response
    for i, record in enumerate(response.records):
        # Validate that each record has 6 or 8 bytes (X16 minimum/average/max/current value)
        if observable_bits == 8:
            assert len(record) == 8, f"Record {i} is not 8 bytes."
        else:
            assert len(record) == 6, f"Record {i} is not 6 bytes."

# Function to validate state transition
def validate_state_transition(current_state, target_state):
    # Simulate a simple state transition validation for demonstration purposes
    return current_state == 'INIT' and target_state == 'READY'