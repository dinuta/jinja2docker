FROM alpine:3.11

# Install python3 and other deps
RUN apk add --no-cache python3
RUN pip3 install pip==20.1.1 setuptools==47.1.1 --no-cache
RUN apk add --no-cache build-base sshpass

# Create folders
RUN mkdir /templates/
RUN mkdir /variables/

# Expose some volumes
VOLUME ["/templates"]
VOLUME ["/variables"]

# Set needed env vars
ENV SCRIPTS_DIR /scripts
ENV TEMPLATES_DIR /templates
ENV VARS_DIR /variables
ENV TEMPLATE docker-compose.j2
ENV VARIABLES variables.yml

# Copy extra scripts: embedded render and main flask service
COPY entities/render.py $SCRIPTS_DIR/entities/render.py
COPY main_flask.py $SCRIPTS_DIR/main_flask.py
COPY requirements.txt $SCRIPTS_DIR/requirements.txt

RUN chmod +x $SCRIPTS_DIR/entities/render.py
RUN chmod +x $SCRIPTS_DIR/main_flask.py

WORKDIR /templates

RUN pip3 install -r $SCRIPTS_DIR/requirements.txt

ENTRYPOINT ["jinja2"]
