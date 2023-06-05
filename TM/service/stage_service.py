from uuid import uuid4, UUID
from ..model.status import Status
from ..rest.json import CreateStageInput
from ..repo.stage_repo import StagetDTO, add_stage, update_stage
from .rules_service import create_ruleset


class CreateStageError(ValueError):
    pass


def create_stage(stage: CreateStageInput):
    if not stage.ruleset_id:
        if not stage.ruleset:
            raise CreateStageError("Either ruleset ID or ruleset input must be present")
        ruleset_id = create_ruleset(stage.ruleset)
    else:
        ruleset_id = stage.ruleset_id
    stage_id = uuid4()
    add_stage(StagetDTO(id=stage_id,
                    tournament_id=stage.tournament_id,
                    ruleset_id=ruleset_id,
                    status=Status.planned))
    return stage_id


def start_stage(stage_id: UUID):
    pass


def finish_stage(stage: UUID):
    pass


def final_standings(stage: UUID):
    pass
