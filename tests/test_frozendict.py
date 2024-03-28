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

"""Test the FrozenDict class."""

from arctictypes._internal.frozendict import FrozenDict
from pydantic import BaseModel, ConfigDict


def test_frozen_dict():
    """Test validation and serialization of FrozenDict used in pydantic models.."""

    class Test(BaseModel):
        dict_: FrozenDict

    test_dict = {1: 2}

    test_from_dict = Test.model_validate({"dict_": test_dict})
    test_from_frozendict = Test(dict_=FrozenDict(test_dict))

    assert test_from_dict.dict_ == test_from_frozendict.dict_ == FrozenDict(test_dict)

    test_dumped = test_from_dict.model_dump()
    observed_dict = test_dumped["dict_"]
    assert observed_dict == test_dict
    assert isinstance(observed_dict, dict)


def test_frozen_dict_schema():
    """Test JSON schema generation of FrozenDicts-containing pydantic models."""

    class Test(BaseModel):
        dict_: FrozenDict

    schema_from_frozendict = Test.model_json_schema()

    # redefine Test to not using standard dict:
    class Test(BaseModel):  # type: ignore
        dict_: dict

    schema_from_dict = Test.model_json_schema()

    assert schema_from_frozendict == schema_from_dict


def test_frozen_dict_hashing():
    """Test hashing and comparison of pydantic models using FrozenDicts."""

    class Test(BaseModel):
        dict_: FrozenDict

        model_config = ConfigDict(frozen=True)

    test_dict = {1: 2}

    test1 = Test.model_validate({"dict_": test_dict})
    test2 = Test.model_validate({"dict_": test_dict})

    # make sure hash does not throw an exception
    hash(test1)

    assert test1 == test2


def test_frozen_dict_nesting():
    """Test nested pydantic models using FrozenDict."""

    class Inner(BaseModel):
        dict_: FrozenDict

    class Test(BaseModel):
        inner: FrozenDict[str, Inner]

    test_dict = {1: 2}

    test1 = Test.model_validate({"inner": {"test": {"dict_": test_dict}}})
    assert isinstance(test1.inner["test"], Inner)

    test2 = Test(
        inner=FrozenDict({"test": FrozenDict({"dict_": FrozenDict(test_dict)})})
    )
    assert test1 == test2
