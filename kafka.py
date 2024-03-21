import subprocess

import sys
 
def run_command(command):

    try:

        subprocess.check_call(command, shell=True)

    except subprocess.CalledProcessError as e:

        print(f"erorr: {e}")

        sys.exit(1)
 
def install_helm():

    print("trying 1st install ever of helm")

    run_command("curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash")
 
def deploy_kafka_cluster():

    print("add bitnami to the helm")

    run_command("helm repo add bitnami https://charts.bitnami.com/bitnami")

    run_command("helm repo update")
 
    print("deploy kafka with 3 nodes")

    run_command("helm install kafka bitnami/kafka --set replicaCount=3")
 
if __name__ == "__main__":

    install_helm()

    deploy_kafka_cluster()
