import os
import tqdm
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
    
    hailstones = []
    for line in data:
        pos = [int(x) for x in line.split("@")[0].strip().split(", ")]
        vel = [int(x) for x in line.split("@")[1].strip().split(", ")]
        hailstones.append((pos, vel))

    pos_min = 7 if filename[0] == 't' else 200000000000000
    pos_max = 27 if filename[0] == 't' else 400000000000000

    for i in range(len(hailstones)):
        for j in range(i):
            pos, vel = hailstones[i]
            x, y, z = pos
            vx, vy, vz = vel
            pos2, vel2 = hailstones[j]
            x2, y2, z2 = pos2
            vx2, vy2, vz2 = vel2
            if vx * vy2 != vy * vx2:
                # x + vxa = x2 + vx2b
                # y + vya = y2 + vy2b
                # b = (y+vya-y2)/vy2
                a = ((x2-x) * vy2 + (y-y2) * vx2) / (vx*vy2 - vx2*vy)
                inter_x = x + vx * a
                inter_y = y + vy * a
                b = (x + vx * a - x2) / vx2
                if a > 0 and b > 0:
                    if inter_x >= pos_min and inter_x <= pos_max and inter_y >= pos_min and inter_y <= pos_max:
                        # print(pos, vel)
                        # print(pos2, vel2)
                        # print(inter_x, inter_y)
                        tot += 1

    
    

    # x + vxt = x2 + vx2t
    # y + vyt = y2 + vy2t
    # z + vzt = z2 + vz2t
    # (x-x2) / (vx2-vx) = (y-y2) / (vy2-vy) = (z-z2) / (vz2-vz) > 0
    # 6 free parameters and 2 constraints per hailstone
    #   only need 3 hailstones?
    # (x-x2) (vy2-vy) = (y-y2) (vx2-vx)
    
    # x2 = (y2-y) (vx2-vx) / (vy2-vy) - x
    # y2 = (x2-x) (vy2-vy) / (vx2-vx) - y
    

    print(tot)
    # try all possible t for first and second collision?
    # line up with rest of hailstones and see if it matches
    # issue: doesn't scale well
    pos1, vel1 = hailstones[0]
    pos2, vel2 = hailstones[1]
    pos3, vel3 = hailstones[2]
    # match = False
    # for t in range(1, 10):
    #     collision1 = [pos1[i] + vel1[i] * t for i in range(3)]
    #     for t2 in range(1, 10):
    #         if t2 == t:
    #             continue
    #         collision2 = [pos2[i] + vel2[i] * t2 for i in range(3)]
    #         integer_vel = True
    #         for i in range(3):
    #             if (collision2[i] - collision1[i]) % (t2-t) != 0:
    #                 integer_vel = False
    #                 break
    #         if not integer_vel:
    #             continue
    #         vel_collider = [(collision2[i] - collision1[i]) / (t2-t) for i in range(3)]
    #         pos_collider = [collision1[i] - vel_collider[i]*t for i in range(3)]

    #         t3 = [(pos3[i] - pos_collider[i]) / (vel_collider[i] - vel3[i]) if vel_collider[i] != vel3[i] else None for i in range(3)]
    #         t_common = None
    #         for x in t3:
    #             if x is not None:
    #                 t_common = x
    #         match = True
    #         for i in range(3):
    #             if t3[i] is None:
    #                 if pos3[i] != pos_collider[i]:
    #                     match = False
    #                     break
    #             else:
    #                 if t_common != t3[i]:
    #                     match = False
    #                     break
    #         if match:
    #             print(pos_collider, vel_collider)
    #             break
    #     if match:
    #         break

    # p + v * t1 = p1 + v1 * t1, p-p1 + (v-v1) * t1 = 0
    # p + v * t2 = p2 + v2 * t2
    #   v * (t1-t2) = p1 - p2 + v1 * t1 - v2 * t2
    # p + v * t3 = p3 + v3 * t3
    #   v * (t1-t3) = p1 - p3 + v1 * t1 - v3 * t3
    #   (p1 - p2 + v1 * t1 - v2 * t2) * (t1 - t3) = (p1 - p3 + v1 * t1 - v3 * t3) * (t1 - t2)
    #   p1 * (t2 - t3) - p2 * (t1 - t3) + p3 * (t1 - t2) + v1 * t1 * (t2 - t3) - v2 * t2 * (t1 - t3) + v3 * t3 * (t1 - t2) = 0
    # (p1 - p2 + v1 * t1 - v2 * t2) x (p1 - p3 + v1 * t1 - v3 * t3) = 0
    # (p1 - p2) x (p1 - p3) + p1 x (v1 * t1 - v2 * t2) + p1 x (v1 * t1 - v3 * t3) + (t1 * v1 - t2 * v2) x (t1 * v1 - t3 * v3)
    #   - p2 x (v1 * t1 - v3 * t3) - p3 x (v1 * t1 - v2 * t2) = 0
    # (p1 - p2) x (p1 - p3) * (v1 * t1 - v2 * t2) - p2 x (v1 * t1 - v3 * t3) * (v1 * t1 - v2 * t2) = 0
    # (p1 - p2) x (p1 - p3) * (v1 * t1 - v3 * t3) - p3 x (v1 * t1 - v2 * t2) * (v1 * t1 - v3 * t3) = 0
    # (v - v1) * (t1 - t2) = p1 - p2 + t2 * (v1 - v2)
    # (v - v1) * (t1 - t3) = p1 - p3 + t3 * (v1 - v3)
    # ((p1 - p2) + t2 * (v1-v2)) x ((p1 - p3) + t3 * (v1 - v3)) = (v - v1) x (v - v1) * C = 0
    # (p1 - p2) x (p1 - p3) - t2 * (p1-p3) x (v1 - v2) + t3 * (p1-p2) x (v1-v3) + t2 * t3 * (v1-v2) x (v1-v3)= 0
    #  [(p1-p2) x (p1-p3)] * (v1-v2) + t3 * [(p1-p2) x (v1-v3)] * (v1-v2) = 0
    #    t3 = -(p1 - p2) x (p1-p3)*(v1-v2) / [(p1 - p2) x (v1-v3) * (v1 - v2)]
    #  [(p1-p2) x (p1-p3)] * (v1-v3) - t2 * [(p1-p3) x (v1-v2)] * (v1-v3) = 0
    #    t2 = ...
    #    c3 = p3 + v3 * t3
    #    c2 = p2 + v2 * t2
    #    v = (c3-c2) / (t3 - t2)
    #    p = c3 - v * t3

    def cross(vec1, vec2):
        return [vec1[(i+1) % 3] * vec2[(i+2) % 3] - vec1[(i+2)%3] * vec2[(i+1)%3] for i in range(3)]
    def dot(vec1, vec2):
        return sum([vec1[i] * vec2[i] for i in range(3)])
    def sub(vec1, vec2):
        return [vec1[i]-vec2[i] for i in range(3)]
    def add(vec1, vec2):
        return [vec1[i] + vec2[i] for i in range(3)]
    def mul(vec, scalar):
        return [vec[i] * scalar for i in range(3)]
    def div(vec, scalar):
        return [vec[i] / scalar for i in range(3)]
    p1_p2 = sub(pos1, pos2)
    p1_p3 = sub(pos1, pos3)
    v1_v2 = sub(vel1, vel2)
    v1_v3 = sub(vel1, vel3)
    t3 = -dot(cross(p1_p2, p1_p3), v1_v2) / dot(cross(p1_p2, v1_v3), v1_v2)
    t2 = dot(cross(p1_p2, p1_p3), v1_v3) / dot(cross(p1_p3, v1_v2), v1_v3)
    print(t3)
    print(t2)
    c3 = add(pos3, mul(vel3, t3))
    c2 = add(pos2, mul(vel2, t2))
    v = div(sub(c3, c2), t3-t2)
    p = sub(c3, mul(v, t3))
    print(p, v)


    tot2 = sum(p)

    print(tot2)