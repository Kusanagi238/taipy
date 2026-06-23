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

import argparse

# Lazily import taipy modules to avoid importing third-party dependencies
# at pytest collection time which can cause ModuleNotFoundError for optional
# packages (e.g. pkg_resources). The LazyObject will import the real object
# on first use during test execution.
import importlib
import typing as t

import pytest


class _LazyObject:
    def __init__(self, module: str, attr: str):
        self._module = module
        self._attr = attr
        self._obj = None

    def _load(self):
        if self._obj is None:
            mod = importlib.import_module(self._module)
            self._obj = getattr(mod, self._attr)

    def __call__(self, *args, **kwargs):
        self._load()
        return self._obj(*args, **kwargs)

    def __getattr__(self, name):
        self._load()
        return getattr(self._obj, name)

    def __repr__(self):
        if self._obj is None:
            return f"<LazyObject {self._module}.{self._attr}>"
        return repr(self._obj)


def _lazy(module: str, attr: str):
    return _LazyObject(module, attr)


_TaipyParser = _lazy("taipy.common._cli._base_cli._taipy_parser", "_TaipyParser")
Config = _lazy("taipy.common.config", "Config")
_inject_section = _lazy("taipy.common.config", "_inject_section")
_Config = _lazy("taipy.common.config._config", "_Config")
_ConfigComparator = _lazy("taipy.common.config._config_comparator._config_comparator", "_ConfigComparator")
_BaseSerializer = _lazy("taipy.common.config._serializer._base_serializer", "_BaseSerializer")
_TomlSerializer = _lazy("taipy.common.config._serializer._toml_serializer", "_TomlSerializer")
_Checker = _lazy("taipy.common.config.checker._checker", "_Checker")
IssueCollector = _lazy("taipy.common.config.checker.issue_collector", "IssueCollector")
CoreSection = _lazy("taipy.core.config", "CoreSection")
DataNodeConfig = _lazy("taipy.core.config", "DataNodeConfig")
JobConfig = _lazy("taipy.core.config", "JobConfig")
ScenarioConfig = _lazy("taipy.core.config", "ScenarioConfig")
TaskConfig = _lazy("taipy.core.config", "TaskConfig")
RestConfig = _lazy("taipy.rest.config", "RestConfig")


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom command line options for pytest."""
    parser.addoption("--e2e-base-url", action="store", default="/", help="base url for e2e testing")
    parser.addoption("--e2e-port", action="store", default="5000", help="port for e2e testing")


@pytest.fixture(scope="session")
def e2e_base_url(request: pytest.FixtureRequest) -> str:
    """Fixture to get the base URL for e2e testing."""
    return request.config.getoption("--e2e-base-url")


@pytest.fixture(scope="session")
def e2e_port(request: pytest.FixtureRequest) -> str:
    """Fixture to get the port for e2e testing."""
    return request.config.getoption("--e2e-port")


def remove_subparser(name: str) -> None:
    """Remove a subparser from argparse."""
    _TaipyParser._sub_taipyparsers.pop(name, None)

    if _TaipyParser._subparser_action:
        _TaipyParser._subparser_action._name_parser_map.pop(name, None)

        for action in _TaipyParser._subparser_action._choices_actions:
            if action.dest == name:
                _TaipyParser._subparser_action._choices_actions.remove(action)


@pytest.fixture
def clean_argparser() -> t.Callable:
    """Fixture to clean the argument parser."""

    def _clean_argparser() -> None:
        _TaipyParser._parser = argparse.ArgumentParser(conflict_handler="resolve")
        _TaipyParser._subparser_action = None
        _TaipyParser._arg_groups = {}
        subcommands = list(_TaipyParser._sub_taipyparsers.keys())
        for subcommand in subcommands:
            remove_subparser(subcommand)

    return _clean_argparser


@pytest.fixture
def reset_configuration_singleton() -> t.Callable:
    """Fixture to reset the configuration singleton."""

    def _reset_configuration_singleton() -> None:
        Config.unblock_update()

        Config._default_config = _Config()._default_config()
        Config._python_config = _Config()
        Config._file_config = _Config()
        Config._env_file_config = _Config()
        Config._applied_config = _Config()
        Config._collector = IssueCollector()
        Config._serializer = _TomlSerializer()
        Config._comparator = _ConfigComparator()
        _BaseSerializer._SERIALIZABLE_TYPES = [
            "bool",
            "str",
            "int",
            "float",
            "datetime",
            "timedelta",
            "function",
            "class",
            "SECTION",
        ]
        _Checker._checkers = []

    return _reset_configuration_singleton


@pytest.fixture
def inject_core_sections() -> t.Callable:
    """Fixture to inject core sections into the configuration."""

    def _inject_core_sections() -> None:
        _inject_section(
            JobConfig,
            "job_config",
            JobConfig("development"),
            [("configure_job_executions", JobConfig._configure)],
            True,
        )
        _inject_section(
            CoreSection,
            "core",
            CoreSection.default_config(),
            [("configure_core", CoreSection._configure)],
            add_to_unconflicted_sections=True,
        )
        _inject_section(
            DataNodeConfig,
            "data_nodes",
            DataNodeConfig.default_config(),
            [
                ("configure_data_node", DataNodeConfig._configure),
                ("configure_data_node_from", DataNodeConfig._configure_from),
                ("set_default_data_node_configuration", DataNodeConfig._set_default_configuration),
                ("configure_csv_data_node", DataNodeConfig._configure_csv),
                ("configure_json_data_node", DataNodeConfig._configure_json),
                ("configure_sql_table_data_node", DataNodeConfig._configure_sql_table),
                ("configure_sql_data_node", DataNodeConfig._configure_sql),
                ("configure_mongo_collection_data_node", DataNodeConfig._configure_mongo_collection),
                ("configure_in_memory_data_node", DataNodeConfig._configure_in_memory),
                ("configure_pickle_data_node", DataNodeConfig._configure_pickle),
                ("configure_excel_data_node", DataNodeConfig._configure_excel),
                ("configure_generic_data_node", DataNodeConfig._configure_generic),
                ("configure_s3_object_data_node", DataNodeConfig._configure_s3_object),
            ],
        )
        _inject_section(
            TaskConfig,
            "tasks",
            TaskConfig.default_config(),
            [
                ("configure_task", TaskConfig._configure),
                ("set_default_task_configuration", TaskConfig._set_default_configuration),
            ],
        )
        _inject_section(
            ScenarioConfig,
            "scenarios",
            ScenarioConfig.default_config(),
            [
                ("configure_scenario", ScenarioConfig._configure),
                ("set_default_scenario_configuration", ScenarioConfig._set_default_configuration),
            ],
        )

    return _inject_core_sections


@pytest.fixture
def inject_rest_sections() -> t.Callable:
    """Fixture to inject core sections into the configuration."""

    def _inject_rest_sections() -> None:
        _inject_section(
            RestConfig,
            "rest",
            default=RestConfig.default_config(),
            configuration_methods=[("configure_rest", RestConfig._configure_rest)],
        )

    return _inject_rest_sections
