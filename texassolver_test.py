from subprocess import Popen, PIPE
# Must be python 3.4 or higher:
from pathlib import Path

# Code taken from colab:

def make_round_str(round,player,bet,raise_str,donk,allin):
  retstr = ""
  if bet:
    retstr += f"set_bet_sizes {player},{round},bet,{bet}\n"
  if raise_str:
    retstr += f"set_bet_sizes {player},{round},raise,{raise_str}\n"
  if donk:
    retstr += f"set_bet_sizes {player},{round},donk,{donk}\n"
  if allin:
    retstr += f"set_bet_sizes {player},{round},allin\n"
  return retstr

#@title Solver Global settings { run: "auto" }

pot = 50 #@param
effective_stack = 70 #@param

ip_range = "AA,KK,QQ,JJ,TT,99:0.75,88:0.75,77:0.5,66:0.25,55:0.25,AK,AQs,AQo:0.75,AJs,AJo:0.5,ATs:0.75,A6s:0.25,A5s:0.75,A4s:0.75,A3s:0.5,A2s:0.5,KQs,KQo:0.5,KJs,KTs:0.75,K5s:0.25,K4s:0.25,QJs:0.75,QTs:0.75,Q9s:0.5,JTs:0.75,J9s:0.75,J8s:0.75,T9s:0.75,T8s:0.75,T7s:0.75,98s:0.75,97s:0.75,96s:0.5,87s:0.75,86s:0.5,85s:0.5,76s:0.75,75s:0.5,65s:0.75,64s:0.5,54s:0.75,53s:0.5,43s:0.5" #@param {type:"string"}
oop_range = "QQ:0.5,JJ:0.75,TT,99,88,77,66,55,44,33,22,AKo:0.25,AQs,AQo:0.75,AJs,AJo:0.75,ATs,ATo:0.75,A9s,A8s,A7s,A6s,A5s,A4s,A3s,A2s,KQ,KJ,KTs,KTo:0.5,K9s,K8s,K7s,K6s,K5s,K4s:0.5,K3s:0.5,K2s:0.5,QJ,QTs,Q9s,Q8s,Q7s,JTs,JTo:0.5,J9s,J8s,T9s,T8s,T7s,98s,97s,96s,87s,86s,76s,75s,65s,64s,54s,53s,43s" #@param {type:"string"}
board = "Qs,Jh,2h" #@param {type:"string"}

allin_threshold =  0.80#@param
thread_num =  2#@param
accuracy_percent = 5.0 #@param
max_iteration = 200 #@param {type:"integer"}
print_interval = 10 #@param {type:"integer"}
use_isomorphism = True #@param {type:"boolean"}

dump_rounds = 1 #@param {type:"integer"}

global_setting = f"""set_pot {pot}
set_effective_stack {effective_stack}
set_board {board}
set_range_ip {ip_range}
set_range_oop {oop_range}
set_allin_threshold {allin_threshold}
set_thread_num {thread_num}
set_accuracy {accuracy_percent}
set_max_iteration {max_iteration}
set_print_interval {print_interval}
set_use_isomorphism {int(print_interval)}
set_dump_rounds {dump_rounds}
"""

#@title Flop setting { run: "auto" }
flop_ip_bet_sizes = "50,100" #@param {type:"string"}
flop_ip_raise_sizes = "50" #@param {type:"string"}
flop_ip_allin = True #@param {type:"boolean"}

flop_oop_bet_sizes = "50" #@param {type:"string"}
flop_oop_raise_sizes = "50" #@param {type:"string"}
flop_oop_allin = True #@param {type:"boolean"}

flop_setting = make_round_str("flop","ip",flop_ip_bet_sizes,flop_ip_raise_sizes,None,flop_ip_allin)
flop_setting += make_round_str("flop","oop",flop_oop_bet_sizes,flop_oop_raise_sizes,None,flop_oop_allin)

#@title Turn setting { run: "auto" }
turn_ip_bet_sizes = "50" #@param {type:"string"}
turn_ip_raise_sizes = "50" #@param {type:"string"}
turn_ip_allin = True #@param {type:"boolean"}

turn_oop_bet_sizes = "50" #@param {type:"string"}
turn_oop_raise_sizes = "50" #@param {type:"string"}
turn_oop_donk_sizes = "" #@param {type:"string"}
turn_oop_allin = True #@param {type:"boolean"}

turn_setting = make_round_str("turn","ip",turn_ip_bet_sizes,turn_ip_raise_sizes,None,turn_ip_allin)
turn_setting += make_round_str("turn","oop",turn_oop_bet_sizes,turn_oop_raise_sizes,turn_oop_donk_sizes,turn_oop_allin)

#@title River setting { run: "auto" }
river_ip_bet_sizes = "50" #@param {type:"string"}
river_ip_raise_sizes = "50" #@param {type:"string"}
river_ip_allin = True #@param {type:"boolean"}

river_oop_bet_sizes = "50" #@param {type:"string"}
river_oop_raise_sizes = "50" #@param {type:"string"}
river_oop_donk_sizes = "" #@param {type:"string"}
river_oop_allin = True #@param {type:"boolean"}

river_setting = make_round_str("river","ip",river_ip_bet_sizes,river_ip_raise_sizes,None,river_ip_allin)
river_setting += make_round_str("river","oop",river_oop_bet_sizes,river_oop_raise_sizes,river_oop_donk_sizes,river_oop_allin)

#@title <- Press here to start solving (Could be 30~60x *slower* than you PC)

input_str = global_setting + flop_setting + turn_setting + river_setting + """build_tree
start_solve
dump_result output_result.json
"""

# Code added for testing:

# Get the path for console_solver.exe:
base_path = Path(__file__).parent
command = str(base_path / 'TexasSolver-v0.2.0-Windows/console_solver.exe')

# Run the command asynchronously
p = Popen(command, shell=True, stdout=PIPE, stdin=PIPE)

# Write some input to the process
p.stdin.write(input_data.encode())

# Close the stdin stream to signal the end of the input
p.stdin.close()

# Wait for the command to complete
p.wait()

# Read the output of the command
output = p.stdout.read()

# Print the output
print(output.decode())
