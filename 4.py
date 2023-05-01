import paramiko
import time
from datetime import datetime

channel_2g_command = ["iwlist ath0 chan | grep -i Frequency | awk '{print $5}' | tail -1", 'Operating Channel 2GHz']
channel_5g_command = ["iwlist ath1 chan | grep -i Frequency | awk '{print $5}' | tail -1", 'Operating Channel 5GHz']
memory_command = ["free -h | grep -i Mem | awk '{print $2,$3,$4}'", 'Total Memory, Used Memory, Free Memory']
cpu_utilization_command = ["mpstat | grep -i all | awk '{print $3,$5}'", 'CPU Utilization user, system']
uptime_command = ['uptime', 'Uptime']
client_connection_2g_command = ["wlanconfig ath0 list sta | grep NULL | awk '{print $1,$20}'", '2G Clients, Association time']
client_connection_5g_command = ["wlanconfig ath1 list sta | grep NULL | awk '{print $1,$20}'", '5G Clients, Association time']

command_list = [memory_command, cpu_utilization_command, uptime_command, client_connection_2g_command, client_connection_5g_command]

ip_address = "192.168.1.1"
password = "Password123"
monitoring_time = 1
memory_threshold = 50

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip_address, '22', 'root', password)

def check_memory_leakage(total_memory, used_memory, free_memory):
    if free_memory / total_memory * 100 < memory_threshold:
        print("Memory leakage detected! Free memory is less than 50% of total memory.")

def router_monitor():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d_%m_%Y")

    with open(f'long_run_logs_{current_date}.txt', 'a') as log_file:
        log_file.write(f"{'*'*50} {current_time} {'*'*50}\n")
        for i in command_list:
            stdin, stdout, stderr = ssh.exec_command(i[0])
            lines = stdout.readlines()
            log_file.write(i[1] + '\n')
            for output in lines:
                log_file.write(output)
            if i == memory_command:
                memory_info = lines[0].split()
                check_memory_leakage(int(memory_info[0][:-1]), int(memory_info[1][:-1]), int(memory_info[2][:-1]))
            log_file.write('\n')

while True:
    router_monitor()
    print(f"Monitoring in progress... Sleep time {monitoring_time} minute(s)")
    time.sleep(monitoring_time * 60)
