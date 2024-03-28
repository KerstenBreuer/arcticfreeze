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

"""An implementation of a frozen dictionary with support for pydantic."""

import typing
from collections.abc import Mapping
from typing import Any, TypeVar

from immutabledict import immutabledict
from pydantic import GetCoreSchemaHandler
from pydantic_core.core_schema import (
    CoreSchema,
    no_info_after_validator_function,
    plain_serializer_function_ser_schema,
)

_K = TypeVar("_K")
_V_co = TypeVar("_V_co", covariant=True)


class FrozenDict(immutabledict[_K, _V_co]):
    """A pydantic-comatible wrapper around immutabledict."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Get the pydantic core schema for this type."""
        # Validate the type against a Mapping:
        args = typing.get_args(source)
        if not args:
            validation_schema = handler.generate_schema(Mapping)
            return_schema = handler.generate_schema(dict)
        elif len(args) == 2:
            validation_schema = handler.generate_schema(Mapping[args[0], args[1]])  # type: ignore
            return_schema = handler.generate_schema(dict[args[0], args[1]])  # type: ignore
        else:
            raise TypeError(
                "Expected exactly two (or no) type arguments for FrozenDict, got"
                + f" {len(args)}"
            )

        serialization_schema = plain_serializer_function_ser_schema(
            lambda x: dict(x), return_schema=return_schema
        )

        # Uses cls as validator function to convert the dict to a FrozenDict:
        return no_info_after_validator_function(
            # callable to use after validation against the schema (convert to
            # FrozenDict):
            cls,
            # the validation schema to use before executing the callable:
            validation_schema,
            serialization=serialization_schema,
        )
