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

"""Logic for deep freezing mutable objects."""

import collections
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from types import NoneType  # type: ignore
from typing import Callable, Final, Generic, TypeVar

import immutabledict

DEFAULT_PRIORITY: Final = 0
BUILTIN_PRIMITIVE_PRIORITY: Final = 200
BUILTIN_NON_PRIMITIVE_IMMUTABLE_PRIORITY: Final = 100
BUILTIN_MUTABLE_PRIORITY: Final = -100

BUILTIN_PRIMITIVE_TYPES: Final = (str, int, float, bool, NoneType)

InputObject = TypeVar("InputObject")


def no_op_return(obj: InputObject) -> InputObject:
    """Returns the provided object unchanged."""
    return obj


def get_mapping_children(obj: Mapping) -> Iterable:
    """Returns an iterable that contains both the keys and the values of the provided
    mapping.
    """
    return (obj for key_value_pair in obj.items() for obj in key_value_pair)


@dataclass(frozen=True)
class Converter(Generic[InputObject]):
    """A class describing how to convert a (mutable) object to an immutable counterpart.

    Attributes:
        input_type:
            The type of the object to convert. The object may also has a type that is
            a subclass of this type.
        converter:
            A callable that takes an object and returns an immutable version of it.
            By default a no-op converter is used that returns the object unchanged.
        children:
            A callable that returns an iterable of all the children of the object. By
            default an empty iterable is returned corresponding to the assumption that
            the object has no children.
        priority:
            An integer indicating the priority of this converter. A higher priority
            means that this converter is preferred over others when multiple converters
            are applicable to the same object. The default priority is 0.
            For reference, the builtin converters for primitive
            types (such as str, int, float, etc.) have a priority of 200; the builtin
            converters for types that are already considered immutable have a priority
            of 100; the builtin converters for mutable types (such as list, dict, set,
            etc.) have a priority of -100.
    """

    input_type: type[InputObject]
    converter: Callable[[InputObject], object] = no_op_return
    children: Callable[[InputObject], Iterable[object]] = lambda obj: ()
    priority: int = DEFAULT_PRIORITY


BUILTIN_PRIMITIVE_CONVERTERS: Final[Sequence[Converter]] = tuple(
    Converter(input_type=type_, priority=BUILTIN_PRIMITIVE_PRIORITY)
    for type_ in BUILTIN_PRIMITIVE_TYPES
)

BUILTIN_NON_PRIMITIVE_IMMUTABLE_CONVERTERS: Final[Sequence[Converter]] = (
    Converter(input_type=bytes, priority=BUILTIN_NON_PRIMITIVE_IMMUTABLE_PRIORITY),
    Converter(
        input_type=tuple,
        children=no_op_return,
        priority=BUILTIN_NON_PRIMITIVE_IMMUTABLE_PRIORITY,
    ),
    Converter(
        input_type=frozenset,
        children=no_op_return,
        priority=BUILTIN_NON_PRIMITIVE_IMMUTABLE_PRIORITY,
    ),
    Converter(
        input_type=immutabledict.immutabledict,
        children=get_mapping_children,
        priority=BUILTIN_NON_PRIMITIVE_IMMUTABLE_PRIORITY,
    ),
)

BUILTIN_MUTABLE_CONVERTERS: Final[Sequence[Converter]] = (
    Converter(
        input_type=list, children=no_op_return, priority=BUILTIN_MUTABLE_PRIORITY
    ),
    Converter(
        input_type=dict,
        children=get_mapping_children,
        priority=BUILTIN_MUTABLE_PRIORITY,
    ),
    Converter(input_type=set, children=no_op_return, priority=BUILTIN_MUTABLE_PRIORITY),
    Converter(
        input_type=collections.deque,
        children=no_op_return,
        priority=BUILTIN_MUTABLE_PRIORITY,
    ),
)

BUILTIN_CONVERTERS: Final = (
    *BUILTIN_PRIMITIVE_CONVERTERS,
    *BUILTIN_NON_PRIMITIVE_IMMUTABLE_CONVERTERS,
    *BUILTIN_MUTABLE_CONVERTERS,
)


def shallow_freeze(obj: object):
    """Shallow freeze an object."""
