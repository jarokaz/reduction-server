
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

"""TensorFlow Datasets text classification task dataset generator."""

import functools
import json
import os

# Import libraries
from absl import app
from absl import flags
import tensorflow as tf
from official.nlp.bert import tokenization
from official.nlp.data import classifier_data_lib

FLAGS = flags.FLAGS

flags.DEFINE_string("vocab_file", None,
                    "The vocabulary file that the BERT model was trained on.")

flags.DEFINE_string(
    "train_data_output_path", None,
    "The path in which generated training input data will be written as tf"
    " records.")

flags.DEFINE_string(
    "eval_data_output_path", None,
    "The path in which generated evaluation input data will be written as tf"
    " records.")

flags.DEFINE_string(
    "test_data_output_path", None,
    "The path in which generated test input data will be written as tf"
    " records. If None, do not generate test data. Must be a pattern template"
    " as test_{}.tfrecords if processor has language specific test data.")

flags.DEFINE_string("meta_data_file_path", None,
                    "The path in which input meta data will be written.")

flags.DEFINE_integer(
    "max_seq_length", 128,
    "The maximum total input sequence length after WordPiece tokenization. "
    "Sequences longer than this will be truncated, and sequences shorter "
    "than this will be padded.")

flags.DEFINE_enum(
    "tokenization", "WordPiece", ["WordPiece", "SentencePiece"],
    "Specifies the tokenizer implementation, i.e., whether to use WordPiece "
    "or SentencePiece tokenizer. Canonical BERT uses WordPiece tokenizer, "
    "while ALBERT uses SentencePiece tokenizer.")

flags.DEFINE_string(
    "tfds_params", "", "Comma-separated list of TFDS parameter assigments for "
    "generic classfication data import (for more details "
    "see the TfdsProcessor class documentation).")
 

def main(_):
    if FLAGS.tokenization == "WordPiece":
        if not FLAGS.vocab_file:
            raise ValueError(
                "FLAG vocab_file for word-piece tokenizer is not specified.")
        tokenizer = tokenization.FullTokenizer(
            vocab_file=FLAGS.vocab_file, do_lower_case=FLAGS.do_lower_case)
        processor_text_fn = tokenization.convert_to_unicode
    else:
        assert FLAGS.tokenization == "SentencePiece"
        if not FLAGS.sp_model_file:
          raise ValueError(
              "FLAG sp_model_file for sentence-piece tokenizer is not specified.")
        tokenizer = tokenization.FullSentencePieceTokenizer(FLAGS.sp_model_file)
        processor_text_fn = functools.partial(
            tokenization.preprocess_text, lower=FLAGS.do_lower_case) 
        
    processor = classifier_data_lib.TfdsProcessor(
        tfds_params=FLAGS.tfds_params, process_text_fn=processor_text_fn)
  
    input_meta_data = classifier_data_lib.generate_tf_record_from_data_file(
        processor,
        None,
        tokenizer,
        train_data_output_path=FLAGS.train_data_output_path,
        eval_data_output_path=FLAGS.eval_data_output_path,
        test_data_output_path=FLAGS.test_data_output_path,
        max_seq_length=FLAGS.max_seq_length)

    tf.io.gfile.makedirs(os.path.dirname(FLAGS.meta_data_file_path))
    with tf.io.gfile.GFile(FLAGS.meta_data_file_path, "w") as writer:
        writer.write(json.dumps(input_meta_data, indent=4) + "\n")


if __name__ == "__main__":
    flags.mark_flag_as_required("meta_data_file_path")
    flags.mark_flag_as_required("tfds_params")
    app.run(main)
