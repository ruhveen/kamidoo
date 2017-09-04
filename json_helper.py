import json


class JsonHelper(object):

    @staticmethod
    def convert_companies_json_to_dictionary(companies_json):

        companies_json = json.loads(companies_json)
        result = {}
        for company in companies_json["companiesEntities"]:
            result[company["EntityName"]] = [datapoint["Label"] for datapoint in company["DataPoints"] if "Label" in datapoint]

        return result

    @staticmethod
    def convert_companies_to_labels_list_to_json(list):

        result = {"comparisonGroups":[]}
        for companies_to_labels in list:
            result["comparisonGroups"].append({"companies":companies_to_labels[0],
                                               "comparisonCreteria":companies_to_labels[1]})

        return json.dumps(result)