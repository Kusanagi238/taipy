# Copyright 2021-2025 Avaiga Private Limited

# Provide a minimal fallback for pkg_resources if it's not available in the environment
# Some third-party packages import pkg_resources at import time; in minimal test environments
# pkg_resources (from setuptools) may be missing and cause import-time failures. This shim
# injects a lightweight module that implements the small surface area commonly used
# (e.g. get_distribution().version) so imports don't crash during test collection.
try:
    import pkg_resources  # type: ignore
except Exception:
    import sys
    import types

    _pkg = types.ModuleType("pkg_resources")

    def get_distribution(name):
        class _Dist:
            version = "0.0.0"
        return _Dist()

    _pkg.get_distribution = get_distribution
    # Optionally provide a minimal Requirement parser if some code uses it
    def Requirement(x):
        return x
    _pkg.Requirement = Requirement

    sys.modules["pkg_resources"] = _pkg

#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
