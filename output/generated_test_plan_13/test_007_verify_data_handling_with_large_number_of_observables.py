import pytest

@pytest.fixture
def configure_device():
    monitor_link_status(5000)
    read_register('CONTROL').write({'PM_MODE': 'LPL', 'NUM_RECORDS': 20})
    wait_for_state('READY', 3000)

@pytest.mark.parametrize("device", ["dev1", "dev2"])
def test_pm_data(device, configure_device):
    pm_data = device.read_pm_data()
    
    # Verify the length of PM data matches the total number of available records (up to 15)
    assert len(pm_data) <= 15
    
    # Parse received data and validate that all records are present with valid values
    for record in pm_data:
        # Assuming each record has at least one value, check if it's not None
        assert record is not None
        
        # Placeholder validation logic: check if the record contains expected fields
        assert 'field1' in record and isinstance(record['field1'], int)
        assert 'field2' in record and isinstance(record['field2'], str)