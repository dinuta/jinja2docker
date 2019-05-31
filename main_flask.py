#!/usr/bin/env python3

from rest.render_flask_app import init_app, app

if __name__ == "__main__":
    init_app(app)
    app.run(host='0.0.0.0')
