# fluxion - testing framework for codecs
# Copyright (C) 2020, Fluendo, S.A.
#  Author: Pablo Marcos Oltra <pmarcos@fluendo.com>, Fluendo, S.A.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import os
import unittest

from fluxion.decoder import Decoder
from fluxion.test_vector import TestVector


class Test(unittest.TestCase):
    '''Test suite for decoder tests'''

    def __init__(self, decoder: Decoder, test_suite, test_vector: TestVector, results_dir: str,
                 reference: bool, timeout: int):
        self.decoder = decoder
        self.test_suite = test_suite
        self.test_vector = test_vector
        self.resources_dir = self.test_suite.resources_dir
        self.results_dir = results_dir
        self.reference = reference
        self.timeout = timeout
        test_name = ''
        for char in f'{decoder.name}_{test_suite.name}_{test_vector.name}':
            if char.isalnum():
                test_name += char
            else:
                test_name += '_'
        setattr(self, test_name, self._test)
        super().__init__(test_name)

    def _test(self):
        output_dir = os.path.join(
            self.results_dir, self.test_suite.name, str(self.test_suite.codec))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_filepath = os.path.join(
            output_dir, self.test_vector.name + '.yuv')
        result = self.decoder.decode(
            os.path.join(self.resources_dir, self.test_suite.name,
                         self.test_vector.name, self.test_vector.input_file),
            output_filepath, self.timeout)
        if not self.reference:
            self.assertEqual(self.test_vector.result.lower(), result.lower(),
                             f'{self.test_vector.input_file}')
        else:
            for test_vector in self.test_suite.test_vectors:
                if test_vector.name == self.test_vector.name:
                    test_vector.result = result
