from os import path

from kubernetes import client, config, utils

from kubernetes.stream import stream

from pprint import pprint

from kubecopy import copy_file_to_pod
def execute_on_container(core_api_instance,pod,namespace,exec_command1):
    user_name_str = stream(core_api_instance.connect_get_namespaced_pod_exec, pod,
    namespace,command=exec_command1, stderr=True, stdin=False,
    stdout=True, tty=False)
    return user_name_str

config.load_kube_config()
namespace = "default"
pod = "termi-demo"
exec_command1 = ["bash","/src/checkDirectory.sh"]
core_api_instance = client.CoreV1Api()
copy_file_to_pod(core_api_instance,"checkDirectory.sh","/home/roshan/Docker/BashScripts","/src")

result=execute_on_container(core_api_instance,pod,namespace,exec_command1)
print(result)
