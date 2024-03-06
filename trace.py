import json
import subprocess
import sys

class ListChangeIdentifier:
    def __init__(self, objects_index, list_index):
        self.objects_index = objects_index
        self.list_indices = list_index

        print(f"New ListChangeIdentifier({objects_index}, {list_index})")

class JavaObject:
    def __init__(self, instance, name, value):
        self.instance = instance
        self.name = name
        self.value = value

        print(f"New JavaObject('{instance}', {name}, {value})")

class State:
    empty_state = {
        'line': 0,
        'stdout': '',
        'heap': {},
        'stack_to_render': []
    }
    def __init__(self, state_dict, previous_state=empty_state):
        self.objects = []
        self.changes = []
        self.line_num = state_dict['line']
        self.stdout = state_dict['stdout']
        self.heap = state_dict['heap']

        ## For now, we only parse arrays and primitives ##
        encoded_locals = state_dict['stack_to_render'][0]['encoded_locals']
        for varname in state_dict['stack_to_render'][0]['ordered_varnames']:
            if varname == '__return__':
                continue

            if type(encoded_locals[varname]) is list:
                # Handle heap reference
                ref = encoded_locals[varname][1]
                heap_item = self.heap[str(ref)]

                if heap_item[0] == 'LIST': # handle list
                    list_var_old = None
                    for obj in previous_state.objects:
                        if obj.name == varname:
                            list_var_old = obj.value
                            break

                    list_var = []
                    for list_item in heap_item[1:]:
                        if type(list_item) is list: # Assume item 0 is "ELIDE"
                            for i in range(list_item[1]):
                                list_var.append(list_var[-1])
                        else:
                            list_var.append(list_item)

                    self.objects.append(JavaObject('LIST', varname, list_var))
                    for i in range(len(list_var)):
                        try:
                            if list_var[i] != list_var_old[i]: # Changed item
                                print(f"{varname}[{i}] changed from {list_var_old[i]} to {list_var[i]}")
                                self.changes.append(ListChangeIdentifier(len(self.objects) - 1, i))
                        except: # New item
                            self.changes.append(ListChangeIdentifier(len(self.objects) - 1, i))
            else: # Handle primitive data type
                self.objects.append(JavaObject('primitive', varname, encoded_locals[varname]))
                var_old = None
                for obj in previous_state.objects:
                    if obj.name == varname:
                        var_old = obj.value
                        break
                if var_old != encoded_locals[varname]:
                    pass
                    # TODO: PrimitiveChangeIdentifier


class Tracer:
    def __init__(self, usercode):
        self.states = []

        ## Run code through Traceprinter ##
        trace_input_dict = {
            "usercode": usercode,
            "options": {},
            "args": [], # massed to main()
            "stdin": ""
        }

        trace_input_json = json.dumps(trace_input_dict)

        # print(trace_input_json) # DEBUG

        traceprinter_command = "../java/bin/java -cp .:javax.json-1.0.jar:../java/lib/tools.jar traceprinter.InMemory"
        trace_proc = subprocess.Popen(traceprinter_command.split(),
                                      stdout=subprocess.PIPE,
                                      stdin=subprocess.PIPE,
                                      cwd="./traceprinter_backend/cp")

        trace_json = trace_proc.communicate(input=trace_input_json.encode())[0]

        # print(trace_json.decode('utf-8')) # DEBUG

        self.states = Tracer.parse(trace_json)

    def parse(trace_json):
        states = []

        trace_dict = json.loads(trace_json)
        trace = trace_dict['trace']

        for state in trace:
            print(f"\nNew State at states[{len(states)}]")
            if len(states) > 0:
                states.append(State(state, states[-1]))
            else:
                states.append(State(state))

        return states

# tracer = Tracer(open('Test.java').read()) # DEBUG
