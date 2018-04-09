import pandas as pd


def pretty_verbose_print_graph(G):
    """
    Method to pretty print a graph
    Parameters:
    -----------------------------------
    G : nx.Graph
        The networkx graph to be pretty-printed
    """
    verbose_print_2("\n")
    verbose_print_2("Number of nodes : ", len(G.nodes))
    verbose_print_2("Number of edges : ", len(G.edges))


def deterministic_pac(concept):
    """
    Groups attributes in a concept based on deterministic clustering.
    Parameters:
    -----------------------------------
    concept : object[FCA]

    Returns:
    -----------------------------------
    pac : list[tuple]
        Computed canonical-basis
    """
    def generate_df(concept):
        """
        Converts a given concept to a pandas dataframe
        Parameters:
        -----------------------------------
        concept : object[FCA]
            The concept to be converted into a pd dataframe

        Returns:
        -----------------------------------
        df : pd.DataFrame
            DF form of the given concept
        """
        rows = []
        for word in concept.attributes():
            operations = sorted(list(concept.objects_intent(set([word]))))
            rows.append({'source': word, 'operations': ','.join(operations)})

        df = pd.DataFrame(rows)
        return df

    def structure_df_to_pac(df):
        """
        Calculate canonical-basis from the given dataframe
        Parameters:
        -----------------------------------
        df : pd.DataFrame
            Input dataframe consisting of all the input-output pairs

        Returns:
        -----------------------------------
        pac : list[tuple]
            Computed canonical basis
        """
        pac = []
        for (operations, sub_df) in sorted(df.groupby(['operations']), key=lambda x: len(list(x[1]['source'])), reverse=True):
            consequent_attrs = tuple(sorted(list(sub_df['source'])))
            antecedent_attrs = tuple([consequent_attrs[0]])
            pac.append((antecedent_attrs, consequent_attrs))

        return pac

    df = generate_df(concept)
    pac = structure_df_to_pac(df)
    return pac
