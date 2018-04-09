import pandas as pd


def pretty_verbose_print_graph(G):
    verbose_print_2("\n")
    verbose_print_2("Number of nodes : ", len(G.nodes))
    verbose_print_2("Number of edges : ", len(G.edges))


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
