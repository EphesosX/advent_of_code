import os
import re
import tqdm
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils import *

basepath = os.path.dirname(os.path.abspath(__file__))

for filename in ['test_input.txt', 'test_input2.txt', 'input.txt']:
    print(filename)
    # if filename[0] != "t":
    #     break
    tot = 0
    tot2 = 0

    lines = []
    grid = []
    with open(os.path.join(basepath, filename), 'r') as fin:
        lines = [x.strip() for x in fin]
        grid = [[x for x in line] for line in lines]

    inputs = {}
    gates = []
    for line in lines:
        if ':' in line:
            wire, val = line.split(":")
            val = int(val.strip())
            inputs[wire] = val
        elif '->' in line:
            stmt, dst = line.split('->')
            dst = dst.strip()
            stmt = tuple(stmt.strip().split(" "))
            gates.append((stmt, dst))
    
    gates_ = [x for x in gates]

    def evaluate(inputs, gates):
        values = {x:y for x,y in inputs.items()}
        while gates:
            stmt, dst = gates.pop(0)
            x1, op, x2 = stmt
            if x1 not in values or x2 not in values:
                gates.append((stmt, dst))
                continue
            if op == "AND":
                values[dst] = values[x1] & values[x2]
            elif op == "XOR":
                values[dst] = values[x1] ^ values[x2]
            elif op == "OR":
                values[dst] = values[x1] | values[x2] 
        return values
    values = evaluate(inputs, gates)

    # print(values)
    z_keys = sorted([key for key in values if key[0]=="z"])
    for z_key in sorted(z_keys, reverse=True):
        tot *= 2
        tot += values[z_key]
    print(tot)
    if filename[0] != "t":
        gates = gates_
        print(len(gates), len(z_keys))
        gate_map = {x:y for x,y in gates}
        and_count = 0
        or_count = 0
        xor_count = 0
        for z_key in z_keys:
            x_key = "x" + z_key[1:]
            y_key = "y" + z_key[1:]
            if (x_key, "XOR", y_key) in gate_map:
                print(z_key, gate_map[(x_key, "XOR", y_key)])
        x_keys = ["x" + z_key[1:] for z_key in z_keys]
        y_keys = ["y" + z_key[1:] for z_key in z_keys]
        inputs = set()
        outputs = set()
        use_counts = {}
        for stmt, out in gates:
            input1, op, input2 = stmt
            inputs.add(input1)
            inputs.add(input2)
            use_counts[input1] = use_counts.get(input1, 0) + 1
            use_counts[input2] = use_counts.get(input2, 0) + 1
            outputs.add(out)
            if op == "AND":
                and_count += 1
            elif op == "OR":
                or_count += 1
            elif op == "XOR":
                xor_count += 1
        print(len(gates), len(inputs), len(outputs))
        print(and_count, or_count, xor_count)
        print([x for x in outputs if x not in inputs])
        count_uses = {}
        for use, count in use_counts.items():
            count_uses[count] = count_uses.get(count, 0) + 1
        print(count_uses)
        for x_key, y_key in zip(x_keys, y_keys):
            a = 0
            b = 0
            ops = []
            for stmt, out in gates:
                input1, op, input2 = stmt
                if input1 in [x_key, y_key] and input2 in [x_key, y_key]:
                    b += 1
                    ops.append(op)
            # print(ops)

        # 222 gates, 266 inputs, 46 outputs
        # 89 AND, 44 XOR, 89 OR
        # 45 x values, 45 y values used only in XOR or AND
        # seems like this is a minimal adder, so construct it and try and match up the labels
        # z_k+1 = (x_k+1 XOR y_k+1) XOR ((x_k AND y_k) OR ((x_k-1 AND x_k-1) AND (x_k XOR y_k))
        # z_0 = (x_0 XOR y_0)
        # z_max = (x_max AND y_max) OR ((x_max XOR y_max) AND carry_max-1)

        add_gates = []
        val_map = {}
        gate_map = {stmt: out for stmt, out in gates}
        for x_key, y_key in zip(x_keys, y_keys):
            for stmt, out in gates:
                input1, op, input2 = stmt
                if input1 in [x_key, y_key] and input2 in [x_key, y_key]:
                    # gate_map[stmt] = out
                    pass
        out_gates = rmap(gate_map)

        bad_z = []
        for i, xy in enumerate(zip(x_keys, y_keys)):
            x_key, y_key = xy
            test_map = val_map.copy()
            if i == 0:
                val_map[z_keys[i]] = gate_map[(x_key, "AND", y_key)]
            else:
                final1, xor, final2 = out_gates[z_keys[i]]
                
                if xor != "XOR":
                    print(z_keys[i])
                    bad_z.append(i)
        
        bad_z.append(15)
        for i in bad_z:
            x_key = x_keys[i]
            y_key = y_keys[i]
            z_key = z_keys[i]
            print("Z:", z_key)
            xandy = gate_map.get((x_key, "AND", y_key), gate_map.get((y_key, "AND", x_key), None))
            xxory = gate_map.get((x_key, "XOR", y_key), gate_map.get((y_key, "XOR", x_key), None))
            print("AND: ", xandy)
            print("XOR: ", xxory)
            print(out_gates[z_key], z_key)
            for stmt, out in gate_map.items():
                if xandy in stmt or xxory in stmt:
                    print(stmt, out)

            in_1, op, in_2 = out_gates[z_key]
            if in_1 in out_gates:
                print(out_gates[in_1], in_1)
            if in_2 in out_gates:
                print(out_gates[in_2], in_2)
            
            
            input()

        # z01:
        # (rvh xor kgc) -> z01
        # (x00 and y00) -> rvh
        # (x01 xor y01) -> kgc
        # (rvh and kgc) -> vtk (carry bit)

        # z02:
        # (fbc xor vbf) -> z02
        # (vtk or (x01 and y01)) -> fbc
        # (x02 xor y02) -> vbf

        # z08:
        # dnn AND (x08 xor y08) -> z08
        # (x and y) OR ((x xor y) xor dnn) -> fqs
        # dnn = ((x07 and y07) or ckq)

        # want:
        # z08 = (op1 xor dqd)
        # (carry or (x07 and y07)) -> op1
        # (x08 xor y08) -> dqd
        # swap: ffj, z08
        # op1 = dnn

        # z22:
        # x22 and y22 -> z22
        # x22 xor y22 -> hgq
        # hgq xor pgt -> gjh
        # swap: gjh, z22

        # z31:
        # swap jdr, z31?

        # z45: doesn't count

        # z15:
        # tpr xor dwp -> z15
        # x15 and y15 -> dwp
        # wkm or pwq -> tpr
        # 

        def swap(d, k1, k2):
            tmp = d[k1]
            d[k1] = d[k2]
            d[k2] = tmp
        
        swap(out_gates, 'ffj', 'z08')
        swap(out_gates, 'gjh', 'z22')
        swap(out_gates, 'jdr', 'z31')
        swap(out_gates, 'dwp', 'kfm')
        
        bad_gates = ['ffj','z08','gjh','z22','jdr','z31','dwp','kfm']


        gates = [(stmt, out) for out, stmt in out_gates.items()]
        test_inputs = {x_key: 1 for x_key in x_keys}
        test_inputs.update({y_key: 0 for y_key in y_keys})
        values = evaluate(test_inputs, gates)
        print({k: v for k,v in values.items() if k in z_keys})

        gates = [(stmt, out) for out, stmt in out_gates.items()]
        test_inputs = {x_key: 0 for x_key in x_keys}
        test_inputs.update({y_key: 1 for y_key in y_keys})
        values = evaluate(test_inputs, gates)
        print({k: v for k,v in values.items() if k in z_keys})

        gates = [(stmt, out) for out, stmt in out_gates.items()]
        test_inputs = {x_key: 1 for x_key in x_keys}
        test_inputs.update({y_key: 1 for y_key in y_keys})
        values = evaluate(test_inputs, gates)
        print({k: v for k,v in values.items() if k in z_keys})

        print(",".join(sorted(bad_gates)))

    # print(tot2)

## Couldn't figure out how to do part 2 automatically, so I ended up just doing it by hand
## Maybe you could write out the formula for the adder and then figure out a best assignment or something
## Basically figured that the result going into Z had to be an xor, so make a list of all z's that don't take an xor
## and then inspect those by hand
## Fortunately, the gate swaps were only between gates affecting the same digit
## Could have been way more confusing otherwise