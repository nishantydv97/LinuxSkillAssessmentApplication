from kubernetes import client, config


def main():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body=client.V1Namespace()
    body.metadata=client.V1ObjectMeta(name="mynamespace")
    
    #print(v1.list_namespace())
    v1.create_namespace(body)
   

main()
