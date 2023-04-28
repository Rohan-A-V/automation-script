import paramiko
import time
import json

# Command to get attached devices
command = 'ubus call devwatchd.device get_attached_devices \'{"type" : "wired"}\''

# SSH credentials
ip_address = "192.168.1.1"
password = "Password123"

# Connect to the router via SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip_address, '22', 'root', password)

# Open the log file
log_file_name = 'attached_devices_log.txt'
with open(log_file_name, 'w') as log_file:
    log_file.write('Attached devices log\n')

    while True:
        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)

        # Read the output
        output = stdout.read().decode('utf-8')

        # Convert the output to a JSON object
        attached_devices = json.loads(output)

        # Write the attached devices to the log file
        log_file.write(f'\n{time.ctime()}\n')
        for device in attached_devices['devices']:
            log_file.write(f'{device["name"]}: {device["mac"]}\n')

        # Wait for 1 minute before executing the command again
        time.sleep(60)

# Close the SSH connection
ssh.close()
