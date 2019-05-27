# Jinja2 templating with Docker

DockerHub: https://cloud.docker.com/repository/docker/dinutac/jinja2docker  


The key things to remember are:   
* Mount the directory containing your template(s) to the container's /data directory
* Mount the directory containing your variables file(s) directory
* Pass needed env vars (any number)
* In jour jinja2 template get OS env and your inserted env vars with ```OS_ENV.<your_env_var>```

### Supported formats
- json
- yaml

### Synthax
docker run -i   -v <your_jinja2_template_folder>:/data \ 
-v <your_jinja2_variables_file_folder>:/variables  \
-e TEMPLATE=<name_of_your_j2_template>.j2 -e VARIABLES=<name_of_your_variable_file> \
-e <list_of_your_env_vars> cdinuta/jinja2:latest > **<your_output_file>**

Example: 
```
docker run -i   -v C:\Users\cdinuta\IdeaProjects\jinja2docker\templates:/data \
-v C:\Users\cdinuta\IdeaProjects\jinja2docker\variables:/variables   \
-e TEMPLATE=standalone.j2 -e VARIABLES=variables.yml -e DATABASE=mysql56 cdinuta/jinja2:latest > docker-compose.yml
```

### Example template ```json-template.j2```
``` txt
Os: {{os}}
Flavour: {{flavour}}
   
Path: {{OS_ENV.PATH}}
```

### Example json variables file ```variables.json```
```json
{
  "os" : "Linux",
  "flavour": "CentOS"
}
```

### Additional flexibility & base image inheritance
- ! Verify the Dockerfile in order to check the python packages installed inside.
- Override the ```render.py``` file (you must use this file name) in /home/dev/bin/ in order to execute your own logic.
- If no support exists in the current image use this as base image and add your python packages using pip commands.

### Limitations
- big chunks of yaml data can't be pasted into the jinja2 template files. Currently no yaml filter exists in jinja2.
 Custom yaml filter was implemented and 2 variants were tested:  
```yaml.dump(value, sys.stdout, Dumper=yaml.RoundTripDumper, indent=4)``` tested, keeps indentations but does not glue yaml chunk where needed)  
```yaml.dump(value, Dumper=yaml.RoundTripDumper, indent=4)``` - this is the current implementation, but does not keep indentations for large chunks of yaml)  

The recommendation is either paste selectively smaller chunks of yaml or use json whenever possible.