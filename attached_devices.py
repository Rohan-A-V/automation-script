import subprocess
import json
import paramiko
import time
from datetime import datetime

def get_attached_devices():
    # Define the command to execute
    cmd = ["ubus", "call", "devwatchd.device", "get_attached_devices", '{"type" : "wired"}']

    # Execute the command and capture the output
    output = subprocess.check_output(cmd)

    # Parse the JSON output into a Python object
    attached_devices = json.loads(output)

    # Print information about the attached devices
    for device in attached_devices:
        print("MAC address:", device.get("macaddr"))
        print("Interface name:", device.get("iface"))
        print("Device type:", device.get("type"))
        print("Device name:", device.get("name"))

ip_address = "192.168.1.1"
Password = "Password123"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip_address, '22', 'root', Password)

def router_monitor():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d_%m_%Y")
  
    with open("router_log.txt", "a") as log_file:
        log_file.write(f"{'*'*50} {current_time} {'*'*50}\n")
        for command in command_list:
            stdin, stdout, stderr = ssh.exec_command(command[0])
            output = stdout.read().decode().strip()
            log_file.write(f"{command[1]}:\n{output}\n")
        log_file.write("\n")
    get_attached_devices()

command_list = [channel_2g_command, channel_5g_command, memory_command, cpu_utilization_command, uptime_command, client_connection_2g_command, client_connection_5g_command]

while True:
    router_monitor()
    print('Monitoring In Progress....Sleep Time ',monitoring_time, 'Minutes')
    time.sleep(int(monitoring_time)*60)
