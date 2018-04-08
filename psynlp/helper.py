"""
Contains helper functions used by different submodules
"""

import os
import re
import time
import operator
import networkx as nx
import matplotlib.pyplot as plt
from ..psynlp.fca import FCA
from ..psynlp.inflection_deterministic import deterministic_pac



def align(lemma, form):
    alemma, aform, _ = levenshtein(lemma, form)
    lspace = max(len(alemma) - len(alemma.lstrip('_')),
                 len(aform) - len(aform.lstrip('_')))
    tspace = max(len(alemma[::-1]) - len(alemma[::-1].lstrip('_')),
                 len(aform[::-1]) - len(aform[::-1].lstrip('_')))
    return alemma[0:lspace], alemma[lspace:len(alemma) - tspace], alemma[len(
        alemma) - tspace:], aform[0:lspace], aform[lspace:len(alemma) - tspace], aform[len(alemma) - tspace:]


def levenshtein(s, t, inscost=1.0, delcost=1.0, substcost=1.0):
    """Recursive implementation of Levenshtein, with alignments returned."""
    def lrec(spast, tpast, srem, trem, cost):
        if len(srem) == 0:
            return spast + len(trem) * '_', tpast + \
                trem, '', '', cost + len(trem)
        if len(trem) == 0:
            return spast + srem, tpast + \
                len(srem) * '_', '', '', cost + len(srem)

        addcost = 0
        if srem[0] != trem[0]:
            addcost = substcost

        return min((lrec(spast + srem[0], tpast + trem[0], srem[1:], trem[1:], cost + addcost),
                    lrec(spast + '_', tpast +
                         trem[0], srem, trem[1:], cost + inscost),
                    lrec(spast + srem[0], tpast + '_', srem[1:], trem, cost + delcost)),
                   key=lambda x: x[4])

    answer = lrec('', '', s, t, 0)
    return answer[0], answer[1], answer[4]


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


def fetch_testing_data(language='english'):
    filepath = "psynlp/data/{}-dev".format(language)
    T = []
    file = open(filepath, 'r')
    for line in file.readlines():
        source, expected_dest, metadata = line.split("\t")
        if "*" not in source and "*" not in expected_dest:
            metadata = metadata.strip("\n")
            T.append((source, metadata, expected_dest))
    print("Providing all test words in structured manner")
    T = sorted(T, key=operator.itemgetter(0))
    return T


def parse_metadata_words(language='english', quality='low'):
    metadata_words = {}
    filepath = "psynlp/data/{}-train-{}".format(language, quality)
    file = open(filepath, 'r')
    for line in file.readlines():
        source, dest, metadata = line.split("\t")
        if "*" not in source and "*" not in dest:
            metadata = metadata.strip()
            if metadata in metadata_words:
                metadata_words[metadata].append((source, dest))
            else:
                metadata_words[metadata] = []
    return metadata_words


def parse_metadata_fca(metadata_words, type='pac'):
    metadata_fca = {}
    for metadata in metadata_words:
        wordpairs = metadata_words[metadata]
        concept = init_concept_from_wordpairs(wordpairs)
        if len(concept.objects()) > 0:
            start1 = time.clock()
            if type == 'deterministic':
                pac = deterministic_pac(concept)
            else:
                pac = concept.pac_basis(concept.is_member, 0.1, 0.1)
            end1 = time.clock() - start1
        else:
            pac, end1 = None, None
        metadata_fca[metadata] = (concept, pac, end1)
    return(metadata_fca)


def pretty_print_graph(G):
    print("\n")
    print("Number of nodes : ", len(G.nodes))
    print("Number of edges : ", len(G.edges))


def inflect(word, operations):
    for operation in sorted(operations):
        method, chunk = operation.split('_')
        if method == 'delete':
            word = word.rstrip(chunk)
        else:
            word = word + chunk
    return word


def fetch_input_output_pairs(language='english', quality='low'):
    filepath = "psynlp/data/{}-train-{}".format(language, quality)
    T = list()
    file = open(filepath, 'r')
    for line in file.readlines():
        source, dest, metadata = line.split("\t")
    if "*" not in source and "*" not in dest:
        metadata = metadata.strip("\n").split(";")
        T.append((source, metadata, dest))
    print("Providing all words in structured manner, to OSTIA")
    T = sorted(T, key=operator.itemgetter(0))
    return T


def get_io_chunks(s1, s2):
    chunks = []
    while len(s1) != 0 or len(s2) != 0:
        if len(s1) != 0 and len(s2) != 0:
            l = lcs(s1, s2)
            print(s1, s2, l)
            if s1.find(l) == 0 and l:
                # chunks.append((l, l))
                for c in list(l):
                    chunks.append((c, c))
                s1 = s1[len(l):]
                s2 = s2[len(l):]
            elif l:
                if s2.find(l) == 0:
                    chunks.append((s1[0], ''))
                    s1 = s1[1:]
                else:
                    for c in list(s2[:s2.find(l)]):
                        chunks.append(('', c))
                    # chunks.append(('', l))
                    s2 = s2[s2.find(l):]
            else:
                for c in list(s1):
                    chunks.append((c, ''))
                # chunks.append((s1, ''))
                s1 = ''
        elif len(s1) != 0:
            for c in list(s1):
                chunks.append((c, ''))
            # chunks.append((s1, ''))
            s1 = ''
        else:
            for c in list(s2):
                chunks.append(('', c))
            # chunks.append(('', s2))
            s2 = ''
    return chunks


def init_concept_from_wordpairs(wordpairs):
    concept = FCA()
    for (source, target) in wordpairs:
        if "*" not in source and "*" not in target:
            mutations = iterLCS({'source': source, 'target': target})
            for addition in mutations['added']:
                concept.add_relation("insert_" + addition, source)
            for deletion in mutations['deleted']:
                concept.add_relation("delete_" + deletion, source)
    return concept


def iterLCS(pdf):
    sw1 = pdf['source']
    sw2 = pdf['target']
    longList = []
    while True:
        tempVal = lcs(sw1, sw2)
        if len(tempVal) <= 1:
            break

    longList.append(tempVal)
    sw1 = sw1.replace(tempVal, '#', 1)
    sw2 = sw2.replace(tempVal, '!', 1)
    pdf['common'] = longList
    pdf['deleted'] = [item for item in sw1.split('#') if len(item) > 0]
    pdf['added'] = [item for item in sw2.split('!') if len(item) > 0]
    return pdf
