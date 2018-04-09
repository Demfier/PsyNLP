"""
Contains implementation of algorithms and data representation techniques in
Formal Concept Analysis.

For theory refer:

> Coursera course on Formal Concept Analysis by Sergei Obiedkov
> "Conceptual Exploration", Bernhard Ganter & Sergei Obiedkov
    - https://link.springer.com/content/pdf/10.1007%2F978-3-662-49291-8.pdf
"""
import itertools
import networkx as nx
from ..core import oracle


class FCA(nx.Graph):
    """
    Class to represent methods in Formal Concept Analysis.

    A formal concept (K) has the following properties:

    Attributes:
    objects (G)    : A set of objects (operation sequences for our case)
    attributes (M) : A set of attributes (source words for our case)
    relations (I)  : A set of relations between objects (G) & attributes (M)
    """

    nqueries = 0
    pn_ratio = 0
    max_pn_ratio = 2

    def add_object(self, object_name):
        """
        Adds a new object to the concept.
        Parameters:
        -----------------------------------
        object_name : str
            Name of the object to be added to the concept
        """
        self.add_node(object_name, type='object')

    def add_objects(self, object_names):
        """
        Adds multiple objects to the concept.
        Parameters:
        -----------------------------------
        object_names : list
            Array of object names to be added to the concept
        """
        [self.add_object(object_name) for object_name in object_names]

    def add_attribute(self, attribute_name):
        """
        Adds a new attribute to the concept.
        Parameters:
        -----------------------------------
        attribute_name : str
            Name of the attribute to be added to the concept
        """
        self.add_node(attribute_name, type='attribute')

    def add_attributes(self, attribute_names):
        """
        Adds multiple attributes to the concept.
        Parameters:
        -----------------------------------
        attribute_names : list
            Array of attribute names to be added to the concept
        """
        [self.add_attribute(attribute_name)
         for attribute_name in attribute_names]

    def add_relation(self, object_name, attribute_name):
        """
        Adds a relation to the concept. Since our concept lattice is a
        Directed networkx graph, relations are nothing but edges of the graph.
        Parameters:
        -----------------------------------
        object_name : str
            Name of the object in the relation
        attribute_name : str
            Name of the attribute in the relation
        """
        self.add_object(object_name)
        self.add_attribute(attribute_name)
        self.add_edge(object_name, attribute_name)

    def add_relations(self, relations):
        """
        Adds multiple relations to the concept.
        Parameters:
        -----------------------------------
        relations : list
            list of relations to be added to the concept
        """
        for (object_name, attribute_name) in relations:
            self.add_relation(object_name, attribute_name)

    def objects(self, attribute_name=None):
        """
        Returns objects corresponding to an attribute.
        Parameters:
        -----------------------------------
        attribute_name : str
            Attribute whose objects are to found

        Returns:
        -----------------------------------
        objects : list
            Array of objects corresponding to the given attribute_name
        """
        if attribute_name is None:
            # Return all the objects in the lattice
            objects = [
                node for (
                    node, data) in self.nodes(
                    data=True) if data['type'] == 'object']
        else:
            objects = self[attribute_name]

        objects = sorted(objects)
        return(objects)

    def attributes(self, object_name=None):
        """
        Returns attributes corresponding to an object.
        Parameters:
        -----------------------------------
        object_name : str
            Object whose attributes are to found

        Returns:
        -----------------------------------
        attributes : list
            Array of attributes corresponding to the given object_name
        """
        if object_name is None:
            # Return all attributes in the concept
            attributes = [
                node for (
                    node, data) in self.nodes(
                    data=True) if data['type'] == 'attribute']
        else:
            attributes = self[object_name]

        attributes = sorted(attributes)
        return(attributes)

    def objects_intent(self, object_names):
        """
        Given a subset A of objects from G, calculates:
        A' = attributes shared by objects in A = objects intent
        Parameters:
        -----------------------------------
        object_names : list
            Arrary of objects whose intent is to be found

        Returns:
        -----------------------------------
        shared_attributes : set
            The set of attributes sharing the objects in object_names
        """
        if len(object_names) is 0:
            return(self.attributes())
        else:
            attribute_sets = [set(self.attributes(object_name))
                              for object_name in object_names]
            shared_attributes = set.intersection(*attribute_sets)
        return(shared_attributes)

    def attributes_extent(self, attribute_names):
        """
        Given a subset B of attributes from m, calculates:
        B' = objects shared by attributes in B = attributes extent.
        Parameters:
        -----------------------------------
        attribute_names : list
            Arrary of attributes whose extent is to be found

        Returns:
        -----------------------------------
        shared_objects : set
            The set of objects sharing the attributes in attribute_names
        """
        if len(attribute_names) is 0:
            return(self.objects())
        else:
            object_sets = [set(self.objects(attribute_name))
                           for attribute_name in attribute_names]
            shared_objects = set.intersection(*object_sets)
        return(shared_objects)

    def objects_superset(self, object_names):
        """
        Equal to `closure` operation for an object set discussed in theory.
        Given a subset A of objects from G, calculates
        A'  = attributes shared by objects in A = objects intent
        A'' = objects that share attributes in A'.
        Parameters:
        -----------------------------------
        objects_names : list
            List of objects whose closure is to be calculated

        Returns:
        -----------------------------------
        closure of object_names
        """
        return(self.attributes_extent(self.objects_intent(object_names)))

    def attributes_superset(self, attribute_names):
        """
        Equal to `closure` operation for an attribute set discussed in theory.
        Given a subset B of attributes from G,
        B'  = objects shared by attributes in B = attributes extent
        B'' = attributes that share objects in B'.
        Parameters:
        -----------------------------------
        attributes_names : list
            List of attributes whose closure is to be calculated

        Returns:
        -----------------------------------
        closure of attribute_names
        """
        return(self.objects_intent(self.attributes_extent(attribute_names)))

    def all_subsets(self, master_set):
        """
        Finds all the subsets for a given master_set.
        Parameters:
        -----------------------------------
        master_set : set
            Set whose subsets are to calculated

        Returns:
        -----------------------------------
        all_subsets : list
            Array of all the subsets of the given master_set
        """
        all_subsets = []

        for subset_size in range(1, len(master_set) + 1):
            all_subsets += sorted(
                list(
                    itertools.combinations(
                        master_set,
                        subset_size)))
        return(all_subsets)

    def set_of_intents(self):
        """
        Gives all matching attribute subsets such that B = B''.
        """
        all_attribute_subsets = self.all_subsets(self.attributes())

        matching_attribute_subsets = set()
        for attribute_subset in all_attribute_subsets:
            if set(attribute_subset) == self.attributes_superset(
                    attribute_subset):
                matching_attribute_subsets.add(attribute_subset)
        return(matching_attribute_subsets)

    def relations(self):
        """
        Gives all the relations in the lattice
        """
        return(self.edges)

    def pretty_print(self):
        verbose_print_3("\n------------------------------------------------")
        verbose_print_3("Brief overview of this concept")
        verbose_print_3("------------------------------------------------")
        for object_name in self.objects():
            verbose_print_3("Object " + str(object_name) + " : " +
                  str(self.attributes(object_name)))
        verbose_print_3("Number of objects : ", len(self.objects()))
        verbose_print_3("Number of attributes : ", len(self.attributes()))
        verbose_print_3("Number of relations : ", len(self.relations()))
        verbose_print_3("------------------------------------------------")

    def implications(self, attribute_names=None):
        """
        Gives the set of all possible implications between attributes in B
        Parameters:
        -----------------------------------
        attribute_names : set
            Set of all the attributes among which to find the implications

        Returns:
        -----------------------------------
        matching_attributes_pairs : set
            Set of implications (represented as tuples)
        """
        if attribute_names is None:
            attribute_names = self.attributes()

        attribute_subsets = self.all_subsets(attribute_names)
        matching_attribute_pairs = set()

        all_attribute_pairs = itertools.combinations(attribute_subsets, 2)
        for (attr_1, attr_2) in all_attribute_pairs:
            attr_1_prime = self.attributes_extent(attr_1)
            attr_2_prime = self.attributes_extent(attr_2)

        if attr_1_prime.issubset(attr_2_prime):
            matching_attribute_pairs.add((attr_1, attr_2))
        else:
            if attr_2_prime.issubset(attr_1_prime):
                matching_attribute_pairs.add((attr_2, attr_1))

        return(matching_attribute_pairs)

    def is_model_of_implication(self, attribute_names, antecedent_attrs,
                                consequent_attrs):
        """
        Determines where a given set A follows an implication L.
        Parameters:
        -----------------------------------
        attribute_names : set
            Set of all the attributes among which to find the implications
        antecedent_attrs : set
            Attributes in the premise of an implication
        consequent_attrs : set
            Attributes in the conclusion of an implication
        """
        attribute_names = set(attribute_names)
        antecedent_attrs = set(antecedent_attrs)
        consequent_attrs = set(consequent_attrs)
        return((not antecedent_attrs.issubset(attribute_names)) or (consequent_attrs.issubset(attribute_names)))

    def is_model_of_implications(self, attribute_names, implications):
        """
        Determines where a given set A is closed under a set of implications L
        by checking if A is closed under every implication in L.
        Parameters:
        -----------------------------------
        attribute_names : set
            Set of all the attributes among which to find the implications
        implications : list[tuple]
            Array of implications
        """
        for (antecedent_attrs, consequent_attrs) in implications:
            if not self.is_model_of_implication(
                    attribute_names, antecedent_attrs, consequent_attrs):
                return(False)
        return(True)

    def models(self, set_of_implications=None, attribute_names=None):
        """
        Gives the set of all sets closed under L i.e the models of L,
        denoted by Mod(L).
        Parameters:
        -----------------------------------
        set_of_implications : list
            Impliction set whose models are to determined
        attribute_names : set
            Testing attribute set to tell whether it is a model of the
            set_of_implications or not

        Returns:
        -----------------------------------
        matching_attribute_subsets : set
            Set of models of the given implication set
        """
        if set_of_implications is None:
            set_of_implications = self.implications()

        if attribute_names is None:
            attribute_names = self.attributes()

        all_attribute_subsets = self.all_subsets(
            self.attributes())  # ! Should these be all attrs?
        matching_attribute_subsets = set()

        for attribute_subset in all_attribute_subsets:
            is_closed = True
        for (antecedent_attrs, consequent_attrs) in set_of_implications:
            is_closed = is_closed and self.is_model_of_implication(
                attribute_subset, antecedent_attrs, consequent_attrs)

        if is_closed:
            matching_attribute_subsets.add(attribute_subset)
        return(matching_attribute_subsets)

    def valid_implication(self, antecedent_attrs, consequent_attrs):
        """
        Determines if an implication is valid or not
        For an implication to be valid, X' should be subset of Y'.
        Parameters:
        -----------------------------------
        antecedent_attrs : set
            Premise of the implication whose validity to check
        consequent_attrs : set
            Conclusion of the implication whose validity to check
        """
        antecedent_attrs_prime = self.attributes_extent(set(antecedent_attrs))
        consequent_attrs_prime = self.attributes_extent(set(consequent_attrs))
        return(antecedent_attrs_prime.issubset(consequent_attrs_prime))

    def theory(self):
        """
        The set of all implications valid in K is the theory of K,
        denoted by Th(K).
        Returns:
        -----------------------------------
        matching_implications: set
            Theory of the concept
        """
        all_implications = self.implications()
        matching_implications = set()

        for (antecedent_attrs, consequent_attrs) in all_implications:
            if self.valid_implication(antecedent_attrs, consequent_attrs):
                matching_implications.add((antecedent_attrs, consequent_attrs))

        return(matching_implications)

    def is_basis(self, implications):
        """
        A set L ⊆ Imp(M) is a basis of K if the models of L are the intents of K.
        Parameters:
        -----------------------------------
        implications : set
            The set of implications under testing
        """
        return(self.models(implications) == self.set_of_intents())

    def is_irredundant_basis(self, implications):
        """
        A basis L of K is called irredundant if no strict subset of L is a
        basis of K.
        Parameters:
        -----------------------------------
        implications : set
            The set of implications under testing
        """
        for subset_size in range(1, len(implications)):
            for implications_subset in itertools.combinations(
                    implications, subset_size):
                if self.is_basis(implications_subset):
                    return(False)
        return(True)

    def implications_not_respecting_attributes(self, attribute_names,
                                               implications):
        """
        Gives a set of implications not respecting a given attribute set.
        Parameters:
        -----------------------------------
        attribute_names : set
            Set of attributes under consideration
        implications : set
            The set of implications under testing

        Returns:
        disrespectful_implications : set
            Set of implications not respecting attribute_names
        """
        disrespectful_implications = set()
        for (antecedent_attrs, consequent_attrs) in implications:
            if not self.is_model_of_implication(
                    attribute_names, antecedent_attrs, consequent_attrs):
                disrespectful_implications.add(
                    (antecedent_attrs, consequent_attrs))
        return(disrespectful_implications)

    def replace_disrespectful_implications(self, implications,
                                           disrespectful_implications,
                                           attribute_names):
        """
        Replaces all the disrepectful implications A --> B by A --> BnC.
        Parameters:
        -----------------------------------
        implications : set
            The set of implications under consideration
        disrespectful_implications : set
            The set of implications not respecting the given attribute_names
        attribute_names : set
            Set of attributes under consideration

        Returns:
        final_implications : set
            Updated set of implications
        """
        final_implications = set()
        for implication in implications:
            if implication in disrespectful_implications:
                antecedent_attrs, consequent_attrs = implication
                consequent_attrs = tuple(
                    sorted(set(consequent_attrs).intersection(attribute_names)))
                final_implications.add((antecedent_attrs, consequent_attrs))
            else:
                final_implications.add(implication)
        return(final_implications)

    def find_not_members(self, implications, attribute_names, is_member):
        """
        Returns an implication from the given set of implications that is not a
        member of the hypothesis, i.e gives a negative test with the membership
        oracle.
        Parameters:
        -----------------------------------
        implications : set
            The set of implications under consideration
        attribute_names : set
            Set of attributes under consideration
        is_member : function
            Membership oracle
        """
        for (antecedent_attrs, consequent_attrs) in implications:
            antecedent_attrs = set(antecedent_attrs)
            consequent_attrs = set(consequent_attrs)
            attribute_names = set(attribute_names)

            if attribute_names.intersection(antecedent_attrs) != antecedent_attrs and not is_member(
                    implications, attribute_names.intersection(antecedent_attrs), self.attributes_superset):
                return((tuple(sorted(antecedent_attrs)), tuple(sorted(consequent_attrs))))

    def clean_hypothesis(self, H):
        """
        Removes duplicate implications from the hypothesis H.
        Parameters:
        -----------------------------------
        H : set[tuple]
            The hypothesis to be cleaned

        Returns:
        -----------------------------------
        H2 : set[tuple]
            Cleaned hypothesis
        """
        all_shared_objects = set()
        H2 = set()
        for (antecedent_attrs, consequent_attrs) in H:
            shared_objects = tuple(
                sorted(
                    self.attributes_extent(
                        set(consequent_attrs))))
            if shared_objects not in all_shared_objects and len(
                    shared_objects) > 0:
                all_shared_objects.add(shared_objects)
                H2.add((antecedent_attrs, consequent_attrs))
        return(H2)

    def horn1(self, is_member, is_equivalent):
        """
        The famous HORN1 algorithm to find implications for the concept
        Parameters:
        -----------------------------------
        is_member : function
            Membership oracle
        is_equivalent : function
            Equivalence oracle

        Returns:
        -----------------------------------
        H : set
            The computed set of implications for the given concept lattice
        """
        H = set()

        C, self.nqueries, self.pn_ratio = is_equivalent(H, self.nqueries,
                                                        oracle.li_times,
                                                        self.pn_ratio,
                                                        self.max_pn_ratio)
        while C is not True:
            # if some A->B belonging to H does not respect C: not(A doesnt
            # belong to C or B belongs to C)
            disrespectful_implications = self.implications_not_respecting_attributes(
                C, H)
            if len(disrespectful_implications) is not 0:
                verbose_print_3("Present in Block-1 of Horn1")
                # replace all such implications A->B by A->BnC
                H = self.replace_disrespectful_implications(
                    H, disrespectful_implications, C)
            else:
                # find first A->B belonging to H such that CnA not equal to A
                # and not is_member(H, CnA)
                such_implication = self.find_not_members(H, C, is_member)
                # if such A->B doesnt exist:
                if such_implication is None:
                    # add C->M to H
                    verbose_print_3("Present in Block-3 of Horn1")
                    H.add((tuple(sorted(C)), tuple(self.attributes())))
                else:
                    # replace A->B by CnA -> BU(A-C)
                    verbose_print_3("Present in Block-2 of Horn1")
                    C = set(C)
                    H.discard(such_implication)
                    antecedent_attrs, consequent_attrs = such_implication
                    antecedent_attrs = set(antecedent_attrs)
                    consequent_attrs = set(consequent_attrs)
                    antecedent_attrs = C.intersection(antecedent_attrs)
                    consequent_attrs = consequent_attrs.union(
                        antecedent_attrs - C)
                    H.add(
                        (tuple(
                            sorted(antecedent_attrs)), tuple(
                            sorted(consequent_attrs))))

            C, self.nqueries, self.pn_ratio = is_equivalent(H,
                                                            self.nqueries,
                                                            oracle.li_times,
                                                            self.pn_ratio,
                                                            self.max_pn_ratio)
            # wait_till_user_responds = input("Press enter to go through
            # next loop")
            j = 0
            for (antecedent_attrs, consequent_attrs) in H:
                j += 1
                verbose_print_3("PAC Implication",
                      j,
                      ":",
                      len(antecedent_attrs),
                      "attributes:",
                      " ->",
                      len(consequent_attrs),
                      "attributes with",
                      len(self.attributes_extent(set(consequent_attrs))),
                      "objects:",
                      self.attributes_extent(set(consequent_attrs)))

        H = self.clean_hypothesis(H)
        return(H)

    def pac_basis(self, is_member, epsilon=0.8, delta=0.5):
        """
        The even more famous PAC algorithm to compute canonical basis for a
        given concept lattice
        Parameters:
        -----------------------------------
        is_member : function
            Membership oracle
        epsilon : float (0, 1)
            Tolerance for error in accuracy for the pac-basis
        delta : float (0, 1)
            Tolerance for confidence in confidence for the pac-basis

        Returns:
        -----------------------------------
        The computed pac-basis for given concept lattice
        """
        return(self.horn1(is_member, oracle.is_approx_equivalent(is_member, self.attributes(), self.nqueries, self.attributes_extent, self.attributes_superset, self.is_model_of_implications, self.pn_ratio, self.max_pn_ratio, epsilon, delta)))
