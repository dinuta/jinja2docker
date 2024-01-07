FROM alpine:3.19.0

# Set env vars
ENV TEMPLATES_DIR /templates
ENV VARIABLES_DIR /variables


# Create folders
RUN mkdir $TEMPLATES_DIR
RUN mkdir $VARIABLES_DIR

RUN apk add --no-cache py3-pip

RUN pip3 install jinja2-cli[yaml,toml,xml,hjson,json5]==0.8.2 --break-system-packages

ENTRYPOINT ["jinja2"]
