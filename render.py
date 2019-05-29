#!/usr/bin/env python3

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import os
import jinja2
import sys
import yaml

class Render:

    def __init__(self):
        pass

    TEMPLATES_DIR = os.environ.get('TEMPLATES_DIR')
    TEMPLATE = os.environ.get('TEMPLATE')
    VARS_DIR = os.environ.get('VARS_DIR')
    VARIABLES = os.environ.get('VARIABLES')

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATES_DIR),
        extensions=['jinja2.ext.autoescape', 'jinja2.ext.do', 'jinja2.ext.loopcontrols', 'jinja2.ext.with_'],
        autoescape=True,
        trim_blocks=True)


    def yamlFilter(self, value):
        return yaml.dump(value, Dumper=yaml.RoundTripDumper, indent=4)

    def env_override(self, value, key):
        return os.getenv(key, value)


    def rend_template(self, argv):
        data = yaml.load(open(self.VARS_DIR + "/" + self.VARIABLES), Loader=yaml.Loader)

        self.env.filters['yaml'] = self.yamlFilter
        self.env.globals["environ"] = lambda key: os.environ.get(key)
        self.env.globals["get_context"] = lambda: data

        template = self.env.get_template(self.TEMPLATE)
        sys.stdout.write(template.render(data))

if __name__ == '__main__':
    render = Render()
    render.rend_template(sys.argv[1:])
