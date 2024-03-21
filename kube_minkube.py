import subprocess

import sys

import os
 
def run_command(command):

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

    if result.returncode != 0:

        print(f"Error: {result.stderr}")

        sys.exit(result.returncode)

    print(result.stdout)
 
def install_minikube():

    print("let's do the 1st install")

    run_command("curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64")

    run_command("sudo install minikube-linux-amd64 /usr/local/bin/minikube")
 
def install_kubectl():

    print("let's do the 2nd install")

    run_command("curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl")

    run_command("chmod +x ./kubectl")

    run_command("sudo mv ./kubectl /usr/local/bin/kubectl")
 
def start_minikube():

    print("let's test it!")

    run_command("minikube start --cpus=4 --memory=8192")
 
def check_kubectl_config():

    print("safety check")

    run_command("kubectl cluster-info")

    #check kubectl coomand is configured properly to communicate with the cluster
    run_command("kubectl get nodes")
 
 #def check root should always run with root permissions, so use sudo to run it
def check_root():

    if os.geteuid() != 0:

        print("you've got root permissions!")

        sys.exit(1)
 
if __name__ == "__main__":

    check_root()

    install_minikube()

    install_kubectl()

    start_minikube()

    check_kubectl_config()
