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

    trace_output_json = json.loads(trace_proc.communicate(input=trace_input_json.encode())[0])

    print(json.dumps(trace_output_json))

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
# This is where the fun begins :D #
#---------------------------------#
if __name__ == "__main__":
    main(sys.argv)
