

#craete service account first
kubectl create -f createServiceAC.yaml


# add roles to that account
kubectl craete -f clustorRole.yaml
