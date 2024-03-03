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

"""An implementation of a deep frozen dictionary."""


from typing import TypeVar

import immutabledict

_K = TypeVar("_K")
_V_co = TypeVar("_V_co", covariant=True)


class ArcticDict(immutabledict.immutabledict[_K, _V_co]):
    """An implementation of a deep frozen dictionary."""
