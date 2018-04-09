import os
import re
from functools import wraps


def align(lemma, form):
    """
    Aligns the lemma and form to identify the prefix, root and suffix for
    each of them.
    ParameParameters:
Parameters:
emminga str
     form : str
       words tstr
        o be aligned
    """
    alemma, aform, _ = levenshtein(lemma, form)
    lspace = max(len(alemma) - len(alemma.lstrip('_')),
                 len(aform) - len(aform.lstrip('_')))
    tspace = max(len(alemma[::-1]) - len(alemma[::-1].lstrip('_')),
                 len(aform[::-1]) - len(aform[::-1].lstrip('_')))

    lp = alemma[0:lspace].replace('_', '')
    lr = alemma[lspace:len(alemma) - tspace].replace('_', '')
    ls = alemma[len(alemma) - tspace:].replace('_', '')
    rp = aform[0:lspace].replace('_', '')
    rr = aform[lspace:len(alemma) - tspace].replace('_', '')
    rs = aform[len(alemma) - tspace:].replace('_', '')

    return((lp, lr, ls, rp, rr, rs))


def levenshtein(s, t, inscost=1.0, delcost=1.0, substcost=1.0):
    """
    Recursive implementation of Levenshtein, with alignments returned.
    """
    @memolrec
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
                    lrec(spast + '_', tpast + trem[0], srem, trem[1:], cost + inscost),
                    lrec(spast + srem[0], tpast + '_', srem[1:], trem, cost + delcost)),
                   key=lambda x: x[4])

    answer = lrec('', '', s, t, 0)
    return answer[0], answer[1], answer[4]


def memolrec(func):
    """
    Memoizer for Levenshtein. Make the algo run significantly faster
    """
    cache = {}

    @wraps(func)
    def wrap(sp, tp, sr, tr, cost):
        if (sr, tr) not in cache:
            res = func(sp, tp, sr, tr, cost)
            cache[(sr, tr)] = (res[0][len(sp):], res[1][len(tp):], res[4] - cost)
        return sp + cache[(sr, tr)][0], tp + cache[(sr, tr)][1], '', '', cost + cache[(sr, tr)][2]
    return wrap


def is_prefixed_with(string, prefix):
    """
    Checks if the given string is prefixed with prefix
    Parameters:
    -----------------------------------
    string: str
        An input word / sub-word
    prefix: str
        A prefix to check in the word / sub-word

    Returns:
    -----------------------------------
    bool : True if prefix, else False
    """
    return string.find(prefix) == 0


def lcp(strings):
    """
    Computes longest common prefix of given set of strings
    Parameters:
    -----------------------------------
    strings : set
        A set of strings

    Returns:
    -----------------------------------
    prefix : str
        The longest common prefix
    """

    prefix = os.path.commonprefix(list(strings))
    return prefix


def eliminate_suffix(v, w):
    """
    Removes suffix w from the input word v

    If v = uw (u=prefix, w=suffix),
    u = v w-1
    Parameters:
    -----------------------------------
    v: str
        A (sub)word
    w: str
        The suffix to remove

    Returns:
    -----------------------------------
    u: str
        (sub)word with the suffix removed
    """

    u = v.rstrip(w)
    return(u)


def eliminate_prefix(v, u):
    """
    Removes prefix b from the given input word v
    If v = uw (u=prefix, w=suffix),
    w = u-1 v
    Parameters:
    -----------------------------------
    v: str
        A (sub)word
    u: str
        The prefix to remove

    Returns:
    -----------------------------------
    w : str
        (sub)word with the prefix removed
    """

    w = v.lstrip(u)
    return(w)


def lcs(s1, s2):
    """
    Returns Iterative longest contiguous sequence. No one character matchings
    Parameters:
    -----------------------------------
    s1, s2 : str
        The two strings among which to find the lcs

    Returns:
    -----------------------------------
    longest : str
        Required LCS

    """
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


def inflect(word, operations):
    """
    Inflects the given word by applying the operations on it
    Parameters:
    -----------------------------------
    word : str
        The word to be inflected
    operations : list
        Operation sequence to be applied to the input word to inflect it

    Returns:
    -----------------------------------
    word : str
        Inflected word
    """
    for operation in sorted(operations):
        method, chunk = operation.split('_')
        if method == 'delete':
            word = word.rstrip(chunk)
        else:
            word = word + chunk
    return word


def get_io_chunks(s1, s2):
    chunks = []
    while len(s1) != 0 or len(s2) != 0:
        if len(s1) != 0 and len(s2) != 0:
            l = lcs(s1, s2)
            if s1.find(l) == 0 and l:
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
                    s2 = s2[s2.find(l):]
            else:
                for c in list(s1):
                    chunks.append((c, ''))
                s1 = ''
        elif len(s1) != 0:
            for c in list(s1):
                chunks.append((c, ''))
            s1 = ''
        else:
            for c in list(s2):
                chunks.append(('', c))
            s2 = ''
    return chunks


def iterLCS(pdf):
    """
    Applies `lcs` method on the dataframe provided

    Parameters:
    -----------------------------------
    pdf : pd.DataFrame
        The dataframe where to apply to the lcs method

    Returns:
    pdf : pd.DataFrame
        The updated dataframe
    """
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
