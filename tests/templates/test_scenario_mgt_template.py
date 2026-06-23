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

import os

from cookiecutter.main import cookiecutter


def test_scenario_management_with_toml_config(tmpdir):
    cookiecutter(
        template="taipy/templates/sdm",
        output_dir=tmpdir,
        no_input=True,
        extra_context={
            "Application root folder": "foo_app",
            "Application main Python file": "main.py",
            "Application title": "bar",
            "With TOML Config?": "yes",
        },
    )

    assert os.listdir(tmpdir) == ["foo_app"]
    assert sorted(os.listdir(os.path.join(tmpdir, "foo_app"))) == sorted(
        ["requirements.txt", ".taipyignore", "main.py", "algos", "config", "pages"]
    )

    assert sorted(os.listdir(os.path.join(tmpdir, "foo_app", "config"))) == sorted(
        ["__init__.py", "config.py", "config.toml"]
    )
    with open(os.path.join(tmpdir, "foo_app", "config", "config.py")) as config_file:
        assert 'Config.load("config/config.toml")' in config_file.read()

    # Try to run the generated application in a way that surfaces import errors and
    # attempts to run it as a module (python -m <package>.main) first, then as a
    # script if needed. Capture stdout/stderr and include them in assertion
    # diagnostics to help CI debugging when imports fail.
    import subprocess
    import sys

    taipy_path = os.getcwd()
    app_dir = os.path.join(tmpdir, "foo_app")
    module_name = os.path.basename(app_dir)

    stdout = ""
    # First attempt: run as module so relative imports inside the package succeed
    try:
        res = subprocess.run(
            [sys.executable, "-m", f"{module_name}.main"],
            cwd=taipy_path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        stdout = (res.stdout or "") + (res.stderr or "")
    except subprocess.TimeoutExpired as e:
        # Capture partial output if any
        stdout = (e.stdout or "") + (e.stderr or "")
    except Exception:
        stdout = ""

    # If running as a module failed (non-zero exit) or produced no output,
    # try running the script directly from the app folder to collect error details.
    if (
        not stdout
        or ("Traceback (most recent call last)" in stdout and "ImportError" in stdout)
        or ("ModuleNotFoundError" in stdout)
    ):
        try:
            res2 = subprocess.run(
                [sys.executable, "main.py"],
                cwd=app_dir,
                capture_output=True,
                text=True,
                timeout=5,
            )
            stdout = (res2.stdout or "") + (res2.stderr or "")
        except subprocess.TimeoutExpired as e:
            stdout = (e.stdout or "") + (e.stderr or "")
        except Exception:
            stdout = stdout or ""

    # Assert the message when the application is run successfully is in the stdout
    assert (
        "[Taipy][INFO] Configuration 'config/config.toml' successfully loaded." in stdout
    ), f"Expected Taipy configuration load message in stdout. Output:\n{stdout}"
    assert (
        "[Taipy][INFO]  * Server starting on" in stdout
    ), f"Expected Taipy server starting message in stdout. Output:\n{stdout}"


def test_scenario_management_without_toml_config(tmpdir):
    cookiecutter(
        template="taipy/templates/sdm",
        output_dir=tmpdir,
        no_input=True,
        extra_context={
            "Application root folder": "foo_app",
            "Application main Python file": "main.py",
            "Application title": "bar",
            "With TOML Config?": "no",
        },
    )

    assert os.listdir(tmpdir) == ["foo_app"]
    assert sorted(os.listdir(os.path.join(tmpdir, "foo_app"))) == sorted(
        ["requirements.txt", ".taipyignore", "main.py", "algos", "config", "pages"]
    )

    assert sorted(os.listdir(os.path.join(tmpdir, "foo_app", "config"))) == sorted(["__init__.py", "config.py"])
    with open(os.path.join(tmpdir, "foo_app", "config", "config.py")) as config_file:
        config_content = config_file.read()
        assert 'Config.load("config/config.toml")' not in config_content
        assert all(x in config_content for x in ["Config.configure_csv_data_node", "Config.configure_task"])

    # Try to run the generated application in a way that surfaces import errors and
    # attempts to run it as a module (python -m <package>.main) first, then as a
    # script if needed. Capture stdout/stderr and include them in assertion
    # diagnostics to help CI debugging when imports fail.
    import subprocess
    import sys

    taipy_path = os.getcwd()
    app_dir = os.path.join(tmpdir, "foo_app")
    module_name = os.path.basename(app_dir)

    stdout = ""
    try:
        res = subprocess.run(
            [sys.executable, "-m", f"{module_name}.main"],
            cwd=taipy_path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        stdout = (res.stdout or "") + (res.stderr or "")
    except subprocess.TimeoutExpired as e:
        stdout = (e.stdout or "") + (e.stderr or "")
    except Exception:
        stdout = ""

    if (
        not stdout
        or ("Traceback (most recent call last)" in stdout and "ImportError" in stdout)
        or ("ModuleNotFoundError" in stdout)
    ):
        try:
            res2 = subprocess.run(
                [sys.executable, "main.py"],
                cwd=app_dir,
                capture_output=True,
                text=True,
                timeout=5,
            )
            stdout = (res2.stdout or "") + (res2.stderr or "")
        except subprocess.TimeoutExpired as e:
            stdout = (e.stdout or "") + (e.stderr or "")
        except Exception:
            stdout = stdout or ""

    # Assert the message when the application is run successfully is in the stdout
    assert (
        "[Taipy][INFO]  * Server starting on" in stdout
    ), f"Expected Taipy server starting message in stdout. Output:\n{stdout}"


def test_with_git(tmpdir):
    cookiecutter(
        template="taipy/templates/sdm",
        output_dir=str(tmpdir),
        no_input=True,
        extra_context={
            "Application root folder": "foo_app",
            "With a new Git repository?": "y",
        },
    )

    assert os.listdir(tmpdir) == ["foo_app"]
    assert sorted(os.listdir(os.path.join(tmpdir, "foo_app"))) == sorted(
        ["requirements.txt", "main.py", ".git", ".gitignore", ".taipyignore", "algos", "config", "pages"]
    )
