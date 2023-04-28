import paramiko
import time
import json
from datetime import datetime

# SSH connection parameters
ip_address = "192.168.1.1"
port = 22
username = "root"
password = "Password123"

# Command to get attached devices
cmd = 'ubus call devwatchd.device get_attached_devices \'{"type": "wired"}\''

# Interval to get attached devices in seconds
interval = 10

# Function to execute SSH command and return output
def run_command_ssh(ip_address, port, username, password, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, port, username, password)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode('utf-8')
    ssh.close()
    return output.strip()

# Function to get attached devices and write to file
def log_attached_devices():
    while True:
        # Get current time and date
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%d_%m_%Y")

        # Get attached devices and convert to JSON format
        devices_output = run_command_ssh(ip_address, port, username, password, cmd)
        attached_devices = json.loads(devices_output)

        # Write attached devices to file
        with open(f'attached_devices_logs_{current_date}.txt', 'a') as log_file:
            log_file.write(f'Attached devices at {current_time}:\n')
            for device in attached_devices:
                log_file.write(f'{device["name"]}, MAC Address: {device["mac"]}\n')

        # Wait for specified interval
        time.sleep(interval)

# Call log_attached_devices function
log_attached_devices()
