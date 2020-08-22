#!/usr/bin/env python3

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import sys

import yaml
from jinja2 import Template


class Render:
    def __init__(self, template_path=None, variables_path=None):
        self.template_path = template_path
        self.variables_path = variables_path

    def rend_template(self):
        with open(self.variables_path, closefd=True) as f:
            data = yaml.safe_load(f)
        with open(self.template_path, closefd=True) as f:
            template = f.read()

        try:
            rendered = Template(template).render(data)
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
