# TestRail Utility for python3
#

import json
import settings
import sys
from testrail import APIClient

DEFAULT_RESULT_PARSER = "JunitXMLParser"


class TestRailUtil:
    def __init__(self, username='', password='', url=''):
        self.username = username
        self.password = password
        self.url = url

        if not username:
            self.username = settings.USR
        if not password:
            self.password = settings.PWD
        if not url:
            self.url = settings.URL

        client = APIClient(self.url)
        client.user = self.username
        client.password = self.password

        self.client = client
        self.parser = None

    def pretty(self, payload):
        print(json.dumps(payload, sort_keys=True,
                         indent=4, separators=(',', ':')))

    def add_case(self, section_id, **kwargs):
        """Creates a new test case."""
        fields = {}

        for key in kwargs:
            fields[key] = kwargs[key]

        req = self.client.send_post('add_case/' + str(section_id), data=fields)
        return req

    def import_test_cases(self, result_parser, **kwargs):
        def spec(parser):
            imp_path = 'test_result_parser.%s' % parser
            mod_str, dot, cls_str = imp_path.rpartition('.')
            __import__(mod_str)
            try:
                spec_cls_obj = getattr(sys.modules[mod_str], cls_str)
                return spec_cls_obj(**kwargs)
            except AttributeError:
                raise ImportError('No such class %s' % imp_path)

        self.parser = spec(result_parser)
        print(*self.parser.get_test_cases(), sep='\n')


if __name__ == "__main__":
    username = "joe"
    password = "test"
    url = "url"
    test_file = "test-results/sample-junit.xml"
    util = TestRailUtil(username, password, url)
    util.import_test_cases(DEFAULT_RESULT_PARSER, result_file=test_file)
    # mile_stone = util.create_mile_stone()
    # plan_id = util.create_test_plan()
    # util.add_results()
