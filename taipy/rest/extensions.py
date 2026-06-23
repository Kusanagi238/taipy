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

def _create_apispec():
    # Import only when actually creating the instance to avoid module-level side effects
    from .commons.apispec import APISpecExt
    return APISpecExt()


class _LazyAPISpec:
    """Lazy proxy that defers creating the real APISpecExt until first use."""
    def __init__(self):
        self._instance = None

    def _ensure(self):
        if self._instance is None:
            self._instance = _create_apispec()

    def __getattr__(self, name):
        self._ensure()
        return getattr(self._instance, name)

    def __repr__(self):
        if self._instance is None:
            return "<Lazy APISpecExt (not created)>"
        return repr(self._instance)


apispec = _LazyAPISpec()
