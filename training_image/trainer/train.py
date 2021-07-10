
# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""TFM common training driver."""

import json
import os

from absl import app
from absl import flags
from absl import logging
import gin
from official.common import distribute_utils
from official.common import flags as tfm_flags
from official.core import task_factory
from official.core import train_lib
from official.core import train_utils
from official.modeling import performance
from tensorflow.dtypes import bfloat16, float16, float32

FLAGS = flags.FLAGS


def _get_model_dir(model_dir):
  """Defines utility functions for model saving.

  In a multi-worker scenario, the chief worker will save to the
  desired model directory, while the other workers will save the model to
  temporary directories. It’s important that these temporary directories
  are unique in order to prevent multiple workers from writing to the same
  location. Saving can contain collective ops, so all workers must save and
  not just the chief.
  """

  def _is_chief(task_type, task_id):
    return ((task_type == 'chief' and task_id == 0) or task_type is None)

  tf_config = os.getenv('TF_CONFIG')
  if tf_config:
    tf_config = json.loads(tf_config)

    if not _is_chief(tf_config['task']['type'], tf_config['task']['index']):
      model_dir = os.path.join(model_dir,
                               'worker-{}').format(tf_config['task']['index'])

  logging.info('Setting model_dir to: %s', model_dir)

  return model_dir


def main(_):

  model_dir = _get_model_dir(FLAGS.model_dir)

  gin.parse_config_files_and_bindings(FLAGS.gin_file, FLAGS.gin_params)
  params = train_utils.parse_configuration(FLAGS)

  if 'train' in FLAGS.mode:
    # Pure eval modes do not output yaml files. Otherwise continuous eval job
    # may race against the train job for writing the same file.
    train_utils.serialize_config(params, model_dir)

  # Sets mixed_precision policy. Using 'mixed_float16' or 'mixed_bfloat16'
  # can have significant impact on model speeds by utilizing float16 in case of
  # GPUs, and bfloat16 in the case of TPUs. loss_scale takes effect only when
  # dtype is float16
  if params.runtime.mixed_precision_dtype:
    performance.set_mixed_precision_policy(params.runtime.mixed_precision_dtype)
  distribution_strategy = distribute_utils.get_distribution_strategy(
      distribution_strategy=params.runtime.distribution_strategy,
      all_reduce_alg=params.runtime.all_reduce_alg,
      num_gpus=params.runtime.num_gpus,
      tpu_address=params.runtime.tpu,
      **params.runtime.model_parallelism())
  with distribution_strategy.scope():
    task = task_factory.get_task(params.task, logging_dir=model_dir)

  train_lib.run_experiment(
      distribution_strategy=distribution_strategy,
      task=task,
      mode=FLAGS.mode,
      params=params,
      model_dir=model_dir)

  train_utils.save_gin_config(FLAGS.mode, model_dir)


if __name__ == '__main__':
  tfm_flags.define_flags()
  app.run(main)
