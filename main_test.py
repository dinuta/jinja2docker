#!/usr/bin/env python3
import os
import unittest

import yaml

from entitities.render import Render


class RenderTestCase(unittest.TestCase):

    def test_json(self):
        os.environ['TEMPLATE'] = "json.j2"
        os.environ['VARIABLES'] = "json.json"
        r = Render(os.environ['TEMPLATE'], os.environ['VARIABLES'])

        template = yaml.load(r.rend_template("dummy"), Loader=yaml.Loader)
        with open(r.VARS_DIR + "/" + r.variables, closefd=True) as f:
            data = yaml.load(f, Loader=yaml.Loader)
        self.assertEqual(template.get("os"), data.get("os"), )
        self.assertEqual(template.get("version"), data.get("version"))
        self.assertEqual(template.get("installed_apps"), data.get("installed_apps"))

    def test_yml(self):
        os.environ['TEMPLATE'] = "yml.j2"
        os.environ['VARIABLES'] = "yml.yml"
        r = Render(os.environ['TEMPLATE'], os.environ['VARIABLES'])

        template = yaml.load(r.rend_template("dummy"), Loader=yaml.Loader)
        with open(r.VARS_DIR + "/" + r.variables, closefd=True) as f:
            data = yaml.load(f, Loader=yaml.Loader)
        self.assertEqual(template, data)


if __name__ == '__main__':
    unittest.main()
