import matplotlib.pyplot as plt
import numpy as np

def plot_data(cpu_data, memory_data):
    x = np.arange(len(cpu_data))
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Time (min)')
    ax1.set_ylabel('CPU Utilization (%)', color=color)
    ax1.plot(x, cpu_data, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()

    color = 'tab:blue'
    ax2.set_ylabel('Memory Usage (GB)', color=color)
    ax2.plot(x, memory_data, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.savefig('usage_graph.png')

    #######################################################################################33
    
    def router_monitor():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d_%m_%Y")

    cpu_data = []
    memory_data = []

    with open(Router_log_file_name, 'a') as log_file:
        log_file.write("%s %s %s\n" % (str('*' * 50), str(current_time), str('*' * 50)))
        for i in command_list:
            stdin, stdout, stderr = ssh.exec_command(i[0])
            lines = stdout.readlines()
            log_file.write(str(i[1]))
            log_file.write('\n')
            for output in lines:
                log_file.write(str(output))
                if i[1].startswith('CPU'):
                    cpu_data.append(float(output.split()[0]))
                elif i[1].startswith('Total Memory'):
                    memory_data.append(float(output.split()[1]) / 1024 / 1024 / 1024)
            log_file.write('\n')

        # Plot the data
        if len(cpu_data) > 0 and len(memory_data) > 0:
            plot_data(cpu_data, memory_data)
