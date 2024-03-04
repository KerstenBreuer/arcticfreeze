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

"""Short description of package."""  # Please adapt to package

from importlib.metadata import version

from ._converters import (
    STANDARD_CONVERTERS,
    STANDARD_CONVERTERS_BY_INPUT_TYPE,
    STANDARD_MUTABLE_PRIORITY,
    STANDARD_NON_PRIMITIVE_IMMUTABLE_PRIORITY,
    STANDARD_PRIMITIVE_PRIORITY,
    Converter,
)
from ._freeze import UnknownTypeException, arctic_freeze

__all__ = [
    "UnknownTypeException",
    "arctic_freeze",
    "STANDARD_CONVERTERS",
    "STANDARD_CONVERTERS_BY_INPUT_TYPE",
    "STANDARD_MUTABLE_PRIORITY",
    "STANDARD_NON_PRIMITIVE_IMMUTABLE_PRIORITY",
    "STANDARD_PRIMITIVE_PRIORITY",
    "Converter",
]

__version__ = version(__package__)
