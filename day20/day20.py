import os
basepath = os.path.dirname(os.path.abspath(__file__))

def get_neighbors(i, j, m, n):
    nbrs = []
    if i > 0:
        nbrs.append((i-1,j))
    if i < m-1:
        nbrs.append((i+1,j))
    if j > 0:
        nbrs.append((i,j-1))
    if j < n-1:
        nbrs.append((i,j+1))
    return nbrs

def print_grid(grid):
    print(stringify_grid(grid))

def stringify_grid(grid):
    s = ""
    for x in grid:
        for y in x:
            s += y if y is not None else '_'
        s += "\n"
    s += "\n"
    return s

dir_map = {'U': (-1,0), 'D': (1,0), 'L':(0,-1), 'R': (0,1)}


for filename in ['test_input.txt', 'input.txt']:
    print(filename)
    data = []

    with open(os.path.join(basepath, filename), 'r') as fin:
        for line in fin:
            data.append(line.strip())

    tot = 0
    tot2 = 0

    modules = {}
    module_types = {}
    for line in data:
        key = line.split("->")[0].strip()
        if "%" in key or "&" in key:
            module_types[key[1:]] = key[0]
            key = key[1:]
        vals = line.split("->")[1].strip().split(", ")
        modules[key] = vals
    # print(modules)
    # print(module_types)

    
    states = {key: 0 for key, val in module_types.items() if val == "%"}
    conj_states = {key: {} for key, val in module_types.items() if val == "&"}
    for key, vals in modules.items():
        for val in vals:
            if val not in module_types:
                continue
            if module_types[val] == "&":
                conj_states[val][key] = 0
    
    def states_to_tuples(states, conj_states):
        states_tuple = tuple((x,states[x]) for x in sorted(states.keys()))
        conj_states_tuple = tuple((key, tuple((x,conj_states[key][x]) for x in sorted(conj_states[key].keys()))) for key in sorted(conj_states.keys()))
        return states_tuple, conj_states_tuple

    def tuples_to_states(states_tuple, conj_states_tuple):
        states = dict(states_tuple)
        conj_states = {x: dict(y) for x,y in conj_states_tuple}
        return states, conj_states

    def get_subgraph(nodes):
        subgraph = set()
        new_nodes = set(x for x in nodes)
        while new_nodes:
            new_node = new_nodes.pop()
            subgraph.add(new_node)
            for key, val in modules.items():
                if new_node in val:
                    if key not in subgraph:
                        new_nodes.add(key)
        return subgraph
    
    subgraphs = []
    
    for x in modules["broadcaster"]:
        subgraph = get_subgraph([x])
        subgraphs.append(subgraph)


    
    def iterate(states_tuple, conj_states_tuple, cache, subgraph=None):
        if (states_tuple, conj_states_tuple) in cache:
            return cache[(states_tuple, conj_states_tuple)], True, {0:0, 1:0}
        states, conj_states = tuples_to_states(states_tuple, conj_states_tuple)
        curr_pulses = [('button', 'broadcaster', 0)]
        n_outputs = {0:0, 1:0}
        n_pulses = 0
        while curr_pulses:
            # print(curr_pulses[0])
            src, dest, pulse = curr_pulses.pop(0)
            if dest == 'rx' and pulse == 0:
                print('rx', n_pulses)
                raise Exception()
            n_outputs[pulse] += 1
            if subgraph is not None and dest not in subgraph:
                continue
            if dest not in module_types:
                if dest == 'output':
                    continue
                elif dest == 'broadcaster':
                    for dest2 in modules[dest]:
                        curr_pulses.append((dest, dest2, 0))
            elif module_types[dest] == "%":
                if pulse == 0:
                    states[dest] = 1 - states[dest]
                    for dest2 in modules[dest]:
                        curr_pulses.append((dest, dest2, states[dest]))
            elif module_types[dest] == "&":
                conj_states[dest][src] = pulse
                new_pulse = 1
                if not any([last_pulse == 0 for last_pulse in conj_states[dest].values()]):
                    new_pulse = 0
                for dest2 in modules[dest]:
                    curr_pulses.append((dest, dest2, new_pulse))
        states_tuple2, conj_states_tuple2 = states_to_tuples(states, conj_states)
        cache[(states_tuple, conj_states_tuple)] = (states_tuple2, conj_states_tuple2)
        return (states_tuple2, conj_states_tuple2), False, n_outputs

    cycle_lens = []
    for subgraph in subgraphs:
        print(subgraph)
        loop = False
        x = states_to_tuples(states, conj_states)
        past_states = []
        n_outputs_list = []
        i = 0
        cache = {}
        while not loop:# and i < 1000:
            i += 1
            past_states.append(x)
            x, loop, n_outputs_i = iterate(*x, cache, subgraph)
            n_outputs_list.append(n_outputs_i)
            # print(len(past_states))
        cycle_len = len(past_states) - 1
        print(cycle_len)
        cycle_lens.append(cycle_len)
        # n_outputs = {0:0, 1:0}
        # for n_outputs_i in n_outputs_list:
        #     for i2, j in n_outputs_i.items():
        #         n_outputs[i2] += j
        # if i < 1000:
        #     assert past_states[0] == past_states[-1]
        #     cycle_len = len(past_states) - 1
        #     print(cycle_len)
        #     n_cycles = 1000 / cycle_len
        # else:
        #     n_cycles = 1
        #     cycle_len = 1000
        # n_low = n_outputs[0] * n_cycles
        # n_high = n_outputs[1] * n_cycles
        # for i in range(1000 % cycle_len):
        #     n_low += n_outputs_i[0]
        #     n_high += n_outputs_i[1]

        # print(n_low * n_high)
        
    from math import lcm
    # No guarantee that it's exactly the LCM, I just assumed it would be
    # in general, you should go through each cycle, analyze states, and figure out the required states to output the correct result
    # then use Chinese Remainder Theorem or similar
    print(lcm(*cycle_lens))
    # print(tot)
    # print(tot2)

# 867118762
# 217317393039529