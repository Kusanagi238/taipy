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

from importlib.util import find_spec

if find_spec("taipy"):
    if find_spec("taipy.common") and find_spec("taipy.common.config"):
        from taipy.common.config._init import *

    if find_spec("taipy.gui"):
        import importlib
        _taipy_lazy_modules = globals().setdefault("_taipy_lazy_modules", {})
        _taipy_lazy_modules["taipy.gui._init"] = None
        if "__getattr__" not in globals():
            def __getattr__(name):
                import importlib as _importlib
                for _mod_name in tuple(globals().get("_taipy_lazy_modules", {})):
                    _cached = globals()["_taipy_lazy_modules"].get(_mod_name)
                    if _cached is None:
                        try:
                            _cached = _importlib.import_module(_mod_name)
                        except Exception:
                            continue
                        globals()["_taipy_lazy_modules"][_mod_name] = _cached
                    if hasattr(_cached, name):
                        return getattr(_cached, name)
                raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    if find_spec("taipy.core"):
        from taipy.core._init import *

    if find_spec("taipy.rest"):
        import importlib
        _taipy_lazy_modules = globals().setdefault("_taipy_lazy_modules", {})
        _taipy_lazy_modules["taipy.rest._init"] = None
        if "__getattr__" not in globals():
            def __getattr__(name):
                import importlib as _importlib
                for _mod_name in tuple(globals().get("_taipy_lazy_modules", {})):
                    _cached = globals()["_taipy_lazy_modules"].get(_mod_name)
                    if _cached is None:
                        try:
                            _cached = _importlib.import_module(_mod_name)
                        except Exception:
                            continue
                        globals()["_taipy_lazy_modules"][_mod_name] = _cached
                    if hasattr(_cached, name):
                        return getattr(_cached, name)
                raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    if find_spec("taipy.gui_core"):
        from taipy.gui_core._init import *

    if find_spec("taipy.enterprise"):
        from taipy.enterprise._init import *

    if find_spec("taipy.designer"):
        from taipy.designer._init import *

    if find_spec("taipy._run"):
        from taipy._run import _run as run
