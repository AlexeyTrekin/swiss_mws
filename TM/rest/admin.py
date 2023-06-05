from fastapi import APIRouter, Request

"""
Admin route is for setup of the tournament.

Admin can:
- setup stages, move fighters to playoffs and finals, etc.
todo: - add or remove fighters
todo: - add or remove secretary tables
-
??

"""

router = APIRouter()


@router.post("/admin/round")
def setup_stage(request: Request):
    """
    Setup a tournament stage (set the current stage as finished and setup the next one)

    It can be either next round inside swiss system, or pass to the next stage like playoff.
    """
    return
