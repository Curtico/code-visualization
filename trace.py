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

    trace_proc = subprocess.Popen(traceprinter_command.split(), stdout=subprocess.PIPE, stdin=subprocess.PIPE, cwd="./traceprinter_backend/cp")

    trace_output_json = trace_proc.communicate(input=trace_input_json.encode())[0]

    print(trace_output_json.decode('utf-8'))

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

    # Put all the code on one line
    source_code = open(filename, 'r')
    while line := source_code.readline().strip():
        trace_input_dict["usercode"] += line + ' '

    source_code.close()
    trace_input_dict["usercode"] = trace_input_dict["usercode"].strip()

    # Return
    return json.dumps(trace_input_dict)

#---------------------------------#
# This is where the fun begins :D #
#---------------------------------#
if __name__ == "__main__":
    main(sys.argv)
