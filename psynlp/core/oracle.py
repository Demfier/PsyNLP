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
    """
    Tells if a given attribute set is a memeber of hypothesis or not, i.e
    if it is closed or not.
    Parameters:
    -----------------------------------
    hypothesis : set
        Hypothesis set under consideration
    attributes_subset : set
        The attribute set to be tested for membership
    attributes_superset : function
        Function to compute closure of an attribute set
    """
    attributes_subset = set(attributes_subset)
    return(attributes_subset == attributes_superset(attributes_subset))


def generate_subset(any_set):
    """
    Randomly samples a subset for a given any_set. To be used for sampling
    attributes in the equivalence oracle.
    Parameters:
    -----------------------------------
    any_set : set
        The set whose subsets are to be generated

    Returns:
    -----------------------------------
    subset : set
        The randomly sampled subset of any_set
    """
    subset = set()
    random.shuffle(any_set)
    for element in any_set:
        if random.random() > 0.5:
            subset.add(element)
    return(subset)


def generate_positive_counterexample(H, M, li_times, is_member, is_model,
                                     attributes_superset, nqueries, pn_ratio):
    """
    Generates positive counterexmample for a given hypothesis set H.
    Parameters:
    -----------------------------------
    H : set
        Hypothesis set
    M : set
        Attribute set
    li_times : int
        Funtion to compute the number of times to loop in the counterexample
        generating part
    is_member : function
        Membership oracle
    is_model : function
        Function to tell if X is a model of H or not
    attributes_superset : function
        Function to calcuate closure of the given attribute set
    nqueries : int
        Number of times the equivalence oracle has been called already
    pn_ratio : int
        The postive to negative counterexample ratio to be referred to while
        'forcing' the implications to disrespect
    """
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
    """
    Approx equivalent oracle to be used in pac-basis
    Parameters:
    -----------------------------------
    is_member : function
        Membership oracle
    M : set
        Attribute set
    nqueries : int
        Number of times the equivalence oracle has been called already
    attributes_extent : function
        Function to find objects shared by the given attributes
    attributes_superset : function
        Function to calcuate closure of the given attribute set
    is_model : function
        Function to tell if X is a model of H or not
    pn_ratio : int
        The postive to negative counterexample ratio to be referred to while
        'forcing' the implications to disrespect
    max_pn_ration : int
        The maximum value of pn_ratio (2 in the current setting)
    epsilon : float (0, 1)
            Tolerance for error in accuracy for the pac-basis
    delta : float (0, 1)
        Tolerance for confidence in confidence for the pac-basis

    Returns:
    -----------------------------------
    query_oracle : function
        Function that actually performs all the logic of the approx-equivalence
        oracle
    """
    def query_oracle(hypothesis, nqueries, li_times, pn_ratio, max_pn_ratio):
        """
        Tells if the given hypothesis is equivalent to the desired hypothesis
        or not

        Returns:
        -----------------------------------
        (True, nqueries, pn_ratio) - if current hypothesis is equivalent to the
                                     desired one
        (counterexample, nqueries, pn_ratio) - otherwise
        """
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
    """
    Computes li, the optimal number of times to loop while sampling the
    equivalence oracle. This li is the reason pac-basis is sooo much faster
    than the original horn1 algorithm.

    Parameters:
    -----------------------------------
    i : int
        Number of times the equivalence oracle has been called already
    epsilon : float (0, 1)
            Tolerance for error in accuracy for the pac-basis
    delta : float (0, 1)
        Tolerance for confidence in confidence for the pac-basis
    """
    return((1.0 / epsilon) * (i - (math.log(delta) / math.log(2))))
