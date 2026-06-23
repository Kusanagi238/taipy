# Copyright 2021-2025 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""

from .commons.apispec import APISpecExt


class _LazyAPISpec:
    """Lazy wrapper to delay APISpecExt instantiation until first use.

    This avoids creating the APISpecExt at module import time which can
    pull in transitive dependencies during pytest collection.
    """
    def __init__(self):
        super().__setattr__("_obj", None)

    def _ensure(self):
        if self._obj is None:
            super().__setattr__("_obj", APISpecExt())

    def __getattr__(self, name):
        self._ensure()
        return getattr(self._obj, name)

    def __setattr__(self, name, value):
        if name == "_obj":
            super().__setattr__(name, value)
        else:
            self._ensure()
            setattr(self._obj, name, value)


apispec = _LazyAPISpec()
