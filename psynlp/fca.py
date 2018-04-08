"""
Contains implementation of algorithms and data representation techniques in
Formal Concept Analysis.

For theory refer:

> Coursera course on Formal Concept Analysis by Sergei Obiedkov
> "Conceptual Exploration", Bernhard Ganter & Sergei Obiedkov
    - https://link.springer.com/content/pdf/10.1007%2F978-3-662-49291-8.pdf
"""
from ..psynlp import oracle
from ..psynlp.helper import init_concept_from_wordpairs, read_wordpairs, iterLCS
import itertools
import networkx as nx


class FCA(nx.Graph):
    """
    A formal concept (K) has the following properties:

    Attributes:
    objects (G)    : A set of objects
    attributes (M) : A set of attributes
    relations (I)  : A set of relations between objects (G) & attributes (M)
    """

    nqueries = 0
    pn_ratio = 0
    max_pn_ratio = 2

    def add_object(self, object_name):
        self.add_node(object_name, type='object')

    def add_objects(self, object_names):
        [self.add_object(object_name) for object_name in object_names]

    def add_attribute(self, attribute_name):
        self.add_node(attribute_name, type='attribute')

    def add_attributes(self, attribute_names):
        [self.add_attribute(attribute_name)
         for attribute_name in attribute_names]

    def add_relation(self, object_name, attribute_name):
        self.add_object(object_name)
        self.add_attribute(attribute_name)
        self.add_edge(object_name, attribute_name)

    def add_relations(self, relations):
        for (object_name, attribute_name) in relations:
            self.add_relation(object_name, attribute_name)

    def objects(self, attribute_name=None):
        if attribute_name is None:
            objects = [
                node for (
                    node, data) in self.nodes(
                    data=True) if data['type'] == 'object']
        else:
            objects = self[attribute_name]

        objects = sorted(objects)
        return(objects)

    def attributes(self, object_name=None):
        if object_name is None:
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
        Given a subset A of objects from G,
        A' = attributes shared by objects in A = objects intent
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
        Given a subset B of attributes from m,
        B' = objects shared by attributes in B = attributes extent
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
        Given a subset A of objects from G,
        A'  = attributes shared by objects in A = objects intent
        A'' = objects that share attributes in A'
        """
        return(self.attributes_extent(self.objects_intent(object_names)))

    def attributes_superset(self, attribute_names):
        """
        Given a subset B of attributes from G,
        B'  = objects shared by attributes in B = attributes extent
        B'' = attributes that share objects in B'
        """
        return(self.objects_intent(self.attributes_extent(attribute_names)))

    def all_subsets(self, master_set):
        all_subsets = []

        for subset_size in range(1, len(master_set) + 1):
            all_subsets += sorted(
                list(
                    itertools.combinations(
                        master_set,
                        subset_size)))

        return(all_subsets)

    def set_of_intents(self):
        """All matching attribute subsets such that B = B''
        """
        all_attribute_subsets = self.all_subsets(self.attributes())

        matching_attribute_subsets = set()
        for attribute_subset in all_attribute_subsets:
            if set(attribute_subset) == self.attributes_superset(
                    attribute_subset):
                matching_attribute_subsets.add(attribute_subset)
        return(matching_attribute_subsets)

    def relations(self):
        return(self.edges)

    def pretty_print(self):
        print("\n------------------------------------------------")
        print("Brief overview of this concept")
        print("------------------------------------------------")
        for object_name in self.objects():
            print("Object " + str(object_name) + " : " +
                  str(self.attributes(object_name)))
        print("Number of objects : ", len(self.objects()))
        print("Number of attributes : ", len(self.attributes()))
        print("Number of relations : ", len(self.relations()))
        print("------------------------------------------------")

    def implications(self, attribute_names=None):
        """
        A set of all possible implications between attributes within B
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

    def is_model_of_implication(
            self,
            attribute_names,
            antecedent_attrs,
            consequent_attrs):
        """
        The set A is closed under a set of implications L if A is closed under every implication in L
        """
        attribute_names = set(attribute_names)
        antecedent_attrs = set(antecedent_attrs)
        consequent_attrs = set(consequent_attrs)
        return((not antecedent_attrs.issubset(attribute_names)) or (consequent_attrs.issubset(attribute_names)))

    def is_model_of_implications(self, attribute_names, implications):
        for (antecedent_attrs, consequent_attrs) in implications:
            if not self.is_model_of_implication(
                    attribute_names, antecedent_attrs, consequent_attrs):
                return(False)
        return(True)

    def models(self, set_of_implications=None, attribute_names=None):
        """The set of all sets closed under L, the models of L, is denoted by Mod(L).
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
        For an implication to be valid, X' should be subset of Y'.
        """
        antecedent_attrs_prime = self.attributes_extent(set(antecedent_attrs))
        consequent_attrs_prime = self.attributes_extent(set(consequent_attrs))
        return(antecedent_attrs_prime.issubset(consequent_attrs_prime))

    def theory(self):
        """The set of all implications valid in K is the theory of K, denoted by Th(K).
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
        """
        return(self.models(implications) == self.set_of_intents())

    def is_irredundant_basis(self, implications):
        """A basis L of K is called irredundant if no strict subset of L is a basis of K
        """
        for subset_size in range(1, len(implications)):
            for implications_subset in itertools.combinations(
                    implications, subset_size):
                if self.is_basis(implications_subset):
                    return(False)
        return(True)

    def closure_under_implications(self, attributes, implications):
        stable = False

        while not stable:
            stable = True
            remove_implications = set()
            for (antecedent_attrs, consequent_attrs) in implications:
                if set(antecedent_attrs).issubset(attributes):
                    attributes = attributes.union(set(consequent_attrs))
                    stable = False
                    remove_implications.add(
                        (antecedent_attrs, consequent_attrs))

        implications = implications - remove_implications

        return(attributes)

    def nextClosure(
            self,
            previous_closure,
            attribute_names=None,
            closure_operator=None):
        if previous_closure is None:
            previous_closure = set()

        if attribute_names is None:
            attribute_names = self.attributes()

        attribute_names = list(attribute_names)
        attribute_names.reverse()

        next_closure = set()

        for attribute_name in attribute_names:
            if attribute_name in previous_closure:
                previous_closure = previous_closure - {attribute_name}
            else:
                next_set = previous_closure.union({attribute_name})
                if closure_operator is None:
                    print("''")
                    next_closure = self.attributes_superset(next_set)
                else:
                    next_closure = self.closure_under_implications(
                        next_set, closure_operator)

                if self.hasNoElementLecticallyLessThan(
                        next_closure - previous_closure, attribute_names, attribute_name):
                    return(next_closure)
        return(set())

    def hasNoElementLecticallyLessThan(self, subset, complete_list, value):
        sublist = list(subset)

        index = complete_list.index(value)
        for element in sublist:
            element_index = complete_list.index(element)
            if element_index < index:
                return(False)
        return(True)

    def canonical_basis(self, attribute_names=None):
        implications = set()
        attributes_subset = set()
        attribute_names = self.attributes()

        while attributes_subset != set(attribute_names):
            attributes_superset = self.attributes_superset(attributes_subset)

            if attributes_subset != attributes_superset:
                implications = implications.union(
                    {(tuple(attributes_subset), tuple(attributes_superset))})
            attributes_subset = self.nextClosure(
                attributes_subset, attribute_names, implications)
            print(set(attribute_names) - attributes_subset)

        return(implications)

    def implications_not_respecting_attributes(
            self, attribute_names, implications):
        disrespectful_implications = set()
        for (antecedent_attrs, consequent_attrs) in implications:
            if not self.is_model_of_implication(
                    attribute_names, antecedent_attrs, consequent_attrs):
                disrespectful_implications.add(
                    (antecedent_attrs, consequent_attrs))
        return(disrespectful_implications)

    def replace_disrespectful_implications(
            self,
            implications,
            disrespectful_implications,
            attribute_names):
        # replace all disrepectful implications A->B by A->BnC
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
        for (antecedent_attrs, consequent_attrs) in implications:
            antecedent_attrs = set(antecedent_attrs)
            consequent_attrs = set(consequent_attrs)
            attribute_names = set(attribute_names)

        if attribute_names.intersection(antecedent_attrs) != antecedent_attrs and not is_member(
                implications, attribute_names.intersection(antecedent_attrs), self.attributes_superset):
            return((tuple(sorted(antecedent_attrs)), tuple(sorted(consequent_attrs))))

    def clean_hypothesis(self, H):
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
        H = set()

        C, self.nqueries, self.pn_ratio = is_equivalent(H)
        while C is not True:
            # if some A->B belonging to H does not respect C: not(A doesnt
            # belong to C or B belongs to C)
            disrespectful_implications = self.implications_not_respecting_attributes(
                C, H)
            if len(disrespectful_implications) is not 0:
                print("Negative counter-example")
                print("Block 1")
                # replace all such implications A->B by A->BnC
                H = self.replace_disrespectful_implications(
                    H, disrespectful_implications, C)
            else:
                print("Positive counter-example")

                # find first A->B belonging to H such that CnA not equal to A
                # and not is_member(H, CnA)
                such_implication = self.find_not_members(H, C, is_member)
                # if such A->B doesnt exist:
                if such_implication is None:
                    # add C->M to H
                    print("Block 3")
                    H.add((tuple(sorted(C)), tuple(self.attributes())))
                else:
                    # replace A->B by CnA -> BU(A-C)
                    print("Block 2")
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

                C, self.nqueries, self.pn_ratio = is_equivalent(H)
                # wait_till_user_responds = input("Press enter to go through
                # next loop")
                j = 0
                for (antecedent_attrs, consequent_attrs) in H:
                    j += 1
                    print("PAC Implication",
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
        return(self.horn1(is_member, oracle.is_approx_equivalent(is_member, self.attibutes(), self.nqueries, self.attributes_extent, self.attributes_superset, self.is_model_of_implications, self.pn_ratio, self.max_pn_ratio, epsilon, delta)))

