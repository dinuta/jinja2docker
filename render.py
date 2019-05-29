#!/usr/bin/env python3

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import os
import jinja2
import sys
import yaml

TEMPLATES_DIR = os.environ.get('TEMPLATES_DIR')
TEMPLATE = os.environ.get('TEMPLATE')
VARS_DIR = os.environ.get('VARS_DIR')
VARIABLES = os.environ.get('VARIABLES')

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATES_DIR),
    extensions=['jinja2.ext.autoescape', 'jinja2.ext.do', 'jinja2.ext.loopcontrols', 'jinja2.ext.with_'],
    autoescape=True,
    trim_blocks=True)


def yamlFilter(value):
    return yaml.dump(value, Dumper=yaml.RoundTripDumper, indent=4)

def env_override(value, key):
    return os.getenv(key, value)


def render_template(argv):
    data = yaml.load(open(VARS_DIR + "/" + VARIABLES), Loader=yaml.Loader)

    env.filters['yaml'] = yamlFilter
    env.globals["environ"] = lambda key: os.environ.get(key)
    env.globals["get_context"] = lambda: data

    template = env.get_template(TEMPLATE)
    sys.stdout.write(template.render(data))

if __name__ == '__main__':
    render_template(sys.argv[1:])
