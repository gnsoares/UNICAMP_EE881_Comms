import numpy as np

from collections import deque
from numpy.typing import ArrayLike


class Vertex:
    def __init__(self, state_index: int, b_arr: tuple):
        self.state = (state_index, b_arr)
        self.adjacent = {}
        self.weight = 0

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'(i = {self.state[0]},' \
               f' b = {",".join(map(str,self.state[1]))},' \
               f' w = {self.weight})'

    def add_neighbor(self, neighbor: 'Vertex'):
        my_state = self.state[1]
        next_state = neighbor.state[1]
        self.adjacent[neighbor] = [
            my_state[1]*my_state[2]*next_state[-1],
            my_state[2]*my_state[3]*next_state[-1],
            my_state[1]*my_state[3]*next_state[-1],
            my_state[1]*next_state[-1],
            my_state[2]*next_state[-1],
            my_state[3]*next_state[-1],
        ]

    def remove_neighbor(self, neighbor: 'Vertex'):
        del self.adjacent[neighbor]

    def get_connections(self):
        return self.adjacent.keys()

    def get_symbols(self, neighbor: 'Vertex') -> tuple:
        return self.adjacent[neighbor]


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(sorted(self.vert_dict.values(), key=lambda x: x.state[0]))

    def __repr__(self):
        return '\n'.join(
            f'{v} -> {list(v.get_connections())}' for v in self
        )

    def add_vertex(self, state_index: int, b_arr: tuple):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(state_index, b_arr)
        self.vert_dict[(state_index, b_arr)] = new_vertex
        return new_vertex

    def remove_vertex(self, state_index: int, b_arr: tuple) -> None:
        if (state_index, b_arr) not in self.vert_dict:
            return
        self.num_vertices = self.num_vertices - 1
        del self.vert_dict[(state_index, b_arr)]

    def get_by_state_index(self, state_index: int) -> Vertex:
        return [
            self.vert_dict[key]
            for key in self.vert_dict.keys()
            if key[0] == state_index
        ]

    def get_vertex(self, n) -> Vertex:
        return self.vert_dict.get(n)

    def get_vertices_that_reach(self, dest: Vertex, states: list) -> Vertex:
        state_index = dest.state[0] - 1
        result = []
        for state_prev in states:
            from_ = self.get_vertex((state_index, state_prev))
            if from_ is not None and dest in from_.get_connections():
                result.append(from_)
        return result

    def add_edge(self, frm: Vertex, to: Vertex):
        if frm.state not in self.vert_dict or to.state not in self.vert_dict:
            return
        frm.add_neighbor(to)

    def remove_edge(self, frm: Vertex, to: Vertex) -> None:
        if frm.state not in self.vert_dict or to.state not in self.vert_dict:
            return
        frm.remove_neighbor(to)

    def get_vertices(self):
        return self.vert_dict.keys()

    def find_shortest_path(self, start: Vertex, end: Vertex):
        dist = {start: [start]}
        q = deque([start])
        while len(q):
            at = q.popleft()
            for next in map(lambda x: self.vert_dict[x.state],
                            at.get_connections()):
                if next not in dist:
                    dist[next] = [*dist[at], next]
                    q.append(next)
        return dist.get(end)

    def find_all_paths(self, start: Vertex, end: Vertex, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start.state not in self.vert_dict:
            return []
        paths = []
        for next in map(lambda x: self.vert_dict[x.state],
                        start.get_connections()):
            if next not in path:
                newpaths = self.find_all_paths(next, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths


def dot_product(x: list, y: list) -> float:
    return sum(i*j for i, j in zip(x, y))


def viterbi(code: ArrayLike) -> str:

    DUMMY = 6

    # evaluate code and message size
    code = np.append([1]*6*DUMMY, code)
    code = np.append(code, [1]*6*3*DUMMY)
    code_len = code.size
    if code_len % 6 != 0:
        print(f'Code size invalid: {code_len}')
        return
    message_len = code_len//6

    # initialize viterbi graph
    g = Graph()

    # create all possible states
    states = [
        (b1, b2, b3, b4)
        for b1 in [1, -1]
        for b2 in [1, -1]
        for b3 in [1, -1]
        for b4 in [1, -1]
        for b5 in [1, -1]
        for b6 in [1, -1]
    ]

    # create the graph vertices starting and ending at the default state
    for i in range(min(message_len, 6)):
        if message_len % 2 == 0 and i == message_len // 2:
            for state in states[:2**i]:
                g.add_vertex(i, state)
            break
        if message_len % 2 != 0 and i > message_len // 2:
            break
        for state in states[:2**i]:
            g.add_vertex(i, state)
            g.add_vertex(message_len - i, state[::-1])

    # create the intermediate vertices if needed
    if message_len >= 12:
        for i in range(6, message_len - 5):
            for state in states:
                g.add_vertex(i, state)

    # add edges between vertices
    for i in range(message_len):
        for state in states:
            curr = g.get_vertex((i, state))
            if curr is None:
                continue
            next_plus = g.get_vertex((i + 1, (*state[1:], 1)))
            if next_plus is not None:
                g.add_edge(curr, next_plus)
            next_minus = g.get_vertex((i + 1, (*state[1:], -1)))
            if next_minus is not None:
                g.add_edge(curr, next_minus)

    # execute the viterbi's algorithm
    for i in range(message_len):
        for dest in g.get_by_state_index(i + 1):

            # get all vertices that reach current
            from_list = g.get_vertices_that_reach(dest, states)

            # observations of current
            yi = code[6*i:6*(i+1)]

            # weight of every transition
            weights = {
                from_: from_.weight + dot_product(from_.get_symbols(dest), yi)
                for from_ in from_list
            }

            # get vertex w/ biggest weight
            from_biggest = max(weights, key=lambda x: weights[x])

            # update current weight and point backwards
            dest.weight = weights[from_biggest]
            dest.from_biggest = from_biggest

    # run the graph backwards to find optimal path
    dest = g.get_vertex((message_len, states[0]))
    path = [dest]
    for _ in range(message_len):
        path.append(dest.from_biggest)
        dest = dest.from_biggest
    path = path[::-1]

    # get bits corresponding to chosen path
    bits = ''.join([
        f'{.5*(vertex.state[1][-1] + 1):.0f}'
        for vertex in path[DUMMY+1:-3*DUMMY]
    ])

    # return decoded
    return path, bits


if __name__ == '__main__':
    import random
    bits = viterbi(np.array([random.randint(-1, 1) for _ in range(28)]))
    print(bits)
