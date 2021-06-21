## Create a MIG templare

```
gcloud compute instance-templates create cluster-template \
--machine-type=n1-custom-24-159744 \
--accelerator=count=1,type=nvidia-tesla-t4 \
--image-family=tf-latest-gpu \
--image-project=deeplearning-platform-release \
--boot-disk-size 200GB \
--network-interface=nic-type=GVNIC,network-tier=PREMIUM,address= \
--maintenance-policy=TERMINATE \
--metadata=install-nvidia-driver=True \
--restart-on-failure \
--scopes=cloud-platform

```

```
gcloud compute instance-templates create cluster-template \
--machine-type=n1-standard-8 \
--accelerator=count=1,type=nvidia-tesla-t4 \
--image-family=tf2-2-5-cu110 \
--image-project=deeplearning-platform-release \
--boot-disk-size 200GB \
--network-interface=nic-type=GVNIC,network-tier=PREMIUM,address= \
--maintenance-policy=TERMINATE \
--metadata=install-nvidia-driver=True \
--restart-on-failure \
--scopes=cloud-platform

```


```
gcloud compute instance-templates describe cluster-template
```

```
gcloud compute instance-templates delete cluster-template
```


```
gcloud compute instance-groups managed create training-cluster \
--base-instance-name cluster \
--size 4 \
--template cluster-template \
--zone us-central1-a
```

```
TRAIN_IMAGE=gcr.io/jk-mlops-dev/model_garden:latest
MODEL_DIR=gs://jk-vertex-demos/t16
PARAMS=\
task.train_data.input_path=gs://jk-vertex-demos/datasets/MNLI/mnli_train.tf_record,\
task.validation_data.input_path=gs://jk-vertex-demos/datasets/MNLI/mnli_valid.tf_record,\
task.hub_module_url=https://tfhub.dev/tensorflow/bert_en_uncased_L-24_H-1024_A-16/4,\
task.train_data.global_batch_size=32,\
task.validation_data.global_batch_size=32,\
runtime.distribution_strategy=multi_worker_mirrored,\
runtime.all_reduce_alg=nccl,\
runtime.num_gpus=1

docker run -it --rm --gpus all \
--env TF_CONFIG='{"cluster": {"chief": ["10.128.15.199:2222"], "worker": ["10.128.15.201:2222"]}, "task": {"type": "chief", "index": 0} }' \
--network=host \
${TRAIN_IMAGE} trainer/train.py \
--experiment=bert/sentence_prediction \
--mode=train_and_eval \
--model_dir=${MODEL_DIR} \
--config_file=trainer/glue_mnli_matched.yaml \
--params_override=${PARAMS} 

docker run -it --rm --gpus all \
--env TF_CONFIG='{"cluster": {"chief": ["10.128.15.199:2222"], "worker": ["10.128.15.201:2222"]}, "task": {"type": "worker", "index": 0} }' \
--network=host \
${TRAIN_IMAGE} trainer/train.py \
--experiment=bert/sentence_prediction \
--mode=train_and_eval \
--model_dir=${MODEL_DIR} \
--config_file=trainer/glue_mnli_matched.yaml \
--params_override=${PARAMS} 

```


```
TRAIN_IMAGE=gcr.io/jk-mlops-dev/model_garden:latest
MODEL_DIR=gs://jk-vertex-demos/t15
PARAMS=\
task.train_data.input_path=gs://jk-vertex-demos/datasets/MNLI/mnli_train.tf_record,\
task.validation_data.input_path=gs://jk-vertex-demos/datasets/MNLI/mnli_valid.tf_record,\
task.hub_module_url=https://tfhub.dev/tensorflow/bert_en_uncased_L-24_H-1024_A-16/4,\
task.train_data.global_batch_size=16,\
task.validation_data.global_batch_size=16,\
runtime.distribution_strategy=mirrored,\
runtime.num_gpus=1

docker run -it --rm --gpus all \
--env TF_CONFIG='{"cluster": {"chief": ["10.128.15.199:2222"], "worker": ["10.128.15.201:2222"]}, "task": {"type": "worker", "index": 0} }' \
${TRAIN_IMAGE} trainer/train.py \
--experiment=bert/sentence_prediction \
--mode=train_and_eval \
--model_dir=${MODEL_DIR} \
--config_file=trainer/glue_mnli_matched.yaml \
--params_override=${PARAMS} 
```