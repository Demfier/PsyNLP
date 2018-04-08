"""
Contains class to represent a Finite State Transducer.

For theory, refer:

> "Learning Transducers"
    - http://pagesperso.lina.univ-nantes.fr/~cdlh//book/Learning_transducers.pdf
"""

import networkx as nx


class FST(nx.DiGraph):
    def add_state(self, newest_state=None):
        """
        Adds a new state, depending on the max added state and returns that state id
        """

        if newest_state is None:
          newest_state = self.new_state()
        self.add_node(newest_state, type='state')
        return(newest_state)

    def new_state(self):
        """
        :return: Returns possible new state in Transducer network
        """

        states = self.states()

        if states:
            return max(states)+1
        else:
            return 1

    def states(self):
        """
        :return states: All states present in the Transducer
        """

        states = [node for (node, data) in self.nodes(data=True) if 'type' in data and data['type'] == 'state']
        return(states)

    def add_metadata(self, metadata):
        """
        Adds a metadata node, to connect to different states
        :param metadata: The metadata to be added
        """

        self.add_node(metadata, type='metadata')

    def metadatas(self):
        """
        :return metadatas: All metadata nodes present in the Transducer
        """

        metadatas = [node for (node, data) in self.nodes(data=True) if data['type'] == 'metadata']
        return(metadatas)

    def contextual_subgraph(self, metadatas=[]):
        """
        :param metadatas: A list of metadatas for context
        :return contextual_subgraph: Transducer network corresponding to given metadatas
        """

        contextual_states = set(self.states())
        contextual_states.add(0)
        contextual_states.add(-1)

        for metadata in metadatas:
            try:
                contextual_states = contextual_states.intersection(set(self[metadata]))
            except KeyError:
                contextual_states = contextual_states

        contextual_subgraph = self.subgraph(list(contextual_states))
        return(contextual_subgraph)

    def add_arc(self, from_state, input, output, to_state):
        """
        :param from_state: The input state of an arc
        :param input: An input character(s)
        :param output: An output character(s)
        :param to_state: The output state of an arc
        """

        self.add_edge(from_state, to_state, input=input, output=output)

    def arcs(self):
        """
        :return edges: A list of edges (arcs) that are present in the Transducer network
        """

        edges = []
        states = self.states() + [0, -1]
        for edge in self.edges:
          node_1, node_2 = edge
          if node_1 in states and node_2 in states:
            edges.append(edge)
        return(edges)
