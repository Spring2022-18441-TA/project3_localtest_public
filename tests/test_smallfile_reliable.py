import subprocess, time, filecmp, os
import sys, traceback, signal
from kill_command import kill_command

TIMEOUT = 10

FILENAME = 'Carnegie_Mellon_University.jpg'

Packet_Drop_Probability = 0.05 # 5%


print("=" * 100)
print("===> Test case 5.1. Small File transfer test with packet loss")

execution_dir_1 = '/18441_project3/localtest/node1/'
execution_dir_2 = '/18441_project3/localtest/node2/'

solution_path = '/18441_project3/solution/tcpserver.py'
# solution_path = '/18441_project3/solution/udpserver.py'

print("===> Activate Packet Drop")
shell_command_line_for_packet_drop = "python3 /18441_project3/localtest/packet_drop_scripts/nf_python.py %f" % Packet_Drop_Probability
print(shell_command_line_for_packet_drop)
pdrop_proc = subprocess.Popen(shell_command_line_for_packet_drop, shell=True)

activate_cmd = "/18441_project3/localtest/packet_drop_scripts/set-iptable.sh"
os.system(activate_cmd)

print("===> Setup Connection")

node_process_list = []
shell_command_line_1 = 'python3 %s node1.json\n' % solution_path
shell_command_line_2 = 'python3 %s node2.json\n' % solution_path
proc = subprocess.Popen(shell_command_line_1, stdin=subprocess.PIPE, shell=True, universal_newlines=True, cwd=execution_dir_1)
node_process_list.append(proc)
proc = subprocess.Popen(shell_command_line_2, stdin=subprocess.PIPE, shell=True, universal_newlines=True, cwd=execution_dir_2)
node_process_list.append(proc)
time.sleep(2)

print("===> Request a small file and wait")

node_process_list[0].stdin.write(FILENAME + '\n')
node_process_list[0].stdin.flush()
time.sleep(TIMEOUT)

print("===> Kill nodes")
try:
	print("kill process1")
	node_process_list[0].kill()
except:
	traceback.print_exc()

try:
	print("kill process2")
	node_process_list[1].kill()
except:
	traceback.print_exc()

kill_command()


return_bool = False
check_exists_bool = os.path.exists(execution_dir_1+FILENAME)
if check_exists_bool:
	return_bool = filecmp.cmp(execution_dir_1+FILENAME, execution_dir_2+FILENAME, shallow=False)
	# os.remove(execution_dir_1+FILENAME)

if return_bool:
	print("===> Test Case Success")
else:
	print("===> Test Case Fail")

print("=" * 100)

print("===> Deactivate Packet Drop")
deactivate_cmd = "/18441_project3/localtest/packet_drop_scripts/unset-iptable.sh"
os.system(deactivate_cmd)
try:
	print("kill nf_python")
	os.killpg(os.getpgid(pdrop_proc.pid), signal.SIGTERM)
except:
	traceback.print_exc()
