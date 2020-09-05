#!/usr/bin/env python3

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import os
import sys

import jinja2
import yaml


class Render:
    TEMPLATES_DIR = os.environ.get('TEMPLATES_DIR') if os.environ.get('TEMPLATES_DIR') is not None else "/templates"

    def __init__(self, template_name=None, variables_path=None):
        self.template_name = template_name
        self.variables_path = variables_path
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.TEMPLATES_DIR),
            extensions=['jinja2.ext.autoescape', 'jinja2.ext.do', 'jinja2.ext.loopcontrols', 'jinja2.ext.with_'],
            autoescape=True,
            trim_blocks=True)

    def yaml_filter(value):
        return yaml.dump(value, Dumper=yaml.RoundTripDumper, indent=4)

    def rend_template(self):
        with open(self.variables_path, closefd=True) as f:
            data = yaml.safe_load(f)

        self.env.filters['yaml'] = self.yaml_filter
        self.env.globals["environ"] = os.environ

        try:
            rendered = self.env.get_template(self.template_name).render(data)
        except Exception as e:
            raise e

        return rendered


def main():
    min_args = 3
    if len(sys.argv) < min_args:
        raise Exception(
            "Error: Expecting at least {} args. Got {}, args={}".format(min_args, len(sys.argv), sys.argv))
    sys.stdout.write(Render(sys.argv[1], sys.argv[2]).rend_template())


if __name__ == '__main__':
    main()
