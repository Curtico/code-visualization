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

    # DEBUG
    #print(json.dumps(trace_output_dict))
    #quit()

    step_bro(json.loads(trace_input_json), trace_output_dict)

#------------------------------------#
# Convert Java source to usable JSON #
#------------------------------------#
def jsonify_java(filename):
    # Initialize
    trace_input_dict = {
        "usercode": "",
        "options": {},
        "args": [], # passed to main()
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

        print_locals(state)

        print(f"\tGlobals: {state['globals']}")
        print(f"stdout: {{\n{state['stdout']}\n}}")
        print("")
        input("Press ENTER to continue...")

def print_locals(state):
    encoded_locals = state['stack_to_render'][0]['encoded_locals']

    print("\tLocals:")
    for var in encoded_locals:
        if isinstance(encoded_locals[var], list):
            if encoded_locals[var][0] == "REF":
                print(f"\t\t{var}:", get_heap_item(state, encoded_locals[var][1]))
        else:
            print(f"\t\t{var}:", encoded_locals[var])

def get_heap_item(state, heap_id):
    heap_item_type = state['heap'][str(heap_id)][0]
    if heap_item_type == 'LIST':
        return get_list(state, heap_id)
    else:
        return f"UNKOWN DATA TYPE: {heap_item_type}"

def get_list(state, heap_id):
    old_list = state['heap'][str(heap_id)]
    new_list = []
    for item in old_list[1:]:
        if isinstance(item, list):
            if item[0] == 'ELIDE':
                prev_item = new_list[-1]
                for i in range(item[1]):
                    new_list.append(prev_item)
            else:
                print("ERROR: unknown:", item)
        else:
            new_list.append(item)

    return new_list

#---------------------------------#
# This is where the fun begins :D #
#---------------------------------#
if __name__ == "__main__":
    main(sys.argv)
