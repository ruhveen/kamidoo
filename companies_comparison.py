import itertools
from consts import DEBUG_MODE


class CompaniesComparison(object):

    @staticmethod
    def merge_two_dicts(x, y):
        """Given two dicts, merge them into a new dict as a shallow copy."""
        z = x.copy()
        z.update(y)
        return z

    @staticmethod
    def get_all_shared_label_combinations_in_size_X(company_one, company_two, size):
        """
        Calculates all of the shared label combinations in the given size between company_one
        and company_two
        :param company_one:
        :param company_two:
        :param size:
        :return:
        """

        shared_labels_combination_id_to_labels = {}

        all_company_one_label_combinations_size_x =\
            CompaniesComparison.get_company_label_combinations_size_x(company_one, size)
        all_company_two_label_combinations_size_x =\
            CompaniesComparison.get_company_label_combinations_size_x(company_two, size)

        keys_a = set(all_company_one_label_combinations_size_x.keys())
        keys_b = set(all_company_two_label_combinations_size_x.keys())
        intersection = keys_a & keys_b

        if DEBUG_MODE:
            print "For %s and %s there are %s intersected combinations of labels\n" % \
              (company_one[0],company_two[0],len(intersection))

        return {hash_key:all_company_two_label_combinations_size_x[hash_key] for hash_key in intersection}

    @staticmethod
    def get_company_label_combinations_size_x(company, size):
        company_label_combinations_size_x = []
        try:
            company_one_labels = company[1]
            company_label_combinations_size_x = itertools.combinations(company_one_labels, size)
        except Exception as err:
            print '%s for %s' % (err, company)


        result = {hash(frozenset(x)):frozenset(x) for x in company_label_combinations_size_x}
        if DEBUG_MODE:
            print "For %s | %s (labels) choose %s (size) of combinations is %s" \
              % (company[0], len(company_one_labels), size, len(result))
        return result

    @staticmethod
    def find_groups_with_size(companies_to_labels, size):
        '''
        Calculates 3 return parameters:
        1. All combinations of all companies with all combinations of shared creterias of the given size -
        AS REQUESTED IN THE EMAIL
        2. All the groups with maximum number of companies that have shared criterias of the given size -
        BONUS
        3. All the Companies combinations with their max shared cretierias that have a minimum shared creteria
        of the given size.
        AS REQUESTED IN THE WHATSAPP AND IN EMAIL BOTTOM

        :param companies_to_labels:
        :param size:
        :return:
        '''

        # Company combination id its to set of companies
        companies_combination_ids_to_companies_store = {}

        # Label combination id to its set of labels
        labels_combination_ids_to_labels_combinations_store = {}

        # A dictionary that represents a company combination ID
        # To a list of label combination ids this company combination has
        companies_combination_ids_to_labels_combination_ids_lists = {}

        # A dictionary that represents a label combination ID
        # to a list of all of the maximum number of company names
        # that have that combination
        labels_combination_ids_to_max_companies_lists = {}

        for company_couples in itertools.combinations(companies_to_labels, 2):

            # If they're not in the same industry
            if not companies_to_labels[company_couples[0]][0] == companies_to_labels[company_couples[1]][0]:
                continue

            company_one_name = company_couples[0]
            company_two_name = company_couples[1]

            # Create a tuple of type: (name, labels array) for each company
            company_one = (company_one_name, companies_to_labels[company_couples[0]][1])
            company_two = (company_two_name, companies_to_labels[company_couples[1]][1])

            # Get all combinations of the shared labels between the 2 companies
            # In the form of a combination id to the set of labels
            shared_label_combination_ids_to_combinations = \
                CompaniesComparison.get_all_shared_label_combinations_in_size_X(company_one, company_two, size)

            # Add the new combination id to labels records to the dictionary
            # that contains all of the combination ids to labels of all of the companies
            labels_combination_ids_to_labels_combinations_store = \
                CompaniesComparison.merge_two_dicts(labels_combination_ids_to_labels_combinations_store,
                                shared_label_combination_ids_to_combinations)

            # For each shared combination between company_one and company_two
            for label_combination_id in shared_label_combination_ids_to_combinations.keys():

                new_companies_combination = [company_one_name, company_two_name]

                CompaniesComparison.add_new_companies_combination_to_companies_combination_store(label_combination_id,
                                                                             companies_combination_ids_to_labels_combination_ids_lists,
                                                                             companies_combination_ids_to_companies_store,
                                                                             list(new_companies_combination))

                # Add the current label combination to the current list of companies that also
                # have that combination
                if label_combination_id in labels_combination_ids_to_max_companies_lists:


                    # If company_one_name has the combination of label_combination_id
                    # but not in the list of companies that have the combination, then add it
                    if company_one_name not in labels_combination_ids_to_max_companies_lists[label_combination_id]:
                        labels_combination_ids_to_max_companies_lists[label_combination_id].append(company_one_name)

                        CompaniesComparison.add_new_companies_combination_to_companies_combination_store(label_combination_id,
                                                                                     companies_combination_ids_to_labels_combination_ids_lists,
                                                                                     companies_combination_ids_to_companies_store,
                                                                                     list(labels_combination_ids_to_max_companies_lists
                                                                                          [label_combination_id]))

                    # If company_two_name has the combination of label_combination_id
                    # but not in the list of companies that have the combination, then add it
                    if company_two_name not in labels_combination_ids_to_max_companies_lists[label_combination_id]:
                        labels_combination_ids_to_max_companies_lists[label_combination_id].append(company_two_name)

                        CompaniesComparison.add_new_companies_combination_to_companies_combination_store(label_combination_id,
                                                                                     companies_combination_ids_to_labels_combination_ids_lists,
                                                                                     companies_combination_ids_to_companies_store,
                                                                                     list(labels_combination_ids_to_max_companies_lists
                                                                                          [label_combination_id]))

                # If this is the first couple of companies who have this combination of labels
                # Then create a new record from this combination id to this current couple of companies
                else:
                    labels_combination_ids_to_max_companies_lists[label_combination_id] = new_companies_combination

        all_companies_with_all_labels_dict =\
            CompaniesComparison.all_companies_combos_with_all_labels_combos(companies_combination_ids_to_labels_combination_ids_lists,
                                                                            companies_combination_ids_to_companies_store,
                                                                            labels_combination_ids_to_labels_combinations_store)


        max_companies_dict = \
            CompaniesComparison.max_number_of_companies_for_label_combination\
                (labels_combination_ids_to_max_companies_lists,
                 labels_combination_ids_to_labels_combinations_store)


        all_with_max_dict = CompaniesComparison.all_companies_with_max_labels(companies_combination_ids_to_labels_combination_ids_lists,
                                                                              companies_combination_ids_to_companies_store,
                                                                              labels_combination_ids_to_labels_combinations_store)

        return all_companies_with_all_labels_dict, max_companies_dict, all_with_max_dict


    @staticmethod
    def add_new_companies_combination_to_companies_combination_store(label_combination_id,
                                                                     companies_combination_ids_to_label_combinations_ids_list,
                                                                     companies_combination_ids_to_companies_store,
                                                                     new_companies_combination):

        # Add new companies combination to the companies combination store
        new_companies_combination_id = hash(frozenset(new_companies_combination))

        if new_companies_combination_id not in companies_combination_ids_to_companies_store:
            companies_combination_ids_to_companies_store[new_companies_combination_id] = new_companies_combination

        # Add the new_companies_combination_id and its label_combination_id to the
        # dictionary between companies_combination_ids to their lists of label_combination_ids
        # The dictionary that contains for each companies combination, the list of all label combinations
        if not new_companies_combination_id in companies_combination_ids_to_label_combinations_ids_list:
            companies_combination_ids_to_label_combinations_ids_list[new_companies_combination_id] = []

        if not label_combination_id in companies_combination_ids_to_label_combinations_ids_list[new_companies_combination_id]:
            companies_combination_ids_to_label_combinations_ids_list[new_companies_combination_id].append(label_combination_id)


    @staticmethod
    def all_companies_combos_with_all_labels_combos(companies_combination_ids_to_labels_combination_ids_lists,
                                                    companies_combination_ids_to_companies_store,
                                                    labels_combination_ids_to_labels_combinations_store):
        '''
        All combinations of all companies with all combinations of shared creterias of size %s:
        :param companies_combination_ids_to_labels_combination_ids_lists:
        :param companies_combination_ids_to_companies_store:
        :param labels_combination_ids_to_labels_combinations_store:
        :return:
        '''
        result = []

        for companies_combination_id, labels_combination_ids_list \
                in companies_combination_ids_to_labels_combination_ids_lists.iteritems():
            for labels_combination_id in labels_combination_ids_list:

                current_companies_combination_labels_combination = \
                    [label for label in labels_combination_ids_to_labels_combinations_store[labels_combination_id]]

                result.append((companies_combination_ids_to_companies_store[companies_combination_id],
                              current_companies_combination_labels_combination))

        return result


    @staticmethod
    def max_number_of_companies_for_label_combination(labels_combination_ids_to_max_companies_lists,
                                                      labels_combination_ids_to_labels_combinations_store):
        '''
        All the Maximum number of companies that have a shared creteria of %s:
        :param labels_combination_ids_to_max_companies_lists:
        :param labels_combination_ids_to_labels_combinations_store:
        :return:
        '''

        result = []
        for labels_combination_id, max_companies_list in  labels_combination_ids_to_max_companies_lists.iteritems():

            current_companies_combination_labels_combination = \
                [label for label in labels_combination_ids_to_labels_combinations_store[labels_combination_id]]

            result.append((max_companies_list,current_companies_combination_labels_combination))
        return result

    @staticmethod
    def all_companies_with_max_labels(companies_combination_ids_to_labels_combination_ids_lists,
                                      companies_combination_ids_to_companies_store,
                                      labels_combination_ids_to_labels_combinations_store):
        '''
        All the Companies combinations with their max shared cretierias that have a minimum shared creteria of %s:
        :param companies_combination_ids_to_labels_combination_ids_lists:
        :param companies_combination_ids_to_companies_store:
        :param labels_combination_ids_to_labels_combinations_store:
        :return:
        '''

        result = []
        for companies_combination_id, labels_combination_ids_list in\
                companies_combination_ids_to_labels_combination_ids_lists.iteritems():
            current_companies_combination_labels_union = set([])
            for labels_combination_id in labels_combination_ids_list:

                current_companies_combination_labels_union = \
                    current_companies_combination_labels_union.union(
                        [label for label in labels_combination_ids_to_labels_combinations_store[labels_combination_id]])

            result.append((companies_combination_ids_to_companies_store[companies_combination_id],
                          list(current_companies_combination_labels_union)))

        return result