import unittest
from companies_comparison import CompaniesComparison


class TestComapniesComparison(unittest.TestCase):

    def assertListOfSets(self,list1,list2):

        new_list1 = []
        for tup in list1:
            new_list1.append((frozenset(tup[0]),frozenset(tup[1])))
        new_list1= frozenset(new_list1)

        new_list2 = []
        for tup in list2:
            new_list2.append((frozenset(tup[0]),frozenset(tup[1])))
        new_list2= frozenset(new_list2)

        self.assertEqual(new_list1,new_list2)

    def assertIsItemContained(self,list1,list2):

        new_list1 = []
        for tup in list1:
            new_list1.append((frozenset(tup[0]),frozenset(tup[1])))
        new_list1= frozenset(new_list1)


        new_list2 = (frozenset(list2[0]),frozenset(list2[1]))

        self.assertIn(new_list2, new_list1)

    def test_one(self):

        input = {}
        input["a"] = ('in',["1","2"])
        input["b"] = ('in',["1","2"])

        all_companies_with_all_labels_dict,max_companies_dict,all_with_max_dict= \
            CompaniesComparison.find_groups_with_size(input,2)

        self.assertEqual(all_companies_with_all_labels_dict, [(["a","b"],["1","2"])])

    def test_two(self):

        input = {}
        input["a"] = ('in',["1","2","3"])
        input["b"] = ('in',["1","2","4"])

        all_companies_with_all_labels_dict,max_companies_dict,all_with_max_dict= \
            CompaniesComparison.find_groups_with_size(input,3)

        self.assertEqual(all_companies_with_all_labels_dict, [])

    def test_three(self):

        input = {}
        input["a"] = ('in',["1","2","3"])
        input["b"] = ('in',["1","2","3","4"])

        all_companies_with_all_labels_dict,max_companies_dict,all_with_max_dict= \
            CompaniesComparison.find_groups_with_size(input,3)

        self.assertListOfSets(all_companies_with_all_labels_dict, [(["a","b"],["1","2","3"])])


    def test_four(self):

        input = {}
        input["a"] = ('in',["1","2","3"])
        input["b"] = ('in',["1","2","3","4"])
        input["c"] = ('in',["2","3","4"])

        all_companies_with_all_labels_dict,max_companies_dict,all_companies_max_labels= \
            CompaniesComparison.find_groups_with_size(input,2)

        self.assertIsItemContained(all_companies_with_all_labels_dict, (["a","b","c"],["2","3"]))
        self.assertIsItemContained(all_companies_with_all_labels_dict, (["a","c"],["2","3"]))
        self.assertIsItemContained(all_companies_with_all_labels_dict, (["a","b"],["1","2"]))
        self.assertIsItemContained(all_companies_with_all_labels_dict, (["a","b"],["2","3"]))

        self.assertIsItemContained(max_companies_dict, (["a","b","c"],["2","3"]))

        self.assertIsItemContained(all_companies_max_labels, (["a","b","c"],["2","3"]))


    def test_five(self):

        input = {}
        input["a"] = ('in',["1","2","3"])
        input["b"] = ('in',["1","2","3","4"])
        input["c"] = ('in',["2","3","4"])
        input["d"] = ('in',["1","2","3","4","5"])

        all_companies_with_all_labels_dict,max_companies_dict,all_companies_max_labels= \
            CompaniesComparison.find_groups_with_size(input,2)

        self.assertIsItemContained(all_companies_with_all_labels_dict, (["a","b","c"],["2","3"]))
        self.assertIsItemContained(all_companies_with_all_labels_dict, (["a","c"],["2","3"]))
        self.assertIsItemContained(all_companies_with_all_labels_dict, (["a","b"],["1","2"]))
        self.assertIsItemContained(all_companies_with_all_labels_dict, (["a","b"],["2","3"]))

        self.assertIsItemContained(all_companies_max_labels, (["b","d"],["1","2","3","4"]))

    def test_six(self):

        input = {}
        input["a"] = ('in',["1","2","3"])
        input["b"] = ('in',["1","2","3","4"])
        input["c"] = ('in',["2","3","4"])
        input["d"] = ('in',["1","2","3","4","5"])

        all_companies_with_all_labels_dict,max_companies_dict,all_companies_max_labels= \
            CompaniesComparison.find_groups_with_size(input,4)

        self.assertIsItemContained(all_companies_with_all_labels_dict, (["d","b"],["2","3","1","4"]))
        self.assertIsItemContained(all_companies_max_labels, (["d","b"],["2","3","1","4"]))

    def test_seven(self):

        input = {}
        input["a"] = ('in1',["1","2","3","5"])
        input["b"] = ('in2',["1","2","3","4"])
        input["c"] = ('in1',["2","3","4"])
        input["d"] = ('in1',["1","2","3","4","5"])

        all_companies_with_all_labels_dict,max_companies_dict,all_companies_max_labels= \
            CompaniesComparison.find_groups_with_size(input,4)

        self.assertIsItemContained(all_companies_with_all_labels_dict, (["d","a"],["2","3","1","5"]))
        self.assertIsItemContained(all_companies_max_labels, (["d","a"],["2","3","1","5"]))

    def test_eight(self):

        input = {}
        input["a"] = ('in1',["1","2","3","5"])
        input["b"] = ('in2',["1","2","3","4"])
        input["c"] = ('in1',["2","3","4"])
        input["d"] = ('in1',["1","2","3","4","5"])

        all_companies_with_all_labels_dict,max_companies_dict,all_companies_max_labels= \
            CompaniesComparison.find_groups_with_size(input,3)

        self.assertIsItemContained(all_companies_with_all_labels_dict, (["d","a"],["2","3","1"]))
        self.assertIsItemContained(all_companies_with_all_labels_dict, (["d","c"],["2","3","4"]))
        self.assertIsItemContained(all_companies_max_labels, (["d","a"],["2","3","1","5"]))