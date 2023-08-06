# Cloudmesh cmsd

Cloudmesh cmsd is a command to run cloudmesh in a container regardles of
the OS. Thus it is extreemly easy to install and use.

cmsd will however use locally installed keys in `~/.ssh` and cloud
configurations stored in `~/.cloudmesh/cloudmesh.yaml`. The yaml file
will be created upon first call of cmsd if it is not available.

## How to use *cmsd*

Important. You must have cms in debug off mode. to use the cmsd command

```
cms debug off
```

### Prerequesites

* Docker
* python 3.8 or newer
* We strongle recommended to use a python virtual environment
* Install *cloudmesh-installer* by following the documentation in 
  the [Cloudmesh manual](https://cloudmesh.github.io/cloudmesh-manual/installation/install.html#installation-of-cloudmesh-source-install-for-developers)

### User instalation

Please use a python virtualenv as to not interfere with your system python.
Activate your python venv. Next just call

    pip install cloudmesh-cmsd
    
This will install a command `cmsd` in your environment that you can use
as in place replacement for the cms command.

The containers are called

- `cloudmesh-cms` 
- `cloudmesh-mongo` 


```bash
$ pip install cloudmesh-cmsd
```


## Developer Source install	

For developers it can be installed in an easy fashion with	

    python3.8 -m venv ~/ENV3
    source ~/ENV3/bin/activate
    mkdir cm	
    cd cm	
    pip install cloudmesh-installer -U	
    cloudmesh-installer git clone cmsd	
    cloudmesh-installer git install cmsd	

Now you can use the command 	

    cmsd help	
    ...
    cmsd --setup

The source code is contained in 	

    cloudmesh-cmsd


### cmsd setup 

To run cmsd, you would need a configuration directory that is mounted into the container.
Let us call this `CLOUDMESH_CONFIG_DIR`. Set `CLOUDMESH_CONFIG_DIR` as an environment variable. 

For Unix:
```
> export CLOUDMESH_CONFIG_DIR=<path to CLOUDMESH_HOME_DIR>
```

For Windows:
```
> set CLOUDMESH_CONFIG_DIR=<path to CLOUDMESH_HOME_DIR>
```

> NOTE: 
> - `CLOUDMESH_CONFIG_DIR` path must not have in any spaces.
> - Clarification for Windows users: 
>  - For example `C:\.cloudmesh` will work, so does 
> `C:\Users\gregor\.cloudmesh`, but not `C:\Users\gregor von Laszewski\.cloudmesh`)
>   - Make sure that the drive of the `CLOUDMESH_CONFIG_DIR` is granted file 
>     access in Docker settings

Run setup. If you are running setup on an empty `CLOUDMESH_CONFIG_DIR`,  you 
will be asked to key in some details that are required for the setup, such as 
profile details, Mongo DB credentials, etc. 

```  
> cmsd --setup 
```

Run the following command to see if the `cloudmesh-cms-container` is running! 
Additionally, check `CLOUDMESH_CONFIG_DIR` contains the `cloudmesh.yaml` file. 

```
> cmsd --ps
```

Run the following to verify if the configurations you entered have been 
properly reflected in the `cloudmesh.yaml` file. 

```
> cmsd config cat
```

### cmsd usages 

- To stop the containers, use `cmsd --stop`. 
- To start/restart the containers, use `cmsd --start`. 
- To clean the containers (remove stopped containers), use `cmsd --clean`. 
- To log into the running `cloudmesh-cms-container`, use `cmsd --shell`. 


### MongoDB and Mongo client connections  

cmsd is running an official MongoDB container from Docker Hub. Refer [here](https://hub.docker.com/_/mongo).

Mongo server container is bound to `127.0.0.1:27071` port. Therefore you can use 
any Mongo client to explore the database by connecting to this port. 

### Example usecase - Creating a vm in AWS 

Create an AWS account and add the authentication information in the 
`CLOUDMESH_HOME_DIR/cloudmesh.yaml` file. Refer [Cloudmesh Manual - AWS](https://cloudmesh.github.io/cloudmesh-manual/accounts/aws.html)

Set cloud to `aws`

```
> cmsd set cloud=aws 
```

Set AWS key name 

```
> cmsd set key=<key name> 
```

Boot a vm with the default config

```
>  cmsd vm boot 
```

## Manual Page

```bash
Usage:
        cmsd --help
        cmsd --setup
        cmsd --clean
        cmsd --version
        cmsd --update
        cmsd --start
        cmsd --stop
        cmsd --ps
        cmsd --gui
        cmsd --shell
        cmsd COMMAND... [--refresh]
        cmsd


  This command passes the arguments to a docker container
  that runs cloudmesh.

  Arguments:
      COMMAND the commands we bass along

  Description:

    cmsd --help

        prints this manual page

    cmsd --setup

        downloads the source distribution, installs the image locally

    cmsd --clean

        removes the container form docker

    cmsd --version

        prints out the verison of cmsd and the version of the container

    cmsd --gui
        runs cloudmesh gui on the docker container

    cmsd --update

        gets a new container form dockerhub

    cmsd COMMAND

        The command will be executed within the container, just as in
        case of cms.

    cmsd

        When no command is specified cms will be run in interactive
        mode.
```
