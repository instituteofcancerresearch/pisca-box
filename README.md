Institute of Cancer Research [Scientific Software Group](https://www.icr.ac.uk/our-research/facilities/scientific-computing-service)  
Please contact the [scientific software team](mailto://scsoftware@icr.ac.uk) for support or information.  
Please raise issues here in github using [New issue](https://github.com/instituteofcancerresearch/pisca-box/issues)

# Pisca-Box

Welcome to **pisca-box**. This application is a user-friendly interface to the pisca-beast plug-in for [BEAST](http://beast.community/) (Bayesian Evolutionary Anaylsis Sampling Trees). It has been created at the Institute of Cancer Research in collaboration with Arizona State University.

The pisca-beast plug-in adapts the BEAST MCMC calculations to apply to cancer evolution. The pisca-beast plug-in was created by Diego Mallo and is available on [github](https://github.com/adamallo/PISCA).

This PISCA-BOX repo is containerised and available on [docker hub](https://hub.docker.com/r/icrsc/pisca-box)  Using the commands below you can pull it from docker and run it as a locally hosted web application.  
If you don't have docker, there are instructions on how to install it [here](https://docs.docker.com/engine/install/)
```
docker pull icrsc/pisca-box
docker run -p 8000:8501 icrsc/pisca-box
```
It is locally hosted on a port of your choice, in this case 8000. Open the app at [http://localhost:8000/](http://localhost:8000/)


        
#### Applications available in pisca-box

The BEAST eco-system includes command line utiltities and java gui applications, two of which are exposed here in **pisca-box**    
- **pisca-box** is the main calculation engine, running the BEAST command-line utility with the PISCA java plug-in.
- **beauti-box**: beauti is the java gui application for creating xml files for the beast application. In beauti-box you can create pisca-specific xml files, with a helpful guide to the inputs.
    
#### Further applications            
**pisca-run** is also a [containerised command line image](https://hub.docker.com/r/icrsc/pisca-run) that can be run locally or on an HPC cluster for heavier-duty use.