from abc import ABC, abstractmethod
from xml.dom import minidom


class AbstractParser(ABC):
    def __init__(self, value):
        self.value = value
        super().__init__()

    @abstractmethod
    def get_test_cases(self):
        raise NotImplementedError

    @abstractmethod
    def get_test_results(self):
        raise NotImplementedError

    @abstractmethod
    def get_test_suites(self):
        raise NotImplementedError


class JunitXMLParser(AbstractParser):
    test_cases = []
    test_suites = []

    def __init__(self, **kwargs):
        self.result_file = kwargs['result_file']

    def get_test_cases(self):
        xmldoc = minidom.parse(self.result_file)
        test_cases = xmldoc.getElementsByTagName('testcase')
        for test_case in test_cases:
            test_case_attributes = {}
            suite_name = test_case.parentNode.attributes['name'].value
            for attr in test_case.attributes.values():
                test_case_attributes[attr.name] = attr.value
                test_case_attributes["suitename"] = suite_name
            self.test_cases.append(test_case_attributes)
        return self.test_cases

    def get_test_results(self):
        print("test_results")

    def get_test_suites(self):
        xmldoc = minidom.parse(self.result_file)
        self.test_suites = xmldoc.getElementsByTagName('testsuite')
        return self.test_suites


class JenkinsApiResult(AbstractParser):
    # Uses the jenkins api to get results from artifacts
    def __init__(self, **kwargs):
        pass

    def get_test_suites(self):
        super().get_test_suite()

    def get_test_cases(self):
        super().get_test_cases()

    def get_test_results(self):
        super().get_test_results()


class CircleCiApiResult(AbstractParser):
    # Uses the cirle ci api to get results from artifacts
    def __init__(self, **kwargs):
        pass

    def get_test_suites(self):
        super().get_test_suite()

    def get_test_cases(self):
        super().get_test_cases()

    def get_test_results(self):
        super().get_test_results()


if __name__ == "__main__":
    test_file = "test-results/sample-junit.xml"
    util = JunitXMLParser(result_file=test_file)
    cases = util.get_test_cases()
    suites = util.get_test_suites()

    print(*cases, sep='\n')
    print("test suites now ======")
    print(*suites, sep='\n')
