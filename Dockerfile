FROM alpine:3.17.3

# Install python3 and other dependencies
RUN apk add --no-cache python3 py3-pip

# Create folders
RUN mkdir /templates/
RUN mkdir /variables/

# Set needed env vars
ENV SCRIPTS_DIR /scripts
ENV TEMPLATES_DIR /templates

# Copy extra scripts: embedded render
COPY entities/render.py $SCRIPTS_DIR/entities/render.py

RUN chmod +x $SCRIPTS_DIR/entities/render.py
RUN pip3 install jinja2-cli[yaml,toml,xml,hjson,json5]==0.8.2

ENTRYPOINT ["jinja2"]
