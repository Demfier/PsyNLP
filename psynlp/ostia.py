"""
Contains implementation of the famous inference algorithm OSTIA.

For theory, refer:

> "Learning Subsequential Transducers for Pattern Recognition Interpretation
  Tasks", Jose Oncina, Pedro Garcia, and Enrique Vidal
    - https://pdfs.semanticscholar.org/9058/01c8e75daacb27d70ccc3c0b587411b6d213.pdf
"""

from fst import FST
from helper import is_prefixed_with, eliminate_prefix, eliminate_suffix, lcp, get_io_chunks


class OSTIA(object):
    """docstring for OSTIA"""


<< << << < HEAD

    def __init__(self, T):
        """
        Initializes an FST from the given input and output tapes, and implements OSTIA
        :param T: An input*output mapping
        """

        self.graph = self.form_digraph(T)
        tou = tou_dup = self
        exit_condition_1 = exit_condition_2 = False
        q = tou.first()
        while q < tou.last():
            q = tou.next(q)
            p = tou.first()
            while p < q and not exit_condition_1:
                tou_dup = tou
                tou = tou.merge(q, p)
                while not tou.subseq() and not exit_condition_2:
                    r, a, v, s, w, t = tou.find_subseq_violation()
                    if (v != w and a == '#') or (
                            s < q and not is_prefixed_with(v, w)):
                        continue

                    u = lcp([v, w])
                    tou = tou.push_back(eliminate_prefix(u, v), (r, a, v, s))
                    tou = tou.push_back(eliminate_prefix(u, w), (r, a, w, t))
                    tou = tou.merge(t, s)

                if tou.subseq():
                    continue

                tou = tou_dup
                p = tou.next(p)

            if not tou.subseq():
                tou = tou_dup

        return tou

    def states(self):
        """
        :return states: A list of all states
        """

        return list(self.graph.states())

    def state(self, index):
        """
        :return state: The index-th state
        """
        state = self.states()[index]
        return state

    def first(self):
        """
        :return first_element: First element in the OTST
        """
        return self.state(0)

    def last(self):
        """
        :return last_element: Last element in the OTST
        """
        return self.state(-1)

    def next(self, a):
        """
        :param T: An element in the OTST
        :return next_element: Next element to a, in the OTST
        """

        all_states = self.states()
        if a not in all_states:
            return self.next(a + 1)
        index_of_a = all_states.index(a)
        if index_of_a == len(all_states) - 1:
            next_element = a
        else:
            next_element = self.state(index_of_a + 1)
        return next_element

    def merge(self, a, b):
        """
        :param a: A state in the OTST
        :param b: Another state in the OTST
        :return merged_otst: OTST with states a & b merged
        """

        graph = self.graph

        for (from_state, _) in graph.in_edges(b):
            try:
                input = graph[from_state][b]['input']
                output = graph[from_state][b]['output']
                # print(input, output)
                graph.add_edge(from_state, a, input=input, output=output)
            except KeyError:
                graph.add_edge(from_state, a)

        for to_state in graph[b]:
            input = graph[b][to_state]['input']
            output = graph[b][to_state]['output']
            # print(input, output)
            graph.add_edge(a, to_state, input=input, output=output)

        graph.remove_node(b)
        self.graph = graph
        return self

    def subseq(self):
        """
        :return bool: True if tou is subsequent, else False
        """

        violation = self.find_subseq_violation()
        return(violation is None)

    def find_subseq_violation(self):
        """
        (r,a,v,s) and (r,a,w,t) are 2 edges of tou that violate subseq condition,
        with s<t

        :return (r, a, v, s, w, t): Tuple
        """

        graph = self.graph
        states = self.states()

        for state in states:
            neighbors = graph[state]
            for neighbor_1 in neighbors:
                for neighbor_2 in neighbors:
                    if neighbor_1 == neighbor_2:
                        continue
                    edge_1 = graph[state][neighbor_1]
                    edge_2 = graph[state][neighbor_2]
                    if edge_1['input'] == edge_2['input'] and edge_1['output'] == edge_2['output']:
                        return((state, edge_1['input'], edge_1['output'], neighbor_1, edge_2['output'], neighbor_2))

    def push_back(self, element, edge):
        """
        :param element: An element in the OTST
        :param edge: An edge in the OTST, as a tuple (r, a, v, s)
        :return tou: OTST with element pushed back from the edge
        """

        graph = self.graph
        input_state, input_text, output_text, output_state = edge

        graph[input_state][output_state]['output'] = eliminate_suffix(
            output_text, element)
        outgoing_states = graph[output_state]
        for state in outgoing_states:
            graph[output_state][state]['output'] = element + \
                graph[output_state][state]['output']

        self.graph = graph
        return self

    def form_digraph(self, T):
        """
        :param T: A set of all input/output pairs
        :return graph: A directed networkx graph
        """

        graph = FST()
        input_arcs = output_arcs = []

        for (input_word, metadatas, output_word) in T:
            io_chunks = get_io_chunks(input_word, output_word) + [('#', '#')]

            for (i, (input_chunk, output_chunk)) in enumerate(io_chunks):
                if i == 0:
                    to_state = graph.add_state()
                    input_arcs.append((input_chunk, output_chunk, to_state))
                elif i == len(io_chunks) - 1:
                    from_state = to_state
                    output_arcs.append((from_state, input_chunk, output_chunk))
                else:
                    from_state = to_state
                    to_state = graph.add_state()
                    for metadata in metadatas:
                        graph.add_edge(metadata, from_state)
                        graph.add_edge(metadata, to_state)
                    graph.add_arc(
                        from_state,
                        input_chunk,
                        output_chunk,
                        to_state)

        for (input_chunk, output_chunk, to_state) in input_arcs:
            graph.add_arc(0, input_chunk, output_chunk, to_state)

        for (from_state, input_chunk, output_chunk) in output_arcs:
            graph.add_arc(from_state, input_chunk, output_chunk, -1)

        print("Done forming the directed FST graph")
        return(graph)

    def word_from_path(self, graph, path):
        path_input_word = ''
        for i in range(0, len(path) - 1):
            edge = graph[path[i]][path[i + 1]]
            path_input_word += edge['input']
        return path_input_word
