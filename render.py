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
    template = None
    variables = None
    env = None

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
        data = yaml.load(open(self.VARS_DIR + "/" + self.variables), Loader=yaml.Loader)

        self.env.filters['yaml'] = self.yaml_filter
        self.env.globals["environ"] = lambda key: os.environ.get(key)
        self.env.globals["get_context"] = lambda: data

        template = self.env.get_template(self.template)
        sys.stdout.write(template.render(data))

        return template.render(data);


if __name__ == '__main__':
    render = Render(os.environ.get('TEMPLATE'), os.environ.get('VARIABLES'))
    render.rend_template(sys.argv[1:])
