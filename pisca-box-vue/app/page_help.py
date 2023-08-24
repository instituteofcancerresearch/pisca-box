import streamlit as st



def add_widgets():   
    #st.markdown('**Documentation for pisca-box-vue**')            
    st.markdown('**[pisca-box-vue](https://hub.docker.com/r/rachelicr/pisca-vue)**')
    st.markdown("_To run the containerised webapp pisca-box-vue_")
    st.code("""
            docker pull rachelicr/pisca-vue            
            docker run -p 8000:8501 rachelicr/pisca-vue            
            """)
    
    st.write("It is locally hosted on a port of your choice, in this case 8000. Open the app at [http://localhost:8000/](http://localhost:8000/)")
    
    st.markdown('**[pisca-box command-line](https://hub.docker.com/r/rachelicr/pisca-box)**')
    msg = "To communicate with the container's file system a drive must be mounted. "
    msg += "In this case the drive is :green[~/dev/beast-icr/xml], but should be the folder where your xml input file is. "
    msg += "The folder with the xml file is also used as the working directory, so the output files will be written to this folder."
    st.write(msg)  
    st.write("Docker and singularity use different inputs for the drive mapping :blue[-v] and :blue[-B] respectively.")
    st.write("The docker command is: docker run -v :green[/your/xml/dir]:/project/xml rachelicr/pisca-box :green[your.xml]")
    st.write("The singularity command is: singularity run -B :green[/your/xml/dir]:/project/xml docker://rachelicr/pisca-box :green[your.xml]")
    
    
    st.markdown("_Running the docker image from docker hub_")

    st.code("""
            docker pull rachelicr/pisca-box
            docker run rachelicr/pisca-box validate            
            docker run -v ~/dev/beast-icr/xml:/project/xml rachelicr/pisca-box testStrictClock.xml
            """)
    
    
    st.markdown("_Running the docker image from singularity hub_")
    st.code("""
            singularity pull docker://rachelicr/pisca-box
            singularity run docker://rachelicr/pisca-box validate            
            singularity run -B ~/dev/beast-icr/xml:/project/xml docker://rachelicr/pisca-box testStrictClock.xml
            """)
    
    with st.expander("All the beast command-line inputs"):
            st.code("""
                -verbose Give verbose XML parsing messages
                -warnings Show warning messages about BEAST XML file
                -strict Fail on non-conforming BEAST XML file
                -window Provide a console window
                -options Display an options dialog
                -working Change working directory to input file's directory
                -seed Specify a random number generator seed
                -prefix Specify a prefix for all output log filenames
                -overwrite Allow overwriting of log files
                -errors Specify maximum number of numerical errors before stopping
                -threads The number of computational threads to use (default auto)
                -java Use Java only, no native implementations
                -threshold Full evaluation test threshold (default 0.1)
                -beagle_off Don't use the BEAGLE library
                -beagle Use BEAGLE library if available (default on)
                -beagle_info BEAGLE: show information on available resources
                -beagle_order BEAGLE: set order of resource use
                -beagle_instances BEAGLE: divide site patterns amongst instances
                -beagle_CPU BEAGLE: use CPU instance
                -beagle_GPU BEAGLE: use GPU instance if available
                -beagle_SSE BEAGLE: use SSE extensions if available
                -beagle_SSE_off BEAGLE: turn off use of SSE extensions
                -beagle_cuda BEAGLE: use CUDA parallization if available
                -beagle_opencl BEAGLE: use OpenCL parallization if available
                -beagle_single BEAGLE: use single precision if available
                -beagle_double BEAGLE: use double precision if available
                -beagle_async BEAGLE: use asynchronous kernels if available
                -beagle_scaling BEAGLE: specify scaling scheme to use
                -beagle_delay_scaling_off BEAGLE: don't wait until underflow for scaling option
                -beagle_rescale BEAGLE: frequency of rescaling (dynamic scaling only)
                -mpi Use MPI rank to label output
                -mc3_chains number of chains
                -mc3_delta temperature increment parameter
                -mc3_temperatures a comma-separated list of the hot chain temperatures
                -mc3_swap frequency at which chains temperatures will be swapped
                -load_dump Specify a filename to load a dumped state from
                -dump_state Specify a state at which to write a dump file
                -dump_every Specify a frequency to write a dump file
                -citations_file Specify a filename to write a citation list to
                -version Print the version and credits and stop
                -help Print this information and stop
                """)

                
    st.markdown("BEAST help can be found in the [Beast Community](http://beast.community/)")