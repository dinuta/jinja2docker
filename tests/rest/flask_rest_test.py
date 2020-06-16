#!/usr/bin/env python3
import unittest

import requests
import yaml
from flask import json
from parameterized import parameterized


class FlaskServerTestCase(unittest.TestCase):
    server = "http://127.0.0.1:8080"

    def test_env_endpoint(self):
        response = requests.get(self.server + "/env")
        body = response.json()
        self.assertGreaterEqual(len(body), 7)
        self.assertEqual(body.get('VARS_DIR'), "/variables")
        self.assertEqual(body.get('TEMPLATES_DIR'), "/templates")

    @parameterized.expand([
        ("json.j2", "json.json"),
        ("yml.j2", "yml.yml")
    ])
    def test_rend_endpoint_p(self, template, variables):
        response = requests.post(self.server + f"/render/{template}/{variables}")
        result = yaml.safe_load(response.text)
        self.assertEqual(len(result), 3)

    @parameterized.expand([
        ("json.j2", "doesnotexists.json"),
        ("yml.j2", "doesnotexists.yml")
    ])
    def test_rend_endpoint_doesnotexist(self, template, variables):
        expected = f"Exception([Errno 2] No such file or directory: \'/variables/{variables}\')"
        response = requests.post(self.server + f"/render/{template}/{variables}")
        self.assertEqual(expected, response.text)

    @parameterized.expand([
        ("doesnotexists.j2", "json.json"),
        ("doesnotexists.j2", "yml.yml")
    ])
    def test_rend_endpoint(self, template, variables):
        expected = f"Exception({template})"
        response = requests.post(self.server + f"/render/{template}/{variables}")
        self.assertEqual(expected, response.text)

    @parameterized.expand([
        ("standalone.j2", "variables.yml")
    ])
    def test_rendwithenv_endpoint(self, template, variables):
        payload = {'DATABASE': 'mysql56', 'IMAGE': 'latest'}
        headers = {'Content-type': 'application/json'}
        response = requests.post(self.server + f"/render/{template}/{variables}", data=json.dumps(payload),
                                 headers=headers)
        body = yaml.safe_load(response.text)
        self.assertEqual(len(body.get("services")), 2)
        self.assertEqual(int(body.get("version")), 3)


if __name__ == '__main__':
    unittest.main()
