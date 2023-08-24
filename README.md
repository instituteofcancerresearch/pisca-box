# Pisca-Box: A containerisation of PISCA

## Summary
Pisca-Box consists of 2 containerised applications to run PISCA.

pisca-box is the command line interface that gives identical functionality and inputs as PISCA, but being containersied is operating system independent and through singularity can be run on the command line from alma.

pisca-vue is a locally hosted streamlit application to give a user-friendly interface for xml generation, help and instructions. Also containerised this is intended to provide both a way to generate xml and also form a platform for creating tutorials and help.

## pisca-box
### docker
Pull the container – either explicitly or it will pull the first time you run it
```
$ docker pull rachelicr/pisca-box
```

No tag is latest, or pull a specific version:
```
$ docker pull rachelicr/pisca-box:v01
```

A simple validate command checks it has worked and displays the local (container’s) file system
```
$ docker run rachelicr/pisca-box validate
$ docker run rachelicr/pisca-box:v01 validate
```

To run pisca-box, you need to pass the directory of your xml file, and then the xml file itself separately as the first input command. Then proceed with any optional parameters that you want to pass to beast. There are 3 hardcoded parameters that will be always be included and you do not need to enter:
•	-beagle_off – this version of pisca cannot use beagle, it is piscav1.1 and beastv1.8.4
•	-working – forces the logs to be the xml directory so the container can communicate back.
•	-overwrite – each existing logfile is prepended with an underscore anyway.

The call to pisca-box thus looks like this, where anything not bold must stay exactly as it is, and anything bold must be changed as per your own inputs. The directory /project/xml is the internal directory of the container to which we map – it cannot be changed.

$ docker run -v **/path/to/my/input/dir**:/project/xml rachelicr/pisca-box **myinput.xml param1 param2**


An example, where my xml files are in the directory ~/dev/beast-icr/xml – validation.xml is the pisca validation file.

$ docker run -v **~/dev/beast-icr/xml**:/project/xml rachelicr/pisca-box **validation.xml**



### singularity
Pull the container – either explicitly or it will pull the first time you run it
```
$ singularity pull docker://rachelicr/pisca-box
```

No tag is latest, or pull a specific version:
```
$ singularity pull docker://rachelicr/pisca-box:v01
```

A simple validate command checks it has worked and displays the local (container’s) file system
```
$ singularity run docker://rachelicr/pisca-box validate
$ singularity run docker://rachelicr/pisca-box:v01 validate
```

The mapping of file systems uses -B instead of -v so the format of the input is as below, with the validation example.

$ singularity run -B **/path/to/my/input/dir**:/project/xml docker://rachelicr/pisca-box** myinput.xml params…**

$ singularity run -B **~/dev/beast-icr/xml**:/project/xml docker://rachelicr/pisca-box **validation.xml**





