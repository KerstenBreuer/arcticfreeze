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

"""Standard converters that come with this library."""

import collections
from collections.abc import Iterable, Mapping, Sequence
from typing import Final

import immutabledict

from arctictypes._converters.base import (
    STANDARD_MUTABLE_PRIORITY,
    STANDARD_NON_PRIMITIVE_IMMUTABLE_PRIORITY,
    STANDARD_PRIMITIVE_PRIORITY,
    Converter,
    no_op_return,
)

STANDARD_PRIMITIVE_TYPES: Final = (str, int, float, bool, type(None))


def get_mapping_children(obj: Mapping) -> Iterable:
    """Returns an iterable that contains both the keys and the values of the provided
    mapping.
    """
    return (obj for key_value_pair in obj.items() for obj in key_value_pair)


STANDARD_PRIMITIVE_CONVERTERS: Final[Sequence[Converter]] = tuple(
    Converter(input_type=type_, priority=STANDARD_PRIMITIVE_PRIORITY)
    for type_ in STANDARD_PRIMITIVE_TYPES
)

STANDARD_NON_PRIMITIVE_IMMUTABLE_CONVERTERS: Final[Sequence[Converter]] = (
    Converter(input_type=bytes, priority=STANDARD_NON_PRIMITIVE_IMMUTABLE_PRIORITY),
    Converter(
        input_type=tuple,
        children=no_op_return,
        priority=STANDARD_NON_PRIMITIVE_IMMUTABLE_PRIORITY,
    ),
    Converter(
        input_type=frozenset,
        children=no_op_return,
        priority=STANDARD_NON_PRIMITIVE_IMMUTABLE_PRIORITY,
    ),
    Converter(
        input_type=immutabledict.immutabledict,
        children=get_mapping_children,
        priority=STANDARD_NON_PRIMITIVE_IMMUTABLE_PRIORITY,
    ),
)

STANDARD_MUTABLE_CONVERTERS: Final[Sequence[Converter]] = (
    Converter(
        input_type=list, children=no_op_return, priority=STANDARD_MUTABLE_PRIORITY
    ),
    Converter(
        input_type=dict,
        children=get_mapping_children,
        priority=STANDARD_MUTABLE_PRIORITY,
    ),
    Converter(
        input_type=set, children=no_op_return, priority=STANDARD_MUTABLE_PRIORITY
    ),
    Converter(
        input_type=collections.deque,
        children=no_op_return,
        priority=STANDARD_MUTABLE_PRIORITY,
    ),
)

STANDARD_CONVERTERS: Final = (
    *STANDARD_PRIMITIVE_CONVERTERS,
    *STANDARD_NON_PRIMITIVE_IMMUTABLE_CONVERTERS,
    *STANDARD_MUTABLE_CONVERTERS,
)

STANDARD_CONVERTERS_BY_INPUT_TYPE: Final = {
    converter.input_type: converter for converter in STANDARD_CONVERTERS
}
