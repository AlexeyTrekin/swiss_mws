from fastapi import APIRouter, Request, Depends

router = APIRouter()

""" 
Secretary route is part of API that is dedicated to Secretary table at each tournament area

They are allowed:
 - to get the list of fights - either bound to their particular area, or any;
 - to send the results of any fight
 
 The secretary is authenticated by token given by administrator
"""


@router.get("/fights/")
def list_fights(request: Request):
    # get all fights
    return


@router.get("/fights/ready")
def list_ready_fights(request: Request):
    # get all fights that are ready for conduction, but not taken yet
    return


@router.get("/fights/my")
def list_my_fights(request: Request):
    # get all fights that are assigned to the current secretary
    return


@router.get("/fights/{id}")
def get_fight(request: Request):
    # get a particular fight data
    return


@router.post("/fights/{id}/acquire")
def take_fight():
    """
    hold the fight, designating that this fight is now conducted on the particular area, and cannot be taken elsewhere
    """
    return


@router.post("/fights/{id}/release")
def release_fight():
    """
    Return the fight back to the pool with specific result.
    """
    return
