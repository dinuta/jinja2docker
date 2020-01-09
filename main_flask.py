#!/usr/bin/env python3

from rest.render_flask_app import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
