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

from collections.abc import Mapping, Sequence
from typing import Optional

from arctictypes._converters import (
    STANDARD_CONVERTERS,
    STANDARD_CONVERTERS_BY_INPUT_TYPE,
    Converter,
)


class ConverterNotFoundError(Exception):
    """An exception indicating that a converter for a given type could not be found."""

    def __init__(self, *, input_type: type):
        super().__init__(
            f"No converter was found freezing an object of type {input_type}."
        )


def sort_and_deduplicate_converters(
    converters: Sequence[Converter],
) -> tuple[Sequence[Converter], Mapping[type, Converter]]:
    """The provided sequence of converters is sorted (1) by decreasing priority and (2)
    by the order in which they where originally defined. For each input type, only the
    last converter in the sorted sequence is kept. The function returns a tuple of the
    sorted sequence of converters and a mapping of sorted converters by input type.
    """
    sorted_converters = sorted(
        converters, key=lambda converter: converter.priority, reverse=True
    )
    converters_by_input_type = {
        converter.input_type: converter for converter in sorted_converters
    }
    sorted_deduplicated_converters = tuple(converters_by_input_type.values())
    return sorted_deduplicated_converters, converters_by_input_type


def get_all_converters(
    *,
    add_converters: Optional[Sequence[Converter]] = None,
) -> tuple[Sequence[Converter], Mapping[type, Converter]]:
    """Returns a tuple of a sequence of all converters and a mapping of converters by
    input type. Both are sorted (1) by decreasing priority and (2) by the order in which
    they where originally defined.

    Args:
        add_converters:
            An optional sequence of additional converters, see the documentation of the
            `get_converter_by_type` function for details.
    """
    if add_converters is None:
        # assumes that the standard converters are already sorted:
        return STANDARD_CONVERTERS, STANDARD_CONVERTERS_BY_INPUT_TYPE

    all_converters = tuple(
        converter
        for sequence in (STANDARD_CONVERTERS, add_converters)
        for converter in sequence
    )
    return sort_and_deduplicate_converters(all_converters)


def get_converter_by_type(
    *,
    input_type: type,
    add_converters: Optional[Sequence[Converter]] = None,
    by_superclass: bool = True,
) -> Converter:
    """Get the converter for the given input type.

    Args:
        input_type:
            The type of the object to be converted.
        add_converters:
            Optionally provide a sequence of converters to be considered in addition
            to the standard converters that come with this library. If providing a
            custom converter for an input type that is already present in the standard
            set, the standard converter is overwritten.
        by_superclass:
            It is always tried to find a converter that matches the exact input type. If
            that fails and this argument is set to True, it is also tried to find a
            converter matching a superclass of the input type. The first matching
            converter is used, thus the priorities and the sequence of the converters
            (both standard and custion once defined via `add_converters`) are important.

    Raises:
        ConverterNotFoundError:
            If no converter for the given input type could be found.
    """
    converters, converters_by_input_type = get_all_converters(
        add_converters=add_converters
    )

    # try to match by exact type:
    try:
        return converters_by_input_type[input_type]
    except KeyError as error:
        if not by_superclass:
            raise ConverterNotFoundError(input_type=input_type) from error

    # match by superclass:
    for converter in converters:
        if issubclass(input_type, converter.input_type):
            return converter

    raise ConverterNotFoundError(input_type=input_type)


def arctic_freeze(obj: object) -> object:
    """Deep freeze the provided object."""
    raise NotImplementedError("This function is not yet implemented.")
