# Copyright 2024 Kersten Henrik Breuer
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

"""Test the standard converters."""

from arctictypes._converters import (
    STANDARD_CONVERTERS,
    STANDARD_CONVERTERS_BY_INPUT_TYPE,
)
from arctictypes._freeze import sort_and_deduplicate_converters


def test_sorting_and_deduplication():
    """Make sure that the standard converters are sorted and that they only contain one
    converter for each input type.
    """
    (
        expected_converters,
        expected_converters_by_input_type,
    ) = sort_and_deduplicate_converters(STANDARD_CONVERTERS)
    assert expected_converters == STANDARD_CONVERTERS
    assert expected_converters_by_input_type == STANDARD_CONVERTERS_BY_INPUT_TYPE
