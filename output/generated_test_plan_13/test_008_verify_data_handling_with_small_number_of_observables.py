import pytest

@pytest.mark.parametrize("pm_data_length", [1, 2, 3, 4, 5])
def test_pm_data_length(monitor_link_status, read_register, wait_for_state, pm_data_length):
    monitor_link_status(5000)
    control_value = read_register('CONTROL')
    # Assuming control_value has a bit mask for PM data length
    # For example: PM data is in the last 4 bits of control_value
    expected_pm_count = (control_value & 0xF) + 1
    
    assert pm_data_length == expected_pm_count, f"Expected {expected_pm_count} records, but got {pm_data_length}"
    
    wait_for_state('READY', 3000)