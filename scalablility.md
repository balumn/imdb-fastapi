# How to make this Architecture Scalable

1. Switch to PostgreSQL or MySQL

# Architecture

There are 2 Solutions

### Solution 1

1. Containarise the application as well as the db
2. Deploy onto a k8s environment
    1. Set up persistant volumes
    2. Two services: FastAPI, Database
    3. Add up number of replicas

This way K8s will handle the scalabilty and failovers

### Solution 2 (AWS based)
1. Use a scalable database service. Eg: `AWS RDS`
2. Deploy our application onto a EC2 machine
3. Add the EC2 machine onto a `EC2 Autoscaling Group`
4. Set up a AWS loadbalancer onto the `EC2 Autoscaling Group` and let it listen for the API calls.