"""
Contains helper functions used by different submodules
"""

import os
import re
import networkx as nx
import matplotlib.pyplot as plt


def align(lemma, form):
    alemma, aform = levenshtein(lemma, form)
    lspace = max(len(alemma) - len(alemma.lstrip('_')),
                 len(aform) - len(aform.lstrip('_')))
    tspace = max(len(alemma[::-1]) - len(alemma[::-1].lstrip('_')),
                 len(aform[::-1]) - len(aform[::-1].lstrip('_')))
    return alemma[0:lspace], alemma[lspace:len(alemma)-tspace], alemma[len(alemma)-tspace:], aform[0:lspace], aform[lspace:len(alemma)-tspace], aform[len(alemma)-tspace:]


def levenshtein(s, t, inscost=1.0, delcost=1.0, substcost=1.0):
    """Recursive implementation of Levenshtein, with alignments returned."""
    def lrec(spast, tpast, srem, trem, cost):
        if len(srem) == 0:
            return spast + len(trem) * '_', tpast + trem, '', '', cost + len(trem)
        if len(trem) == 0:
            return spast + srem, tpast + len(srem) * '_', '', '', cost + len(srem)

        addcost = 0
        if srem[0] != trem[0]:
            addcost = substcost

        return min((lrec(spast + srem[0], tpast + trem[0], srem[1:], trem[1:], cost + addcost),
                    lrec(spast + '_', tpast +
                         trem[0], srem, trem[1:], cost + inscost),
                    lrec(spast + srem[0], tpast + '_', srem[1:], trem, cost + delcost)),
                   key=lambda x: x[4])

    answer = lrec('', '', s, t, 0)
    return answer[0], answer[1]


def is_prefixed_with(string, prefix):
    """
    :param str: An input word / sub-word
    :param prefix: A prefix to check in the word / sub-word
    :return bool: True if prefix, else False
    """
    return string.find(prefix) == 0


def lcp(strings):
    """
    Computes longest common prefix of given set of strings, given on page 449
    :param strings: A set of strings
    :return prefix: The longest common prefix
    """

    prefix = os.path.commonprefix(list(strings))
    return prefix


def eliminate_suffix(v, w):
    """
    If v = uw (u=prefix, w=suffix),
    u = v w-1

    :param v: A (sub)word
    :param w: A suffix
    :return u: (sub)word with the suffix removed
    """

    u = v.rstrip(w)
    return(u)


def eliminate_prefix(v, u):
    """
    If v = uw (u=prefix, w=suffix),
    w = u-1 v

    :param u: A prefix to remove
    :param v: A (sub)word
    :return w: (sub)word with the prefix removed
    """

    w = v.lstrip(u)
    return(w)


# Iterative longest contiguous sequence. No one character matchings
def lcs(s1, s2):
    longest = ""
    i = 0
    for x in s1:
        if re.search(x, s2):
            s = x
            while re.search(s, s2):
                if len(s) > len(longest):
                    longest = s
                if i+len(s) == len(s1):
                    break
            s = s1[i:i+len(s)+1]
        i += 1
    return longest


def lcs(s1, s2):
    s1 = s1.replace('(', '').replace(')', '')
    s2 = s2.replace('(', '').replace(')', '')
    longest = ""
    i = 0
    for x in s1:
        if re.search(x, s2):
            s = x
            while re.search(s, s2):
                if len(s) > len(longest):
                    longest = s
                if i + len(s) == len(s1):
                    break
                s = s1[i:i + len(s) + 1]
        i += 1
    return longest


def visualize_graph(G, attr):
    if attr == 'uid':
        elarge = [
            (u,
             v) for (
                u,
                v,
                d) in G.edges(
                data=True) if len(
                d['uid']) > 2]
        esmall = [
            (u,
             v) for (
                u,
                v,
                d) in G.edges(
                data=True) if len(
                d['uid']) <= 2]
    else:
        elarge = [
            (u, v) for (
                u, v, d) in G.edges(
                data=True) if d['weight'] > 2]
        esmall = [
            (u, v) for (
                u, v, d) in G.edges(
                data=True) if d['weight'] <= 2]

    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=esmall,
        width=6,
        alpha=0.5,
        edge_color='b',
        style='dashed')
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    plt.axis('off')
    plt.savefig("weighted_graph.png")
    plt.show()


def visualize_network(G, attr):
    labels = list()
    for node in G:
        for neighbor in G[node]:
            labels.append(G[node][neighbor][attr])
    graph_pos = nx.spring_layout(G)
    edge_labels = dict(zip(G.edges, labels))
    nx.draw_networkx_nodes(
        G,
        graph_pos,
        node_size=1000,
        node_color='blue',
        alpha=0.3)
    nx.draw_networkx_edges(G, graph_pos, width=2, alpha=0.1, style='dashed')
    nx.draw_networkx_labels(
        G,
        graph_pos,
        font_size=15,
        font_family='sans-serif')
    nx.draw_networkx_edge_labels(
        G, graph_pos, edge_labels=edge_labels, font_size=8)
    plt.axis('off')
    plt.show()


def read_wordpairs(path):
    file = open(path, 'r')
    wordpairs = dict()
    for line in file.readlines():
        source, dest, metadata = line.split("\t")
        # metadata = metadata.replace("\n", "").split(";")
        # if "V" in metadata and "PRS" in metadata:
        wordpairs[source] = dest

        # if len(source) < 10 and len(dest) < 15:
    return(wordpairs)


def pretty_print_graph(G):
    print("\n")
    print("Number of nodes : ", len(G.nodes))
    print("Number of edges : ", len(G.edges))
