import paramiko
import time
import matplotlib.pyplot as plt
from datetime import datetime

#brctl_command = ['brctl show', 'brctl show']
channel_2g_command = ["iwlist ath0 chan | grep -i Frequency | awk '{print $5}' | tail -1", 'Operating Channel 2GHz']
channel_5g_command = ["iwlist ath1 chan | grep -i Frequency | awk '{print $5}' | tail -1", 'Operating Channel 5GHz']
memory_command = ["free -h | grep -i Mem | awk '{print $2/1024,$3/1024,$4/1024}'", 'Total Memory, Used Memory, Free Memory (GB)']
cpu_utilization_command = ["mpstat | grep -i all | awk '{print $3,$5}'", 'CPU Utilization user, system']
uptime_command = ['uptime', 'Uptime']
client_connection_2g_command = ["wlanconfig ath0 list sta | grep NULL | awk '{print $1,$20}'", '2G Clinets, Association time']
client_connection_5g_command = ["wlanconfig ath1 list sta | grep NULL | awk '{print $1,$20}'", '5G Clinets, Association time']
#logread_command = 'logread'
#dmesg_command = 'dmesg'

command_list = [memory_command, cpu_utilization_command, uptime_command, client_connection_2g_command, client_connection_5g_command]

now = datetime.now()
current_date = now.strftime("%d_%m_%Y")

Router_log_file_name = 'long_run_logs_' + current_date + '.txt'
#dmesg_log_file_name = 'dmesg_logs_' + current_date + '.txt'
#logread_log_file_name = 'logread_logs_' + current_date + '.txt'

ip_address = "192.168.1.1"
Password = "Password123"
monitoring_time = 1

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip_address, '22', 'root', Password)

# Initialize empty lists to store memory and CPU data
mem_data = []
cpu_data = []

def router_monitor():
    global mem_data, cpu_data
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d_%m_%Y")
    #print(current_date, current_time)

    with open(Router_log_file_name, 'a') as log_file:
        log_file.write("%s %s %s\n" % (str('*'*50), str(current_time), str('*'*50)))
        for i in command_list:
            stdin, stdout, stderr = ssh.exec_command(i[0])
            lines = stdout.readlines()
            log_file.write(str(i[1]))
            log_file.write('\n')
            for output in lines:
                #log_file.write("%s %s\n" % (str(i), str(output)))
                log_file.write(str(output))
                if 'Memory' in i[1]:
                    mem_data.append(float(output.split()[1]))
                elif 'CPU' in i[1]:
                    cpu_data.append(float(output.split()[0]))
            log_file.write('\n')
    print(f"Memory Data: {mem_data}")
    print(f"CPU Data: {cpu_data}")

# Function to plot memory data
def plot_memory_data():
    plt.plot(mem_data)
    plt.title('Memory Utilization')
