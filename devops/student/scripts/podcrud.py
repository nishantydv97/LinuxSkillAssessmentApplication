import yaml
from os import path
from kubernetes import client, config, utils
from kubernetes.stream import stream
import tarfile
from tempfile import TemporaryFile

from pprint import pprint


class PodCrud():
    DEPLOYMENT_NAME = "termi-demo"
    IMAGE_NAME = "chetanpawar968/terminado"
    PORT_NO = 8765
    APP_NAME = "termi-demo"
    API_VERSION = "v1"
    KIND = "Pod"
    NAMESPACE = "default"
    api_instance = None

    def __init__(self):

        config.load_kube_config()
        configuration = client.Configuration()

        # ssl error
        # configuration.verify_ssl=False

        self.api_instance = client.CoreV1Api(client.ApiClient(configuration))
        print("initates===============================================")

    def create_pod_object(self,pod_name):
        # Configureate Pod template container
        container = client.V1Container(
            name=pod_name,
            image=self.IMAGE_NAME,
            ports=[client.V1ContainerPort(container_port=self.PORT_NO)])
        # Create and configurate a spec section

        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"name": pod_name}),
            spec=client.V1PodSpec(containers=[container]))
        """
        template = client.V1PodTemplateSpec(
            spec=client.V1PodSpec(containers=[container]))
        """
        # Create the specification of deployment
        spec = client.V1PodSpec(containers=[container])
        #    template=template)
        # Instantiate the deployment object
        pod_object = client.V1Pod(
            api_version=self.API_VERSION,
            kind=self.KIND,
            metadata=client.V1ObjectMeta(name=pod_name),
            spec=spec)

        return pod_object

    def create_pod(self,pod_body,name):
        # pod_body = self.create_pod_object()
        # api_result=self.api_instance.read_namespaced_pod(name=name,namespace=self.NAMESPACE)

        #print("name-----------------" + name)
        api_response = self.api_instance.create_namespaced_pod(self.NAMESPACE, pod_body)
        # pprint(api_response)
        # pprint(api_response.status)

        # pprint(api_response.status.pod_ip)
        # ipAllocated=api_response.status.pod_ip
        ipAllocated = None
        while ipAllocated == None:
            # print(ipAllocated)
            ipAllocated = self.read_pod_info( name)
        return ipAllocated

    def delete_pod(self):
        api_response = self.api_instance.delete_namespaced_pod_status(self.DEPLOYMENT_NAME, self.NAMESPACE,
                                                                      body=client.V1DeleteOptions(
                                                                          propagation_policy='Foreground',
                                                                          grace_period_seconds=5))
        # pprint(api_response)

    def read_pod_info(self,name):
        api_response = self.api_instance.read_namespaced_pod(name, self.NAMESPACE)
        return api_response.status.pod_ip
        # pprint(api_response.status.pod_ip)

    def execute_on_container(self, podname, exec_command1):
        user_name_str = stream(self.api_instance.connect_get_namespaced_pod_exec, podname,
                               self.NAMESPACE, command=exec_command1, stderr=True, stdin=False,
                               stdout=True, tty=False)
        return user_name_str

    def copy_file_to_pod(self,filename,sourcePath,destinationPath,name):
        exec_command = ['tar', 'xvf', '-', '-C', destinationPath]
        resp = stream(self.api_instance.connect_get_namespaced_pod_exec, name, self.NAMESPACE,
                      command=exec_command,
                      stderr=True, stdin=True,
                      stdout=True, tty=False,
                      _preload_content=False)

        source_file = sourcePath

        with TemporaryFile() as tar_buffer:
            with tarfile.open(fileobj=tar_buffer, mode='w') as tar:
                # tar.add(source_file)
                tar.add(name=source_file, arcname=filename)

            tar_buffer.seek(0)
            commands = []
            commands.append(tar_buffer.read())

            while resp.is_open():
                resp.update(timeout=1)
                if resp.peek_stdout():
                    a = 0
                    print("STDOUT: %s" % resp.read_stdout())
                if resp.peek_stderr():
                    print("STDERR: %s" % resp.read_stderr())
                if commands:
                    c = commands.pop(0)
                    # print("Running command... %s\n" % c)
                    resp.write_stdin(c.decode())
                else:
                    break
            resp.close()
