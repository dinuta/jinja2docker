import os
import sys

from entitities.render import Render

if __name__ == '__main__':
    render = Render(os.environ.get('TEMPLATE'), os.environ.get('VARIABLES'))
    render.rend_template(sys.argv[1:])
