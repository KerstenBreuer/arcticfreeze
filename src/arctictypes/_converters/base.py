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

"""Classes, constants, and utils for defining converters."""

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Callable, Final, Generic, TypeVar

DEFAULT_PRIORITY: Final = 0
STANDARD_PRIMITIVE_PRIORITY: Final = 200
STANDARD_NON_PRIMITIVE_IMMUTABLE_PRIORITY: Final = 100
STANDARD_MUTABLE_PRIORITY: Final = -100

InputObject = TypeVar("InputObject")


def no_op_return(obj: InputObject) -> InputObject:
    """Returns the provided object unchanged."""
    return obj


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
            For reference, the standard converters for primitive
            types (such as str, int, float, etc.) have a priority of 200; the standard
            converters for types that are already considered immutable have a priority
            of 100; the standard converters for mutable types (such as list, dict, set,
            etc.) have a priority of -100.
    """

    input_type: type[InputObject]
    converter: Callable[[InputObject], object] = no_op_return
    children: Callable[[InputObject], Iterable[object]] = lambda obj: ()
    priority: int = DEFAULT_PRIORITY
