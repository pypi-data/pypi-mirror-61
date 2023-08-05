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
Unit tests for regularizers.
"""

import unittest

import torch

from texar.torch.core.regularizers import *


class RegularizerTest(unittest.TestCase):
    r"""Test regularizers.
    """

    def setUp(self):
        self.x = torch.tensor([-1, 2, -3, 4, -5])
        self.l1 = 0.1
        self.l2 = 0.2

    def test_l1(self):
        r"""Tests l1."""
        regularizer = l1(self.l1)
        self.assertEqual(regularizer.l1, 0.1)
        self.assertEqual(regularizer.l2, 0)

        regularization = regularizer(self.x)
        self.assertEqual(regularization.item(), self.l1 * (1 + 2 + 3 + 4 + 5))

        self.assertEqual(regularizer.get_config().get("l1"), 0.1)
        self.assertEqual(regularizer.get_config().get("l2"), 0)

    def test_l2(self):
        r"""Tests l2."""
        regularizer = l2(self.l2)
        self.assertEqual(regularizer.l1, 0)
        self.assertEqual(regularizer.l2, 0.2)

        regularization = regularizer(self.x)
        self.assertEqual(regularization.item(), self.l2 * (1 + 4 + 9 + 16 + 25))

        self.assertEqual(regularizer.get_config().get("l1"), 0)
        self.assertEqual(regularizer.get_config().get("l2"), 0.2)

    def test_l1_l2(self):
        r"""Tests l1_l2."""
        regularizer = l1_l2(self.l1, self.l2)
        self.assertEqual(regularizer.l1, 0.1)
        self.assertEqual(regularizer.l2, 0.2)

        regularization = regularizer(self.x)
        self.assertEqual(regularization.item(), self.l1 * (1 + 2 + 3 + 4 + 5) +
                         self.l2 * (1 + 4 + 9 + 16 + 25))

        self.assertEqual(regularizer.get_config().get("l1"), 0.1)
        self.assertEqual(regularizer.get_config().get("l2"), 0.2)


if __name__ == "__main__":
    unittest.main()
