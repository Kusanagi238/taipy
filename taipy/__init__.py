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

import importlib
from importlib.util import find_spec

if find_spec("taipy"):
    # Lazily expose symbols from optional subpackages to avoid importing
    # heavy/optional dependencies at package import time (which can break
    # test collection or environments missing extras).
    _lazy_modules = []
    if find_spec("taipy.common") and find_spec("taipy.common.config"):
        _lazy_modules.append("taipy.common.config._init")

    if find_spec("taipy.gui"):
        _lazy_modules.append("taipy.gui._init")

    if find_spec("taipy.core"):
        _lazy_modules.append("taipy.core._init")

    if find_spec("taipy.rest"):
        _lazy_modules.append("taipy.rest._init")

    if find_spec("taipy.gui_core"):
        _lazy_modules.append("taipy.gui_core._init")

    if find_spec("taipy.enterprise"):
        _lazy_modules.append("taipy.enterprise._init")

    if find_spec("taipy.designer"):
        _lazy_modules.append("taipy.designer._init")

    _has_run = bool(find_spec("taipy._run"))

    def __getattr__(name):
        """Lazily import attributes from known submodule init files.

        This avoids importing optional dependencies during package import
        and only triggers imports when a symbol is actually accessed.
        """
        # Special-case the run function (previously imported as _run -> run)
        if _has_run and name == "run":
            m = importlib.import_module("taipy._run")
            return m._run

        for modname in _lazy_modules:
            try:
                m = importlib.import_module(modname)
            except Exception:
                # If the optional module can't be imported, skip it
                continue
            if hasattr(m, name):
                return getattr(m, name)

        raise AttributeError(f"module {__name__} has no attribute {name}")

    def __dir__():
        result = list(globals().keys())
        for modname in _lazy_modules:
            try:
                m = importlib.import_module(modname)
            except Exception:
                continue
            result.extend([n for n in dir(m) if not n.startswith("_")])
        if _has_run:
            result.append("run")
        return sorted(set(result))
