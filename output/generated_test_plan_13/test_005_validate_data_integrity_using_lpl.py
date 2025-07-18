import pytest

def test_pm_data_handling():
    # Simulate a power cycle to reset the device
    simulate_power_cycle()
    
    # Read current control register value and set it to 1
    initial_control = read_register('CONTROL')
    write_register('CONTROL', 1)
    
    # Send request for PM data using LPL with a specific observable set
    pm_data_request = send_request_to_device('LPL', observable_set='specific_set')
    
    # Receive and store the data received from the device
    received_pm_data = receive_data()
    
    # Modify the received data (e.g., swap values)
    modified_pm_data = swap_values(received_pm_data)
    
    # Send the modified data back to the device
    send_modified_data(modified_pm_data)
    
    # Verify that the device rejects or handles the modified data correctly
    verify_device_response()