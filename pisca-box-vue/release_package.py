import __init__ # noqa: F401
import tests.runner as test
import os
import subprocess

# This file runs tests and builds the release
# Manual regression detailed here: readme_regression.md

########################## WHICH STAGES TO RUN ####################################
#### CLEAN ###
pre_clean_up = 1
post_clean_up = 1
#### TEST ###
test_build = 1
build_run = 0
test_regression = 0
#### BUILD ###-
build_vue = 0
tag_dockers = 0
#### RELEASE ###
upload_dockers = 0

########################## VERSION AND NAMES ######################################
version = "v02"
name_run = "pisca-box-run"
name_vue = "pisca-box-vue"
docker = "rachelicr"
###################################################################################

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
print("Current working directory is now:", os.getcwd())
# Vue names
docker_no_tag_vue = f"{docker}/{name_vue}"
docker_latest_vue = f"{docker}/{name_vue}:latest"
docker_versioned_vue = f"{docker}/{name_vue}:{version}"    
# Run names
docker_no_tag_run = f"{docker}/{name_run}"
docker_latest_run = f"{docker}/{name_run}:latest"
docker_versioned_run = f"{docker}/{name_run}:{version}"    

def run_commands(cmd_set):
    for cmd_one in cmd_set:
        print("##################################################################################")
        print(cmd_one)
        print("----------------------------------------------------------------------------------")
        try:            
            result = subprocess.run(cmd_one,stdout=subprocess.PIPE,shell=True,).stdout.decode('utf-8')            
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
#----------------------------------------------------------------------------------
cmd_run_build = []
cmd_run_build.append(f"docker build -t {name_run} -f Dockerfile_run .")
#----------------------------------------------------------------------------------
cmd_set_build = []        
cmd_set_build.append(f"docker build -t {name_vue} .")
#----------------------------------------------------------------------------------
cmd_set_tags = []
# runs
cmd_set_tags.append(f"docker tag {name_run} {docker_no_tag_run}")
cmd_set_tags.append(f"docker tag {name_run} {docker_versioned_run}")    
# vues
cmd_set_tags.append(f"docker tag {name_vue} {docker_no_tag_vue}")
cmd_set_tags.append(f"docker tag {name_vue} {docker_versioned_vue}")    
#----------------------------------------------------------------------------------
cmd_set_upload = []
# runs
cmd_set_upload.append(f"docker push {docker_no_tag_run}")
cmd_set_upload.append(f"docker push {docker_versioned_run}")
# vues
cmd_set_upload.append(f"docker push {docker_no_tag_vue}")
cmd_set_upload.append(f"docker push {docker_versioned_vue}")
#----------------------------------------------------------------------------------
if pre_clean_up:
    print("### 0/8 ##################### Cleaning up... ########################")
    test.clean_logs("tests/fixtures","*.log")
    test.clean_logs("tests/fixtures","*.trees")
    test.clean_logs("tests/fixtures","*.ops")
    test.clean_logs("tests/fixtures","*.Identifier")
    
    #delete the temp files in the fixtures folder
#####################################################
ok = True
#####################################################
if test_build:
    print("### 1/8 ####################### Running tests... ##########################")
    ok = run_commands(cmd_set_test)
#####################################################
if build_run and ok:    
    print("### 2/8 ####################### Running pisca-run build... ##########################")
    ok = run_commands(cmd_run_build)
    if ok:
        print("The pisca-run has built ok")
#####################################################
if test_regression and ok:
    # Run regression tests
    print("### 3/8 ###################### Running regression tests... #########################")
    ok = test.run_regression()
    if ok:
        print("### 4/8 ################## All beauti regression tests passed, commencing pisca/beast regression... #####################")
        ok = test.run_beast_regression()
    if ok:
        print("All regression tests passed, commencing docker builds...")
#####################################################
if build_vue and ok:
    print("### 5/8 ##################### Building docker images... ########################")  
    ok = run_commands(cmd_set_build)
#####################################################
if tag_dockers and ok:
    print("### 6/8 #################### Tagging docker images... #######################")
    ok = run_commands(cmd_set_tags)
#####################################################
if upload_dockers and ok:
    print("### 7/8 #################### Uploading docker images... #######################")
    ok = run_commands(cmd_set_upload)
#####################################################
if post_clean_up:
    print("### 8/8 ##################### Cleaning up... ########################")
    test.clean_logs("tests/fixtures","*.log")
    test.clean_logs("tests/fixtures","*.trees")
    test.clean_logs("tests/fixtures","*.ops")
    test.clean_logs("tests/fixtures","*.Identifier")
    #delete the temp files in the fixtures folder
#####################################################



    




