import subprocess, time, filecmp, os
import sys, traceback

TIMEOUT = 60
FILENAME = 'Firefox_Final_VO.ogv'

print("=" * 100)
print("===> Test case 3.1. Large File transfer test without packet loss")

execution_dir_1 = '/18441_project3/localtest/node1/'
execution_dir_2 = '/18441_project3/localtest/node2/'

solution_path = '/18441_project3/solution/tcpserver.py'

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

node_process_list[1].stdin.write(FILENAME + '\n')
node_process_list[1].stdin.flush()
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

# Check the case where file does not exist

return_bool = False
check_exists_bool = os.path.exists(execution_dir_2+FILENAME)
if check_exists_bool:
	return_bool = filecmp.cmp(execution_dir_1+FILENAME, execution_dir_2+FILENAME, shallow=False)
	# os.remove(execution_dir_2+FILENAME)

if return_bool:
	print("===> Test Case Success")
else:
	print("===> Test Case Fail")
print("=" * 100)