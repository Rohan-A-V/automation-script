import paramiko
import time
import json

# SSH connection details
ip_address = "192.168.1.1"
username = "root"
password = "Password123"

# Log file name
current_date = time.strftime("%d_%m_%Y")
log_file_name = f"attached_devices_{current_date}.txt"

# Command to get attached devices
cmd = "ubus call devwatchd.device get_attached_devices '{\"type\" : \"wired\"}'"

# Create SSH client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(ip_address, username=username, password=password)

# Open log file
with open(log_file_name, "a") as f:
    f.write(f"Attached devices log at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Execute command to get attached devices
    stdin, stdout, stderr = client.exec_command(cmd)

    # Parse and write attached devices to log file
    attached_devices = json.loads(stdout.read().decode())
    for device in attached_devices:
        f.write(f"{device['hostname']}, {device['mac']}\n")

    f.write("\n")

# Close SSH connection
client.close()
