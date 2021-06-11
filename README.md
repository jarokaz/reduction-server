# Optimizing Distributed Training with Reduction Server


## Environment setups

### Create Artifact Repository

```
LOCATION=us-central1
REPO_NAME=jk-docker-repo-${LOCATION}


gcloud artifacts repositories create $REPO_NAME --repository-format=docker \
--location=$LOCATION --description="Docker repository"


gcloud auth configure-docker ${LOCATION}-docker.pkg.dev
```