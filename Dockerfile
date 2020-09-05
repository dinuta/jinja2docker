FROM alpine:3.11

# Install python3 and other deps
RUN apk add --no-cache python3
RUN pip3 install pip==20.2.2 --no-cache

# Create folders
RUN mkdir /templates/
RUN mkdir /variables/

# Set needed env vars
ENV SCRIPTS_DIR /scripts
ENV TEMPLATES_DIR /templates

# Copy extra scripts: embedded render
COPY entities/render.py $SCRIPTS_DIR/entities/render.py

RUN chmod +x $SCRIPTS_DIR/entities/render.py
RUN pip3 install jinja2-cli[yaml,toml,xml]==0.7.0

ENTRYPOINT ["jinja2"]
