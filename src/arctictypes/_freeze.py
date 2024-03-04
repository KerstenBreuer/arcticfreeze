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

from arctictypes._converters import (
    STANDARD_CONVERTERS,
    STANDARD_CONVERTERS_BY_INPUT_TYPE,
    Converter,
)


class UnknownTypeException(Exception):
    """An exception indicating that a converter for a given type could not be found."""

    def __init__(self, input_type: type):
        super().__init__(
            f"No converter was found freezing an object of type {input_type}."
        )


def arctic_freeze(obj: object) -> object:
    """Deep freeze the provided object."""
    raise NotImplementedError("This function is not yet implemented.")
