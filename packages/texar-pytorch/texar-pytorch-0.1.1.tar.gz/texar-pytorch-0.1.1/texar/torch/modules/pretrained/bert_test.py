# Copyright 2019 The Texar Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Unit tests for BERT utils.
"""

import os
import unittest

from texar.torch.modules.pretrained.bert import *
from texar.torch.utils.test import pretrained_test


class BERTUtilsTest(unittest.TestCase):
    r"""Tests BERT utils.
    """

    @pretrained_test
    def test_load_pretrained_bert_AND_transform_bert_to_texar_config(self):

        pretrained_model_dir = PretrainedBERTMixin.download_checkpoint(
            pretrained_model_name="bert-base-uncased")

        info = list(os.walk(pretrained_model_dir))
        _, _, files = info[0]
        self.assertIn('bert_model.ckpt.meta', files)
        self.assertIn('bert_model.ckpt.data-00000-of-00001', files)
        self.assertIn('bert_model.ckpt.index', files)
        self.assertIn('bert_config.json', files)

        model_config = PretrainedBERTMixin._transform_config(
            pretrained_model_name="bert-base-uncased",
            cache_dir=pretrained_model_dir)

        exp_config = {
            'hidden_size': 768,
            'embed': {
                'name': 'word_embeddings',
                'dim': 768
            },
            'vocab_size': 30522,
            'segment_embed': {
                'name': 'token_type_embeddings',
                'dim': 768
            },
            'type_vocab_size': 2,
            'position_embed': {
                'name': 'position_embeddings',
                'dim': 768
            },
            'position_size': 512,
            'encoder': {
                'name': 'encoder',
                'embedding_dropout': 0.1,
                'num_blocks': 12,
                'multihead_attention': {
                    'use_bias': True,
                    'num_units': 768,
                    'num_heads': 12,
                    'output_dim': 768,
                    'dropout_rate': 0.1,
                    'name': 'self'
                },
                'residual_dropout': 0.1,
                'dim': 768,
                'use_bert_config': True,
                'eps': 1e-12,
                'poswise_feedforward': {
                    'layers': [
                        {
                            'type': 'Linear',
                            'kwargs': {
                                'in_features': 768,
                                'out_features': 3072,
                                'bias': True
                            }
                        },
                        {'type': 'BertGELU'},
                        {
                            'type': 'Linear',
                            'kwargs': {
                                'in_features': 3072,
                                'out_features': 768,
                                'bias': True
                            }
                        }
                    ]
                }
            }
        }

        self.assertDictEqual(model_config, exp_config)


if __name__ == "__main__":
    unittest.main()
