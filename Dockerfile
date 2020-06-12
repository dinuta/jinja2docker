FROM alpine:3.11

# Install python3 and other deps
RUN apk add --no-cache python3
RUN pip3 install --upgrade pip==20.1.1 setuptools==47.1.1 --no-cache
RUN apk add --no-cache build-base sshpass

# Create folders
RUN mkdir /data/
RUN mkdir /variables/

# Expose some volumes
VOLUME ["/data"]
VOLUME ["/variables"]

# Set needed env vars
ENV SCRIPTS_DIR /scripts
ENV TEMPLATES_DIR /data
ENV VARS_DIR /variables
ENV TEMPLATE docker-compose.j2
ENV VARIABLES variables.yml

# Copy extra scripts: embedded render and main flask service
COPY entities/render.py $SCRIPTS_DIR/entities/render.py
COPY main_flask.py $SCRIPTS_DIR/main_flask.py

RUN chmod +x $SCRIPTS_DIR/entities/render.py
RUN chmod +x $SCRIPTS_DIR/main_flask.py

WORKDIR /data

RUN pip3 install -r $SCRIPTS_DIR/requirements.txt

ENTRYPOINT ["jinja2"]
