import sys
import typing
import random
import copy


def input_read(input: str, blocks_dic: dict, post_dic: dict) -> None:
    with open(input) as f:
        lines = f.readlines()
        count = 0
        single_count = 1
        for line in lines:
            splitted = []
            splitted[:] = line

            for num in range(0, 4):
                number = int(splitted[num])
                if number == 7:
                    number += single_count
                    single_count += 1

                blocks_dic[count * 4 + num] = number
                if number not in post_dic.keys():
                    post_dic[number] = [count * 4 + num]
                else:
                    post_dic[number].append(count * 4 + num)

            if count >= 4:
                break
            count += 1


#
# class Block:
#     def __init__(self, num: int):
#         self.num = num
#         self.positions = [] #ordered
#
#     def add_pos(self, pos: tuple) -> None:
#         self.positions.append(pos)


def move_left(blocks_dic: dict, pos_dic1: dict, number: int) -> bool:
    for pos in pos_dic1[number]:
        if pos % 4 == 0 or not (blocks_dic[pos - 1] == 0 or blocks_dic[pos - 1] == blocks_dic[pos]):
            return False

    i = 0
    for pos in pos_dic1[number]:
        blocks_dic[pos - 1] = number
        blocks_dic[pos] = 0

        pos_dic1[number][i] = pos - 1
        pos_dic1[0].remove(pos - 1)
        pos_dic1[0].append(pos)
        i += 1

    return True


def move_right(blocks_dic: dict, pos_dic1: dict, number: int) -> bool:
    for pos in pos_dic1[number]:
        if pos % 4 == 3 or not (blocks_dic[pos + 1] == 0 or blocks_dic[pos + 1] == blocks_dic[pos]):
            return False

    for i in range(len(pos_dic1[number]) - 1, -1, -1):
        pos = pos_dic1[number][i]
        blocks_dic[pos + 1] = number
        blocks_dic[pos] = 0

        pos_dic1[number][i] = pos + 1
        pos_dic1[0].remove(pos + 1)
        pos_dic1[0].append(pos)

    return True


def move_up(blocks_dic: dict, pos_dic1: dict, number: int) -> bool:
    for pos in pos_dic1[number]:
        if pos // 4 == 0 or not (
                blocks_dic[pos - 4] == 0 or blocks_dic[pos - 4] == blocks_dic[pos]):
            return False

    i = 0
    for pos in pos_dic1[number]:
        blocks_dic[pos - 4] = number
        blocks_dic[pos] = 0

        pos_dic1[number][i] = pos - 4
        pos_dic1[0].remove(pos - 4)
        pos_dic1[0].append(pos)
        i += 1

    return True


def move_down(blocks_dic: dict, pos_dic1: dict, number: int) -> bool:
    for pos in pos_dic1[number]:
        if pos // 4 >= 4 or not (
                blocks_dic[pos + 4] == 0 or blocks_dic[pos + 4] == blocks_dic[pos]):
            return False

    for i in range(len(pos_dic1[number]) - 1, -1, -1):
        pos = pos_dic1[number][i]
        # print(pos)
        # print(pos+4)
        blocks_dic[pos + 4] = number
        blocks_dic[pos] = 0

        pos_dic1[number][i] = pos + 4
        pos_dic1[0].remove(pos + 4)
        pos_dic1[0].append(pos)

    return True


# class Node:
#     pos: dict
#     blocks: dict
#     neighbours: list
#
#     def __init__(self, blocks: dict, pos: dict):
#         self.pos = pos
#         self.blocks = blocks
#         self.neighbours = []
#
#
# def add_neighbours(self_node: Node,
#                    neighbour: Node) -> None:  # for some reason I couldn't do it inside the class
#     self_node.neighbours.append(neighbour)


def dfs(blocks_dic: dict, pos_dic: dict, count: int, rep: set,
        previous_states: list) -> bool:
    if pos_dic[1][0] == 13:
        # output_to_file(sys.argv[2], count, previous_states)

        return True

    around_zero_left = []  # blocks that are neighbours to a zero
    around_zero_top = []
    around_zero_right = []
    around_zero_bottom = []

    left_trials = set()  # 4
    top_trials = set()  # 3
    right_trials = set()  # 1
    bottom_trials = set()  # 2

    for pos in pos_dic[0]:
        if pos % 4 != 0 and blocks_dic[pos - 1] != 0 and blocks_dic[
            pos - 1] not in around_zero_left:
            around_zero_left.append(blocks_dic[pos - 1])
        if pos % 4 != 3 and blocks_dic[pos + 1] != 0 and blocks_dic[
            pos + 1] not in around_zero_right:
            around_zero_right.append(blocks_dic[pos + 1])
        if pos // 4 != 0 and blocks_dic[pos - 4] != 0 and blocks_dic[
            pos - 4] not in around_zero_top:
            around_zero_top.append(blocks_dic[pos - 4])
        if pos // 4 < 4 and blocks_dic[pos + 4] != 0 and blocks_dic[
            pos + 4] not in around_zero_bottom:
            around_zero_bottom.append(blocks_dic[pos + 4])

    i_total = len(around_zero_top) + len(around_zero_left) + len(around_zero_bottom) + len(
        around_zero_right)

    blocks_cpy = blocks_dic.copy()
    pos_cpy = copy.deepcopy(pos_dic)

    for f in range(0, i_total):

        for element in rep:
            if element[0] == 4:
                right_trials.add(element)
            elif element[0] == 3:
                bottom_trials.add(element)
            elif element[0] == 2:
                top_trials.add(element)
            else:
                left_trials.add(element)

        l_d = len(around_zero_left) - len(left_trials)
        r_d = len(around_zero_right) - len(right_trials)
        t_d = len(around_zero_top) - len(top_trials)
        b_d = len(around_zero_bottom) - len(bottom_trials)

        if b_d > 0:  # search moving top
            if (move_up(blocks_cpy, pos_cpy, around_zero_bottom[b_d - 1])):
                if not any(write_output(blocks_cpy, pos_cpy) in write_output(state[0], state[1])
                           for state in previous_states):

                    previous_states.append((blocks_cpy.copy(), copy.deepcopy(pos_cpy)))
                    count += 1
                    rep = set()
                    if not dfs(blocks_cpy, pos_cpy, count, rep, previous_states):
                        rep.add((3, b_d - 1))
                    else:
                        return True
                rep.add((3, b_d - 1))
            else:
                blocks_cpy = blocks_dic
                pos_cpy = pos_dic
                rep.add((3, b_d - 1))

        elif t_d > 0:  # search moving bottom
            if (move_down(blocks_cpy, pos_cpy,
                          around_zero_top[t_d - 1])):
                if not any(write_output(blocks_cpy, pos_cpy) in write_output(state[0], state[1])
                           for state in previous_states):

                    previous_states.append((blocks_cpy.copy(), copy.deepcopy(pos_cpy)))
                    count += 1
                    rep = set()
                    if not dfs(blocks_cpy, pos_cpy, count, rep, previous_states):
                        rep.add((2, t_d - 1))
                    else:
                        return True
                else:
                    blocks_cpy = blocks_dic
                    pos_cpy = pos_dic
                    rep.add((2, t_d - 1))
            else:
                rep.add((2, t_d - 1))

        elif l_d > 0:  # search moving right
            if move_right(blocks_cpy, pos_cpy, around_zero_left[l_d - 1]):
                if not any(write_output(blocks_cpy, pos_cpy) in write_output(state[0], state[1])
                           for state in previous_states):

                    previous_states.append((blocks_cpy.copy(), copy.deepcopy(pos_cpy)))
                    count += 1
                    rep = set()
                    if not dfs(blocks_cpy, pos_cpy, count, rep, previous_states):
                        rep.add((1, l_d - 1))
                    else:
                        return True
                else:
                    blocks_cpy = blocks_dic
                    pos_cpy = pos_dic
                    rep.add((1, l_d - 1))
            else:
                rep.add((1, l_d - 1))
        elif r_d > 0: #search moving left
            if move_left(blocks_cpy, pos_cpy, around_zero_right[r_d - 1]):
                if not any(write_output(blocks_cpy, pos_cpy) in write_output(state[0], state[1])
                           for state in previous_states):

                    previous_states.append((blocks_cpy.copy(), copy.deepcopy(pos_cpy)))
                    count += 1
                    rep = set()
                    if not dfs(blocks_cpy, pos_cpy, count, rep, previous_states):
                        rep.add((4, r_d - 1))
                    else:
                        return True
                else:
                    blocks_cpy = blocks_dic
                    pos_cpy = pos_dic
                    rep.add((4, r_d - 1))
            else:
                rep.add((4, r_d - 1))
        # print(count)
        # print(pos_dic[1][0])

    output_to_file(sys.argv[2], count, previous_states)
    return False


def a_original(blocks_dic: dict, pos_dic: dict, count: int, rep: set,
               previous_states: list) -> bool:
    if pos_dic[1][0] == 13:
        # output_to_file(sys.argv[2], count, previous_states)

        return True

    around_zero_left = []  # blocks that are neighbours to a zero
    around_zero_top = []
    around_zero_right = []
    around_zero_bottom = []

    left_trials = set()  # 4
    top_trials = set()  # 3
    right_trials = set()  # 1
    bottom_trials = set()  # 2

    for pos in pos_dic[0]:
        if pos % 4 != 0 and blocks_dic[pos - 1] != 0 and blocks_dic[
            pos - 1] not in around_zero_left:
            around_zero_left.append(blocks_dic[pos - 1])
        if pos % 4 != 3 and blocks_dic[pos + 1] != 0 and blocks_dic[
            pos + 1] not in around_zero_right:
            around_zero_right.append(blocks_dic[pos + 1])
        if pos // 4 != 0 and blocks_dic[pos - 4] != 0 and blocks_dic[
            pos - 4] not in around_zero_top:
            around_zero_top.append(blocks_dic[pos - 4])
        if pos // 4 < 4 and blocks_dic[pos + 4] != 0 and blocks_dic[
            pos + 4] not in around_zero_bottom:
            around_zero_bottom.append(blocks_dic[pos + 4])

    i_total = len(around_zero_top) + len(around_zero_left) + len(around_zero_bottom) + len(
        around_zero_right)

    blocks_cpy = blocks_dic.copy()
    pos_cpy = copy.deepcopy(pos_dic)

    for f in range(0, i_total):

        for element in rep:
            if element[0] == 4:
                right_trials.add(element)
            elif element[0] == 3:
                bottom_trials.add(element)
            elif element[0] == 2:
                top_trials.add(element)
            else:
                left_trials.add(element)

        l_d = len(around_zero_left) - len(left_trials)
        r_d = len(around_zero_right) - len(right_trials)
        t_d = len(around_zero_top) - len(top_trials)
        b_d = len(around_zero_bottom) - len(bottom_trials)

        if b_d > 0:  # search moving top
            if move_up(blocks_cpy, pos_cpy, around_zero_bottom[b_d - 1]) and \
                    (distance_btw_sol(pos_cpy[1][0]) <= distance_btw_sol(pos_dic[1][0])):
                if not any(write_output(blocks_cpy, pos_cpy) in write_output(state[0], state[1])
                           for state in previous_states):

                    previous_states.append((blocks_cpy.copy(), copy.deepcopy(pos_cpy)))
                    count += 1
                    rep = set()
                    if not a_original(blocks_cpy, pos_cpy, count, rep, previous_states):
                        rep.add((3, b_d - 1))
                    else:
                        return True
                rep.add((3, b_d - 1))
            else:
                blocks_cpy = blocks_dic
                pos_cpy = pos_dic
                rep.add((3, b_d - 1))

        elif t_d > 0:  # search moving bottom
            if (move_down(blocks_cpy, pos_cpy,
                          around_zero_top[t_d - 1])) and \
                    (distance_btw_sol(pos_cpy[1][0]) <= distance_btw_sol(pos_dic[1][0])):
                if not any(write_output(blocks_cpy, pos_cpy) in write_output(state[0], state[1])
                           for state in previous_states):

                    previous_states.append((blocks_cpy.copy(), copy.deepcopy(pos_cpy)))
                    count += 1
                    rep = set()
                    if not a_original(blocks_cpy, pos_cpy, count, rep, previous_states):
                        rep.add((2, t_d - 1))
                    else:
                        return True
                else:
                    blocks_cpy = blocks_dic
                    pos_cpy = pos_dic
                    rep.add((2, t_d - 1))
            else:
                rep.add((2, t_d - 1))

        elif l_d > 0:  # search moving right
            if move_right(blocks_cpy, pos_cpy, around_zero_left[l_d - 1]) and \
                    (distance_btw_sol(pos_cpy[1][0]) <= distance_btw_sol(pos_dic[1][0])):
                if not any(write_output(blocks_cpy, pos_cpy) in write_output(state[0], state[1])
                           for state in previous_states):

                    previous_states.append((blocks_cpy.copy(), copy.deepcopy(pos_cpy)))
                    count += 1
                    rep = set()
                    if not a_original(blocks_cpy, pos_cpy, count, rep, previous_states):
                        rep.add((1, l_d - 1))
                    else:
                        return True
                else:
                    blocks_cpy = blocks_dic
                    pos_cpy = pos_dic
                    rep.add((1, l_d - 1))
            else:
                rep.add((1, l_d - 1))
        elif r_d > 0:  # search moving left
            if move_left(blocks_cpy, pos_cpy, around_zero_right[r_d - 1]) and \
                    (distance_btw_sol(pos_cpy[1][0]) <= distance_btw_sol(pos_dic[1][0])):
                if not any(write_output(blocks_cpy, pos_cpy) in write_output(state[0], state[1])
                           for state in previous_states):

                    previous_states.append((blocks_cpy.copy(), copy.deepcopy(pos_cpy)))
                    count += 1
                    rep = set()
                    if not a_original(blocks_cpy, pos_cpy, count, rep, previous_states):
                        rep.add((4, r_d - 1))
                    else:
                        return True
                else:
                    blocks_cpy = blocks_dic
                    pos_cpy = pos_dic
                    rep.add((4, r_d - 1))
            else:
                rep.add((4, r_d - 1))
        # print(count)
        # print(pos_dic[1][0])

    output_to_file(sys.argv[2], count, previous_states)
    return False


def write_output(blocks_dic: dict, pos_dic: dict) -> str:
    output = ''
    for i in range(0, 5):
        for j in range(0, 4):
            num = blocks_dic[j + i * 4]
            if num >= 7:
                num = 4
            elif num in range(2, 7):
                if pos_dic[num][0] == pos_dic[num][1] + 1 or pos_dic[num][0] == pos_dic[num][1] - 1:
                    num = 2
                else:
                    num = 3

            output += str(num)
    return output


def distance_btw_sol(i: int) -> int:
    return abs(3 - i // 4) + abs(i % 4)


def output_to_file(filename: str, count, states_list: list) -> None:
    main_out = sys.stdout
    f = open(filename, 'w')
    sys.stdout = f
    print("Cost of the solution:" + str(count))

    for state in states_list:
        output = write_output(state[0], state[1])
        for s in range(0, 6):
            print(output[s * 4:(s + 1) * 4])
        print('')

    sys.stdout = main_out
    f.close()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("length of sysargv should be 4")
        exit(1)
    input = sys.argv[1]

    #input = "input3.txt"

    blocks_dic = {}  # position to blocks
    pos_dic = {}  # blocks to poistions
    input_read(input, blocks_dic, pos_dic)

    previous_states = []
    previous_states.append((blocks_dic.copy(), copy.deepcopy(pos_dic)))
    dfs(blocks_dic, pos_dic, 0, set(), previous_states)
    a_original(blocks_dic, pos_dic, 0, set(), previous_states)

    #print("finished")
