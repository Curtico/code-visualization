import json
import sys
import subprocess

#------------------#
# Main (obviously) #
#------------------#
def main(argv):
    trace_input_json = jsonify_java(sys.argv[1])

    # print(trace_input_json) # DEBUG

    traceprinter_command = "../java/bin/java -cp .:javax.json-1.0.jar:../java/lib/tools.jar traceprinter.InMemory"

    trace_proc = subprocess.Popen(traceprinter_command.split(),
                                  stdout=subprocess.PIPE,
                                  stdin=subprocess.PIPE,
                                  cwd="./traceprinter_backend/cp")

    trace_output_dict = json.loads(trace_proc.communicate(input=trace_input_json.encode())[0])

    step_bro(json.loads(trace_input_json), trace_output_dict)

#------------------------------------#
# Convert Java source to usable JSON #
#------------------------------------#
def jsonify_java(filename):
    # Initialize
    trace_input_dict = {
        "usercode": "",
        "options": {},
        "args": [],
        "stdin": ""
    }

    # Read source file
    source_code = open(filename, 'r')
    trace_input_dict["usercode"] = source_code.read()
    source_code.close()

    # Return
    return json.dumps(trace_input_dict)

#---------------------------------#
# PoC: Step through program trace #
#---------------------------------#
def step_bro(input_json, output_json):
    source_code = input_json['usercode'].split('\n') # Source code being traced
    events = output_json['trace'] # List of entries pertaining to program state
    for state in events:
        print(f"\n{state['event']}: <{state['stack_to_render'][0]['func_name']}>")
        print(f"\tCode: {state['line']} | {source_code[state['line'] - 1].strip()}")
        print(f"\tLocals: {state['stack_to_render'][0]['encoded_locals']}")
        print(f"\tGlobals: {state['globals']}")
        print(f"stdout: {{\n{state['stdout']}\n}}")
        print("")
        input("Press ENTER to continue...")

#---------------------------------#
# This is where the fun begins :D #
#---------------------------------#
if __name__ == "__main__":
    main(sys.argv)
