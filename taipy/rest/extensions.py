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

# Lazy import to avoid hard dependency at module import time (may be missing in some environments)
_APISpecExt = None

def _get_APISpecExt():
    """Return the APISpecExt class, importing it lazily and tolerating import failures."""
    global _APISpecExt
    if _APISpecExt is None:
        try:
            from .commons.apispec import APISpecExt as _ImportedAPISpecExt
        except Exception:
            # If import fails (e.g., missing optional runtime dependency), keep as None
            _ImportedAPISpecExt = None
        _APISpecExt = _ImportedAPISpecExt
    return _APISpecExt

apispec = None

def get_apispec():
    """Lazily instantiate and return the apispec extension. Returns None if unavailable."""
    global apispec
    if apispec is None:
        APISpecExt = _get_APISpecExt()
        if APISpecExt is None:
            return None
        apispec = APISpecExt()
    return apispec
