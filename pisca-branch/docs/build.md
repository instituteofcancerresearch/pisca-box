## Installation instructions for Phyfum on my virtualized linux:

```
git clone git@github.com:pbousquets/beast-mcmc-flipflop
cd beast-mcmc-flipflop
#git checkout dev
ant linux
````
The executable will now be at ./release/Linux/Phyfumv1.0_RC1/bin/beast (edited) 

To build with a private github need ssh keys:
```
docker build -t example --build-arg ssh_prv_key="$(cat ~/.ssh/id_rsa)" --build-arg ssh_pub_key="$(cat ~/.ssh/id_rsa.pub)"

docker build -t pisca-branch-b1 -f Dockerfile_b1 .  --build-arg ssh_prv_key="$(cat ~/.ssh/id_rsa)" --build-arg ssh_pub_key="$(cat ~/.ssh/id_rsa.pub)"
```

## Resources
https://vsupalov.com/build-docker-image-clone-private-repo-ssh-key/