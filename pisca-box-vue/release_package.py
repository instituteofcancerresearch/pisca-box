import __init__ # noqa: F401
import tests.runner as test
import os
import subprocess
# This file runs tests and builds the release
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
print("Current working directory is now:", os.getcwd())

version = "v08"
name = "pisca-vue"
docker = "rachelicr"
docker_no_tag = f"{docker}/{name}"
docker_latest = f"{docker}/{name}:latest"
docker_versioned = f"{docker}/{name}:{version}"    

## WHICH STAGES TO RUN ##
test_build, test_regression, build_docker,upload_docker = True,True,True,False
 

def run_commands(cmd_set):
    for cmd_one in cmd_set:
        print("##################################################################################")
        print(cmd_one)
        print("----------------------------------------------------------------------------------")
        try:            
            result = subprocess.run(cmd_one,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True,).stdout.decode('utf-8')            
            print(result.strip())
        except Exception as e:
            print("Failed to run", cmd_one,str(e),"!")
            return False
    return True

#######################################################
cmd_set_test = []        
cmd_set_test.append("pytest")
cmd_set_test.append("ruff --format=github --select=E9,F63,F7,F82 --target-version=py37 .")
cmd_set_test.append("ruff --format=github --target-version=py37 .")

cmd_set_build = []        
cmd_set_build.append(f"docker build -t {name} .")

cmd_set_upload = []
cmd_set_upload.append(f"docker tag {name} {docker_no_tag}")
cmd_set_upload.append(f"docker tag {name} {docker_versioned}")    
cmd_set_upload.append(f"docker push {docker_no_tag}")
cmd_set_upload.append(f"docker push {docker_versioned}")


#####################################################
if test_build:    
    ok = run_commands(cmd_set_test)
#####################################################
if test_regression and ok:
    # Run regression tests
    ok = test.run_regression()
    if ok:
        print("All regression tests passed, commencing docker builds...")
#####################################################
if build_docker and ok:    
    ok = run_commands(cmd_set_build)
#####################################################
if upload_docker and ok:    
    ok = run_commands(cmd_set_upload)


    




