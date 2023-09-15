import __init__ # noqa: F401
import tests.runner as test
import os
import libs.cmds as cmd
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

# Run regression tests
ok = test.run_regression()

if ok:
    print("All regression tests passed, commencing docker builds...")
    cmd_set = []    
    cmd_set.append(f"docker build -t {name} .")
    cmd_set.append(f"docker tag {name} {docker_no_tag}")
    cmd_set.append(f"docker tag {name} {docker_versioned}")    
    cmd_set.append(f"docker push {docker_no_tag}")
    cmd_set.append(f"docker push {docker_versioned}")
        
    for cmd_one in cmd_set:
        print("##################################################################################")
        print(cmd_one)
        print("----------------------------------------------------------------------------------")
        try:            
            result = subprocess.run(cmd_one,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True,).stdout.decode('utf-8')            
            print(result.strip())
        except Exception as e:
            print("Failed to run", cmd_one,str(e),"!")
            exit(1)
    
    

