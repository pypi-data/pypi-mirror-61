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
* Install *cloudmesh-installer* by following the documentation in the [Cloudmesh manual](https://cloudmesh.github.io/cloudmesh-manual/installation/install.html#installation-of-cloudmesh-source-install-for-developers)


### cmsd installation 

- Activate the python virtual environment
- Clone `cloundmesh-cmsd` repository to a directory of your preference (we reccommend `~\cm`)

```
  cloudmesh-installer git clone cmsd
```

- Install cloudmesh-cmsd using cloudmesh-installer 

```
  cloudmesh-installer install cmsd
```

- Check if the installation succeded

```
cmsd --help
```

### cmsd initial setup 

To run cmsd, you would need a configuration directory that is mounted into the containee
Let us call this `CLOUDMESH_HOME_DIR`. The directory name must not have in a space in it. 

Clarification for Windows users: For example `C:\.cloudmesh` will work, so does
`C:\Users\gregor\.cloudmesh`, but not `C:\Users\gregor von Laszewski\.cloudmesh`

Please also note that in docker setup you need to select the drive C for file access.

Once you created the directory, you need to run the initial setup 

```  
> cmsd --setup <CLOUDMESH_HOME_DIR>
```

Next, run `cmsd --ps` to see if the `cloudmesh-cms-container` is running! 
Additionally, check `CLOUDMESH_HOME_DIR` contains the `cloudmesh.yaml` file. 

Now that the first phase of the setup succeded, let us set up mongodb with the cmsd container. You now need 
to setup a password for the MongoDB. 

```
> cmsd config set cloudmesh.data.mongo.MONGO_PASSWORD=<some password>
```

Run `cmsd --setup <CLOUDMESH_HOME_DIR>` **again** to complete the process. 

Check if both `cloudmesh-cms-container` and `cloudmesh-mongo-container` both are running, using `cmsd --ps`

You can check the `cloudmesh.yaml` file content by running, 

```
> cmsd config cat
```

### cmsd subsequent usages 

- To stop the containers, use `cmsd --stop`. 
- To start/restart the containers, use `cmsd --start`. 
- To clean the containers (remove stopped containers), use `cmsd --clean`. 
- To log into the running `cloudmesh-cms-container`, use `cmsd --shell`. 


### MongoDB and Mongo client connections  

cmsd is running an official MongoDB container from Docker Hub. Refer [here](https://hub.docker.com/_/mongo) and the mongo server instance is bound to the `127.0.0.1:27071` port. Therefore you can use any Mongo client to explore the database by connecting to this port. 

> NOTE:

> Unix - 
> At the setup, `CLOUDMESH_HOME_DIR/mongodb`  directory will be created and used as the data directory for mongo DB. We recommend that you ues `~/.cloudmesh` as `CLOUDMESH_HOME_DIR`. YOu can set it with 

> ```
> $ export CLOUDMESH_HOME_DIR=~/.cloudmesh
> ```

> Windows - 
> Docker windows directory mounting does not work properly with mongo container. See [here](https://github.com/docker/for-win/issues/2189). Hence, a docker volume will be mounted as the data directory. YOu could set is to a directory in your `C:` drive that you create, but it must not have a space in its name.


### Example usecase - Creating a vm in AWS 

- Create an AWS account and add the authentication information in the `CLOUDMESH_HOME_DIR/cloudmesh.yaml` file. Refer [Cloudmesh Manual - AWS](https://cloudmesh.github.io/cloudmesh-manual/accounts/aws.html)

- Set cloud to `aws`
```
  cmsd set cloud=aws 
```

- Set AWS key name 
```
  cmsd set key=<key name> 
```

- Boot a vm with the default config
```
  cmsd vm boot 
```

## End user deployment 

Please uese a python virtualenv as to not interfere with your system python.
Activate your python venv. Next just call

    pip install cloudmesh-cmsd
    
This will install a command `cmsd` in your environment that you can use
as in place replacement for the cms command.

The containers are called

* `cloudmesh/cms` 


## Developer Source install

For developers it can be installed in an easy fashion with

    mkdir cm
    cd cm
    pip install cloudmesh-installer -U
    cloudmesh-installer git clone cmsd
    cloudmesh-installer git install cmsd
 
Now you can use the command 

    cmsd help

The source code is contained in 

    cloudmesh-cmsd


## Manual Page

```bash

  Usage:
        cmsd --help
        cmsd --setup [CLOUDMESH_HOME_DIR]
        cmsd --clean
        cmsd --version
        cmsd --update
        cmsd --image
        cmsd --start
        cmsd --stop
        cmsd --ps
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

    cmsd --image

        list the container

    cmsd --setup [CLOUDMESH_HOME_DIR]

        Sets up cmsd 

    cmsd --clean

        removes the container form docker

    cmsd --version

        prints out the verison of cmsd and the version of the container

    cmsd --update

        gets a new container form dockerhub

    cmsd COMMAND

        The command will be executed within the container, just as in
        case of cms.

    cmsd

        When no command is specified cms will be run in interactive
        mode.

```
