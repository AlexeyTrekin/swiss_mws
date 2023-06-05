from typing import List
from uuid import UUID, uuid4

from ..rest.json import CreateTournamentInput
from ..repo import tournament_repo
from ..model.status import Status
from .stage_service import create_stage
from .fighter_service import create_fighter
from ..errors import TMError


def create_tournament(tournament: CreateTournamentInput):
    tournament_id = uuid4()
    dto = tournament_repo.TournamentDTO(id=tournament_id,
                        status=Status.planned)
    tournament_repo.add_tournament(dto=dto)

    for fighter in tournament.fighters:
        create_fighter(fighter)

    for stage in tournament.stages:
        stage.tournament_id = tournament_id
        create_stage(stage)

    return tournament_id


def start_tournament(tournament_id):
    dto = tournament_repo.get_tournament(tournament_id)
    if dto.status != Status.planned:
        raise TMError("Tournament status must be `planned` before start")
    tournament_repo.update_tournament_status(tournament_id=tournament_id,
                                             status=Status.going)
    active_stage = get_active_stage()
    active_stage.calculate_pairs()