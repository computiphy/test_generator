import pytest

def configure_pmda_with_observable_set(observable_set):
    # Assume a function to set observable set in device
    pass

def simulate_data_transfer(data):
    # Assume a function to send and receive data from the device
    pass

def swap_values_in_data(data):
    # Swap values for demonstration purposes
    return [10 - value for value in data]

def test_pmda_pm_data_handling():
    # Prepare observable set
    observable_set = ['PM1', 'PM2', 'PM3']
    
    # Configure device to return PM data with the observable set
    configure_pmda_with_observable_set(observable_set)
    
    # Simulate power cycle to ensure device is in READY state
    simulate_power_cycle()
    
    # Read control register to validate transition
    read_register('CONTROL')
    validate_state_transition('INIT', 'READY')
    
    # Send request for PM data and receive it
    raw_data = simulate_data_transfer(observable_set)
    
    # Modify the received data (e.g., swap values)
    modified_data = swap_values_in_data(raw_data)
    
    # Attempt to send modified data back to the device
    # Assuming an error or rejection mechanism is part of the test setup
    try:
        simulate_data_transfer(modified_data)
    except Exception as e:
        assert 'error' in str(e), "Device should reject or handle the modified data"