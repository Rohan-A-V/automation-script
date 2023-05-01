import re
import matplotlib.pyplot as plt
import paramiko

memory_command = ["free -h | grep -i Mem | awk '{print $2,$3,$4}'", 'Total Memory, Used Memory, Free Memory']
cpu_utilization_command = ["mpstat | grep -i all | awk '{print $3,$5}'", 'CPU Utilization user, system']
uptime_command = ['uptime', 'Uptime']

def plot_sys_info(server_ip, username, password):
    # Connect to the server
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=server_ip, username=username, password=password)

    # Get CPU utilization
    stdin, stdout, stderr = ssh_client.exec_command(" ".join(cpu_utilization_command))
    cpu_output = stdout.read().decode("utf-8").strip()
    cpu_utilization = re.findall(r"(\d+\.\d+)", cpu_output)
    cpu_utilization = list(map(float, cpu_utilization))

    # Get memory usage
    stdin, stdout, stderr = ssh_client.exec_command(" ".join(memory_command))
    memory_output = stdout.read().decode("utf-8").strip()
    memory_usage = memory_output.split()
    total_memory = float(memory_usage[0][:-1])
    used_memory = float(memory_usage[1][:-1])
    free_memory = float(memory_usage[2][:-1])

    # Get uptime
    stdin, stdout, stderr = ssh_client.exec_command(" ".join(uptime_command))
    uptime_output = stdout.read().decode("utf-8").strip()
    uptime = uptime_output.split()[2:]

    # Plot graph
    plt.plot(['Used Memory'], [used_memory], '-o', label='Used Memory')
    plt.plot(['CPU Utilization'], [cpu_utilization[0]], '-o', label='CPU Utilization')
    plt.ylim(0, 100)
    plt.ylabel('Usage (%)')
    plt.title('System Information')
    plt.legend()

    plt.show()
