# sys will allow us to access the passed arguments
import sys
import cmds

VERSION = "0.0.2"

print("Welcome to pisca-box version " + VERSION)

# sys.argv[0] access the first argument passed that is the python script name

# print arguments other than the file name
print("\nArguments passed:")
for i in range(0, len(sys.argv)):
   print(sys.argv[i], end=" ")

# The first param passed in must be the xml file
# There are 3 fixed params that we will def have and do not need to be added again
params = ["-beagle_off", "-working", "-overwrite"]
TEST_MODE = False
which_xml = ""
for i in range(1, len(sys.argv)):
    print(sys.argv[i])
    if i == 1:
        which_xml = sys.argv[i]
    else:
        param = sys.argv[i]        
        if param == "TEST_MODE":
            TEST_MODE = True
        elif param not in params:
            params.append(param)
   

if which_xml == "validate":
    print(cmds.run_validation(["/project","/project/xml","/mnt"]))
else:    
    output = cmds.run_beast(which_xml,params,TEST_MODE)
    print("--------------")
    print(output)
