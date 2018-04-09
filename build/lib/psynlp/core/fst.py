"""
Contains class to represent a Finite State Transducer.

For theory, refer:

> "Learning Transducers"
    - http://pagesperso.lina.univ-nantes.fr/~cdlh//book/Learning_transducers.pdf
"""

import networkx as nx


class FST(nx.DiGraph):
    """
    An FST has two important properties attached to it,

    - State, to represent a node
    - Edges, that contain the input-output transitions
    """
    def add_state(self, newest_state=None):
        """
        Adds a new state, depending on the max added state.
        Parameters:
        -----------------------------------
        newest_state : int
            Id of the state to be added to the Transducer

        Returns:
        -----------------------------------
        newest_state : int
            Id of the newest state
        """
        if newest_state is None:
            newest_state = self.new_state()
        self.add_node(newest_state, type='state')
        return(newest_state)

    def new_state(self):
        """
        Returns possible new state in Transducer network
        """
        states = self.states()
        if states:
            return max(states) + 1
        else:
            return 1

    def states(self):
        """
        Gives all the states states present in the Transducer.
        Returns:
        -----------------------------------
        states : list[int]
            Arrary of state-ids in the transducer
        """

        states = [node for (node, data) in self.nodes(
            data=True) if 'type' in data and data['type'] == 'state']
        return(states)

    def add_metadata(self, metadata):
        """
        Adds a metadata node that would connect to different states.
        Parameters:
        -----------------------------------
        metadata : str
            The metadata to add to the transducer
        """
        self.add_node(metadata, type='metadata')

    def metadatas(self):
        """
        Returns all metadata nodes present in the Transducer
        """
        metadatas = [node for (node, data) in self.nodes(
            data=True) if 'type' in data and data['type'] == 'metadata']
        return(metadatas)

    def contextual_subgraph(self, metadatas=[]):
        """
        Gives a contextual subgraph based on the given metadata
        Parameters:
        -----------------------------------
        metadatas : list[str]
            A list of metadatas for context
        Returns:
        -----------------------------------
        contextual_subgraph : nx.Graph
            Transducer network corresponding to given metadatas
        """

        contextual_states = set(self.states())
        for metadata in metadatas:
            try:
                contextual_states = contextual_states.intersection(set(self[metadata]))
            except KeyError:
                contextual_states = contextual_states

        contextual_subgraph = self.subgraph(list(contextual_states))
        return(contextual_subgraph)

    def add_arc(self, from_state, input, output, to_state):
        """
        Adds an arc in the transducer contains input-output transitions
        Parameters:
        -----------------------------------
        from_state : int
            The input state of an arc
        input: str
            An input character(s)
        output : str
            An output character(s)
        to_state: int
            The output state of an arc
        """
        self.add_edge(from_state, to_state, input=input, output=output)

    def arcs(self):
        """
        Gives all the edges present the transducer
        Returns:
        -----------------------------------
        edges : list
            A list of edges (arcs) that are present in the Transducer network
        """
        edges = []
        states = self.states()
        for edge in self.edges:
            node_1, node_2 = edge
            if node_1 in states and node_2 in states:
                edges.append(edge)
        return edges
