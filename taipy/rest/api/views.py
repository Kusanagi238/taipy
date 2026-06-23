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

from flask import Blueprint, current_app
from flask_restful import Api

from taipy.common._modules import EnterpriseEdition
from taipy.common.logger._taipy_logger import _TaipyLogger
from taipy.core.common._utils import _load_fct

try:
    # apispec is an optional extension; importing it at module import time can
    # trigger heavy dependency resolution in some environments (e.g. apispec_webframeworks
    # importing pkg_resources). Import lazily / tolerate failure to avoid
    # breaking test collection or environments where the optional dependency
    # is not installed.
    from ..extensions import apispec
except Exception:
    apispec = None

from .resources import (
    CycleList,
    CycleResource,
    DataNodeList,
    DataNodeReader,
    DataNodeResource,
    DataNodeWriter,
    JobExecutor,
    JobList,
    JobResource,
    ScenarioExecutor,
    ScenarioList,
    ScenarioResource,
    SequenceExecutor,
    SequenceList,
    SequenceResource,
    TaskExecutor,
    TaskList,
    TaskResource,
)
from .schemas import CycleSchema, DataNodeSchema, JobSchema, ScenarioSchema, SequenceSchema, TaskSchema

_logger = _TaipyLogger._get_logger()


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

# Defer creation of the Api instance and registration of resources until the
# blueprint is actually registered on an application. Using blueprint.record
# ensures these side-effects do not run at import time, avoiding failures when
# optional runtime dependencies are missing during test collection.


def _setup_api(state):
    api = Api(blueprint)

    api.add_resource(
        DataNodeResource,
        "/datanodes/<string:datanode_id>/",
        endpoint="datanode_by_id",
        resource_class_kwargs={"logger": _logger},
    )

    api.add_resource(
        DataNodeReader,
        "/datanodes/<string:datanode_id>/read/",
        endpoint="datanode_reader",
        resource_class_kwargs={"logger": _logger},
    )

    api.add_resource(
        DataNodeWriter,
        "/datanodes/<string:datanode_id>/write/",
        endpoint="datanode_writer",
        resource_class_kwargs={"logger": _logger},
    )

    api.add_resource(
        DataNodeList,
        "/datanodes/",
        endpoint="datanodes",
        resource_class_kwargs={"logger": _logger},
    )

    api.add_resource(
        TaskResource,
        "/tasks/<string:task_id>/",
        endpoint="task_by_id",
        resource_class_kwargs={"logger": _logger},
    )

    api.add_resource(TaskList, "/tasks/", endpoint="tasks", resource_class_kwargs={"logger": _logger})
    api.add_resource(
        TaskExecutor,
        "/tasks/submit/<string:task_id>/",
        endpoint="task_submit",
        resource_class_kwargs={"logger": _logger},
    )

    api.add_resource(
        SequenceResource,
        "/sequences/<string:sequence_id>/",
        endpoint="sequence_by_id",
        resource_class_kwargs={"logger": _logger},
    )
    api.add_resource(
        SequenceList,
        "/sequences/",
        endpoint="sequences",
        resource_class_kwargs={"logger": _logger},
    )
    api.add_resource(
        SequenceExecutor,
        "/sequences/submit/<string:sequence_id>/",
        endpoint="sequence_submit",
        resource_class_kwargs={"logger": _logger},
    )

    api.add_resource(
        ScenarioResource,
        "/scenarios/<string:scenario_id>/",
        endpoint="scenario_by_id",
        resource_class_kwargs={"logger": _logger},
    )
    api.add_resource(
        ScenarioList,
        "/scenarios/",
        endpoint="scenarios",
        resource_class_kwargs={"logger": _logger},
    )
    api.add_resource(
        ScenarioExecutor,
        "/scenarios/submit/<string:scenario_id>/",
        endpoint="scenario_submit",
        resource_class_kwargs={"logger": _logger},
    )

    api.add_resource(
        CycleResource,
        "/cycles/<string:cycle_id>/",
        endpoint="cycle_by_id",
        resource_class_kwargs={"logger": _logger},
    )
    api.add_resource(
        CycleList,
        "/cycles/",
        endpoint="cycles",
        resource_class_kwargs={"logger": _logger},
    )

    api.add_resource(
        JobResource,
        "/jobs/<string:job_id>/",
        endpoint="job_by_id",
        resource_class_kwargs={"logger": _logger},
    )
    api.add_resource(JobList, "/jobs/", endpoint="jobs", resource_class_kwargs={"logger": _logger})
    api.add_resource(
        JobExecutor,
        "/jobs/cancel/<string:job_id>/",
        endpoint="job_cancel",
        resource_class_kwargs={"logger": _logger},
    )

    # Load enterprise-only resources once the Api is created
    load_enterprise_resources(api)


# Register the setup function to be called when the blueprint is registered
# on an application. This defers all Api/resource creation to that moment.
blueprint.record(_setup_api)


def register_views():
    apispec.spec.components.schema("DataNodeSchema", schema=DataNodeSchema)  # type: ignore[reportOptionalMemberAccess]
    apispec.spec.path(view=DataNodeResource, app=current_app)  # type: ignore[reportOptionalMemberAccess]
    apispec.spec.path(view=DataNodeList, app=current_app)  # type: ignore[reportOptionalMemberAccess]
    apispec.spec.path(view=DataNodeReader, app=current_app)  # type: ignore[reportOptionalMemberAccess]
    apispec.spec.path(view=DataNodeWriter, app=current_app)  # type: ignore[reportOptionalMemberAccess]

    apispec.spec.components.schema("TaskSchema", schema=TaskSchema)  # type: ignore[reportOptionalMemberAccess]
    apispec.spec.path(view=TaskResource, app=current_app)  # type: ignore[reportOptionalMemberAccess]
    apispec.spec.path(view=TaskList, app=current_app)  # type: ignore[reportOptionalMemberAccess]
    apispec.spec.path(view=TaskExecutor, app=current_app)  # type: ignore[reportOptionalMemberAccess]

    apispec.spec.components.schema("SequenceSchema", schema=SequenceSchema)  # type: ignore[reportOptionalMemberAccess]
    apispec.spec.path(view=SequenceResource, app=current_app)  # type: ignore[reportOptionalMemberAccess]
    apispec.spec.path(view=SequenceList, app=current_app)  # type: ignore[reportOptionalMemberAccess]
    apispec.spec.path(view=SequenceExecutor, app=current_app)  # type: ignore[reportOptionalMemberAccess]

    apispec.spec.components.schema("ScenarioSchema", schema=ScenarioSchema)  # type: ignore[reportOptionalMemberAccess]
    apispec.spec.path(view=ScenarioResource, app=current_app)  # type: ignore[reportOptionalMemberAccess]
    apispec.spec.path(view=ScenarioList, app=current_app)  # type: ignore[reportOptionalMemberAccess]
    apispec.spec.path(view=ScenarioExecutor, app=current_app)  # type: ignore[reportOptionalMemberAccess]

    apispec.spec.components.schema("CycleSchema", schema=CycleSchema)  # type: ignore[reportOptionalMemberAccess]
    apispec.spec.path(view=CycleResource, app=current_app)  # type: ignore[reportOptionalMemberAccess]
    apispec.spec.path(view=CycleList, app=current_app)  # type: ignore[reportOptionalMemberAccess]

    apispec.spec.components.schema("JobSchema", schema=JobSchema)  # type: ignore[reportOptionalMemberAccess]
    apispec.spec.path(view=JobResource, app=current_app)  # type: ignore[reportOptionalMemberAccess]
    apispec.spec.path(view=JobList, app=current_app)  # type: ignore[reportOptionalMemberAccess]
    apispec.spec.path(view=JobExecutor, app=current_app)  # type: ignore[reportOptionalMemberAccess]

    apispec.spec.components.schema(  # type: ignore[reportOptionalMemberAccess]
        "Any",
        {
            "description": "Any value",
            "nullable": True,
        },
    )

    if EnterpriseEdition._is_installed():
        _register_views = _load_fct("taipy.enterprise.rest.api.views", "_register_views")
        _register_views(apispec)
