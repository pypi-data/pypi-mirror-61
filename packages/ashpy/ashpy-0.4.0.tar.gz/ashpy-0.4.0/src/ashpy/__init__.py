# Copyright 2019 Zuru Tech HK Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""ASHPY Package."""

from .modes import LogEvalMode  # isort:skip
from . import (
    ashtypes,
    callbacks,
    contexts,
    datasets,
    keras,
    layers,
    losses,
    metrics,
    models,
    restorers,
    trainers,
)

__version__ = "0.4.0"
__url__ = "https://github.com/zurutech/ashpy"
__author__ = "Machine Learning Team @ Zuru Tech"
__email__ = "ml@zuru.tech"
