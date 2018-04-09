"""
Contains algorithms needed for oracle-learning.

For theory, refer:

> "Queries and Concept Learning", Dana Angluin
    - (https://link.springer.com/content/pdf/10.1023%2FA%3A1022821128753.pdf)
> "On the Usability of Probably Approximately Correct Implication Bases",
   Daniel Borchmann Tom Hanika and Sergei Obiedkov
    - https://arxiv.org/pdf/1701.00877.pdf
"""
import math
import random


def is_member(hypothesis, attributes_subset, attributes_superset):
    attributes_subset = set(attributes_subset)
    return(attributes_subset == attributes_superset(attributes_subset))


def generate_subset(any_set):
    subset = set()
    random.shuffle(any_set)
    for element in any_set:
        if random.random() > 0.5:
            subset.add(element)
    return(subset)


def generate_positive_counterexample(H, M, li_times, is_member, is_model,
                                     attributes_superset, nqueries, pn_ratio):
    for i in range(int(li_times)):
        X = generate_subset(M)
        member = is_member(H, X, attributes_superset)
        model = is_model(X, H)
        if (member and not model) or (not member and model):
            return(X, nqueries, pn_ratio)
    return(True, nqueries, pn_ratio)


def is_approx_equivalent(is_member, M, nqueries, attributes_extent,
                         attributes_superset, is_model, pn_ratio, max_pn_ratio,
                         epsilon=0.5, delta=0.5):

    def query_oracle(hypothesis, nqueries, li_times, pn_ratio, max_pn_ratio):
        nqueries += 1
        li_times = li_times(nqueries, epsilon, delta)

        if pn_ratio < max_pn_ratio:
            pn_ratio += 1
            return(generate_positive_counterexample(hypothesis, M, li_times,
                                                    is_member, is_model,
                                                    attributes_superset,
                                                    nqueries, pn_ratio))
        else:
            verbose_print_3("Giving negative counter-example")
            pn_ratio = 0
            H = hypothesis

            for i in range(int(li_times)):
                for antecedent_attrs, consequent_attrs in H:
                    if len(attributes_extent(set(consequent_attrs))) == 0:
                        antecedent_superset = attributes_superset(
                            set(antecedent_attrs))
                        if len(attributes_extent(antecedent_superset)) != 0:
                            return(antecedent_superset, nqueries, pn_ratio)

                verbose_print_3("Redirecting to usual positive counter-example")
                return(generate_positive_counterexample(H, M, li_times,
                                                        is_member, is_model,
                                                        attributes_superset,
                                                        nqueries, pn_ratio))
    return(query_oracle)


def li_times(i, epsilon, delta):
    return((1.0 / epsilon) * (i - (math.log(delta) / math.log(2))))
