from json_helper import JsonHelper
from companies_comparison import CompaniesComparison


MIN_CRITERIA_NUM = 4

with open('companiesComparisonWidgetInput.json', 'r') as content_file:
    content = content_file.read()

company_to_labels = JsonHelper.convert_companies_json_to_dictionary(content)

all_companies_with_all_labels_dict,max_companies_dict,all_with_max_dict = \
    CompaniesComparison.find_groups_with_size(company_to_labels, MIN_CRITERIA_NUM)

print "All combinations of all companies with all combinations of shared creterias of size %s:" % MIN_CRITERIA_NUM
print JsonHelper.convert_companies_to_labels_list_to_json(all_companies_with_all_labels_dict) + '\n'

print 'All the Maximum number of companies that have a shared creteria of %s:' % MIN_CRITERIA_NUM
print JsonHelper.convert_companies_to_labels_list_to_json(max_companies_dict) + '\n'

print 'All the Companies combinations with their max shared cretierias that have a minimum shared creteria of %s:' % MIN_CRITERIA_NUM
print JsonHelper.convert_companies_to_labels_list_to_json(all_with_max_dict) + '\n'