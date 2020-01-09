#!/usr/bin/env python3

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import os
import jinja2
import sys
import yaml


class Render:
    TEMPLATES_DIR = os.environ.get('TEMPLATES_DIR')
    VARS_DIR = os.environ.get('VARS_DIR')

    def __init__(self, template=None, variables=None):
        self.template = template
        self.variables = variables
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.TEMPLATES_DIR),
            extensions=['jinja2.ext.autoescape', 'jinja2.ext.do', 'jinja2.ext.loopcontrols', 'jinja2.ext.with_'],
            autoescape=True,
            trim_blocks=True)

    def yaml_filter(self, value):
        return yaml.dump(value, Dumper=yaml.RoundTripDumper, indent=4)

    def env_override(self, value, key):
        return os.getenv(key, value)

    def rend_template(self, argv):
        with open(self.VARS_DIR + "/" + self.variables, closefd=True) as f:
            data = yaml.safe_load(f)

        self.env.filters['yaml'] = self.yaml_filter
        self.env.globals["environ"] = lambda key: os.environ.get(key)
        self.env.globals["get_context"] = lambda: data

        try:
            template = self.env.get_template(self.template).render(data)
        except Exception as e:
            raise e
        sys.stdout.write(template)

        return template
