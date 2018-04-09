import os
import re
import operator
import pandas as pd
import networkx as nx
from functools import wraps

from ..core import oracle
from ..core.fca import FCA


def pretty_print_graph(G):
    print("\n")
    print("Number of nodes : ", len(G.nodes))
    print("Number of edges : ", len(G.edges))


def deterministic_pac(concept):
    def generate_df(concept):
        rows = []
        for word in concept.attributes():
            operations = sorted(list(concept.objects_intent(set([word]))))
            rows.append({'source': word, 'operations': ','.join(operations)})

        df = pd.DataFrame(rows)
        return df

    def structure_df_to_pac(df):
        pac = []
        for (operations, sub_df) in sorted(df.groupby(['operations']), key=lambda x: len(list(x[1]['source'])), reverse=True):
            consequent_attrs = tuple(sorted(list(sub_df['source'])))
            antecedent_attrs = tuple([consequent_attrs[0]])
            pac.append((antecedent_attrs, consequent_attrs))

        return pac

    df = generate_df(concept)
    pac = structure_df_to_pac(df)
    return pac
