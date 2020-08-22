#!/usr/bin/env python3
import unittest

import yaml

from entities import render
from entities.render import Render


class RenderTestCase(unittest.TestCase):

    def test_json(self):
        template_path = "./inputs/templates/json.j2"
        variables_path = "./inputs/variables/json.json"
        r = Render(template_path=template_path, variables_path=variables_path)

        rendered_data = yaml.safe_load(r.rend_template())
        with open(r.variables_path, closefd=True) as f:
            data = yaml.safe_load(f)
        self.assertEqual(rendered_data, data)

    def test_yml(self):
        template_path = "./inputs/templates/yml.j2"
        variables_path = "./inputs/variables/yml.yml"
        r = Render(template_path=template_path, variables_path=variables_path)

        rendered_data = yaml.safe_load(r.rend_template())
        with open(r.variables_path, closefd=True) as f:
            data = yaml.safe_load(f)
        self.assertEqual(rendered_data, data)

    def test_main_no_parameters(self):
        try:
            render.main()
        except Exception as e:
            self.assertIsInstance(e, Exception)


if __name__ == '__main__':
    unittest.main()
