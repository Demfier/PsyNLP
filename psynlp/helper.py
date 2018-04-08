"""
Contains helper functions used by different submodules
"""

import os
import re


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
