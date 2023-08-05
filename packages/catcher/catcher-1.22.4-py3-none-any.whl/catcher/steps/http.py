import json
import os
import re
from typing import Union

import requests
from requests import request

from catcher.steps.step import Step, update_variables
from catcher.utils.file_utils import read_file
from catcher.utils.logger import debug
from catcher.utils.misc import fill_template, fill_template_str


class Http(Step):
    """
    :Input:

    :<method>: http method. See https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html for details

    - headers: Dictionary with custom headers. *Optional*
    - url: url to call
    - response_code: Code to await. Use 'x' for a wildcard or '-' to set a range between 2 codes.
                     *Optional* default is 200.
    - body: body to send (only for methods which support it).
    - body_from_file: File can be used as data source. *Optional* Either `body` or `body_from_file` should present.
    - verify: Verify SSL Certificate in case of https. *Optional*. Default is true.
    - should_fail: true, if this request should fail, f.e. to test connection refused. Will fail the test if no errors.

    :Examples:

    Put data to server and await 200-299 code
    ::

        http:
          put:
            url: 'http://test.com?user_id={{ user_id }}'
            body: {'foo': bar}
          response_code: 2XX

    Put data to server and await 201-3XX code
    ::

        http:
          put:
            url: 'http://test.com?user_id={{ user_id }}'
            body: {'foo': bar}
          response_code: 201-3xx

    Post data to server with custom header
    ::

        http:
          post:
            headers: {Content-Type: 'application/json', Authorization: '{{ token }}'}
            url: 'http://test.com?user_id={{ user_id }}'
            body: {'foo': bar}

    Post file to remote server
    ::

        http:
          post:
            url: 'http://test.com'
            body_from_file: "data/answers.json"

    SSL without verification
    ::

        http:
          post:
            url: 'https://my_server.de'
            body: {'user':'test'}
            verify: false

    Json body from a variable:
    ::

        http:
          post:
            url: 'http://test.com?user_id={{ user_id }}'
            body: '{{ var |tojson }}'


    Test disconnected service:
    ::

        steps:
        - docker:
            disconnect:
                hash: '{{ my_container }}'
        - http:
            get:
                url: '{{ my_container_url }}'
                should_fail: true
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        method = Step.filter_predefined_keys(kwargs)  # get/post/put...
        self.method = method.lower()
        conf = kwargs[method]
        self.url = conf['url']
        self.headers = conf.get('headers', {})
        self.body = None
        self.verify = conf.get('verify', True)
        self._should_fail = conf.get('should_fail', False)
        if not self.verify:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.code = conf.get('response_code', 200)
        if self.method != 'get':
            self.body = conf.get('body', None)
            if self.body is None:
                self.file = conf['body_from_file']

    @update_variables
    def action(self, includes: dict, variables: dict) -> Union[tuple, dict]:
        url = fill_template(self.url, variables)
        r = None
        try:
            r = request(self.method, url, **self._form_request(url, variables))
            if self._should_fail:  # fail expected
                raise RuntimeError('Request expected to fail, but it doesn\'t')
        except requests.exceptions.ConnectionError as e:
            debug(str(e))
            if self._should_fail:  # fail expected
                return variables
        debug(r.text)
        if self.__check_code(r.status_code, self.code):
            raise RuntimeError('Code mismatch: ' + str(r.status_code) + ' vs ' + str(self.code))
        try:
            response = r.json()
        except ValueError:
            response = r.text
        return variables, response

    def _form_request(self, url, variables: dict) -> dict:
        headers = dict([(fill_template_str(k, variables), fill_template_str(v, variables))
                        for k, v in self.headers.items()])
        rq = dict(verify=self.verify, headers=headers)
        isjson, body = self.__form_body(variables)
        debug('http ' + str(self.method) + ' ' + str(url) + ', ' + str(headers) + ', ' + str(body))
        content_type = self.__get_content_type(headers)
        if isjson or isinstance(body, dict):  # contains tojson or dict supplied
            if isinstance(body, dict) and content_type == 'application/json':
                # json body formed manually via python dict
                rq['json'] = body
            else:  # json string or form-data dict
                rq['data'] = body
        else:  # raw body (or body is None)
            rq['data'] = body
        return rq

    @staticmethod
    def __get_content_type(headers):
        content_type = headers.get('Content-Type')
        if content_type is None:
            content_type = headers.get('content-type')
        return content_type

    def __form_body(self, variables) -> str or dict:
        if self.method == 'get':
            return False, None
        body = self.body
        if body is None:
            resources = variables['RESOURCES_DIR']
            body = read_file(fill_template_str(os.path.join(resources, self.file), variables))
        if isinstance(body, dict):  # dump body to json to be able fill templates in
            body = json.dumps(body)
        isjson = 'tojson' in body
        return isjson, fill_template(body, variables, isjson=isjson)

    @staticmethod
    def __check_code(got: int, expected):
        expected_str = str(expected).lower()
        if '-' in str(expected_str):  # range
            [e_from, e_to] = expected_str.split('-')
            return not (int(e_from.replace('x', '0')) <= got <= int(e_to.replace('x', '9')))
        if 'x' in expected_str:  # regexp
            expected_str = expected_str.replace('x', '.')
        p = re.compile(expected_str)
        return p.match(str(got)) is None
