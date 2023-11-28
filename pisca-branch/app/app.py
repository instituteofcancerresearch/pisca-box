# sys will allow us to access the passed arguments
import sys
import cmds as cmd


# sys.argv[0] access the first argument passed that is the python script name

# print arguments other than the file name
print("\nArguments passed:")
for i in range(0, len(sys.argv)):
   print(sys.argv[i], end=" ")

# The first param passed in must be the xml file
# There are 3 fixed params that we will def have and do not need to be added again
params = ["-beagle_off", "-working", "-overwrite"]
which_xml = ""
for i in range(1, len(sys.argv)):
    print(sys.argv[i])
    if i == 1:
        which_xml = sys.argv[i]
    else:
        param = sys.argv[i]                
        if param not in params:
            params.append(param)   

if which_xml == "validate":
    print(cmd.run_validation(["/project","/mnt"]))
else:    
    output = cmd.run_beast(which_xml,params)
    print("--------------")
    print(output)
