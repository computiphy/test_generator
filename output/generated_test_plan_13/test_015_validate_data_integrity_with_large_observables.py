import pytest

@pytest.fixture(scope='module')
def device_under_test():
    # Simulate setting up a device under test
    simulate_power_cycle()
    write_register('CONTROL', 1)
    return 'device'

def read_pm_data(device):
    # Simulate reading PM data from the device
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

def write_pm_data(device, data):
    # Simulate writing PM data to the device
    return f"Data {data} written to {device}"

@pytest.mark.parametrize('modify_data', [(lambda x: [x[i] for i in range(len(x)) if i % 2 == 0])])
def test_modify_pm_data(device_under_test, modify_data):
    # Read PM data from the device
    original_data = read_pm_data(device_under_test)
    
    # Modify received data
    modified_data = modify_data(original_data)
    
    # Write modified data back to the device
    response = write_pm_data(device_under_test, modified_data)
    
    # Verify that the device rejects or handles the modified data correctly
    assert "Rejected" in response or "Invalid" in response, "Device should reject or handle modified data"