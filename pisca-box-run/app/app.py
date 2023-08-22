# sys will allow us to access the passed arguments
import sys
import cmds

DOCKER = True

# sys.argv[0] access the first argument passed that is the python script name
print("\nFile or Script Name is :", sys.argv[0])

print(sys.argv)

# print arguments other than the file name
print("\nArguments passed:")
for i in range(1, len(sys.argv)):
   print(sys.argv[i])

# Lowercase operation on the passed arguments
which_version = "none"
which_xml = ""
for i in range(1, len(sys.argv)):
    print(sys.argv[i].lower())
    if i == 1:
        which_version = sys.argv[i].lower()
    elif i == 2:
        which_xml = sys.argv[i]
   

if which_version == "validate":
    print(cmds.run_validation("/project"))
elif which_version == "beast01":
    output = cmds.run_beast01(which_xml,DOCKER)
    print("--------------")
    print(output)
    #print(cmds.run_validation("/project/BEASTv1.8.4"))
    #print(cmds.run_validation("/project/tmp"))
elif which_version == "pisca01":
    output = cmds.run_pisca01(which_xml)
    print("--------------")
    print(output)
    print(cmds.run_validation("/project/PISCAv1.1"))
    print(cmds.run_validation("/project/tmp"))