from kubernetes import client, config
from kubernetes.stream import stream
import tarfile
from tempfile import TemporaryFile

# create an instance of the API class

def copy_file_to_pod(api_instance,filename,sourcePath,destinationPath):
    exec_command = ['tar', 'xvf', '-', '-C', destinationPath]
    resp = stream(api_instance.connect_get_namespaced_pod_exec, "termi-demo", 'default',
                  command=exec_command,
                  stderr=True, stdin=True,
                  stdout=True, tty=False,
                  _preload_content=False)

    source_file = sourcePath+"/"+filename

    with TemporaryFile() as tar_buffer:
        with tarfile.open(fileobj=tar_buffer, mode='w') as tar:
            #tar.add(source_file)
            tar.add(name=source_file,arcname=filename)

        tar_buffer.seek(0)
        commands = []
        commands.append(tar_buffer.read())

        while resp.is_open():
            resp.update(timeout=1)
            if resp.peek_stdout():
                a=0
                #print("STDOUT: %s" % resp.read_stdout())
            if resp.peek_stderr():
                print("STDERR: %s" % resp.read_stderr())
            if commands:
                c = commands.pop(0)
                # print("Running command... %s\n" % c)
                resp.write_stdin(c.decode())
            else:
                break
        resp.close()
