from fastapi import APIRouter, HTTPException
from database.member_db import Members


router = APIRouter()


@router.post("", status_code=201)
def add_member(data:dict):
    try:
        id = Members.add_member(data)
        return id
    except ValueError as e:
        raise HTTPException(status_code=409, detail=f"{e}")
    
@router.get("")
def get_all_members():
    members = Members.get_all_members()
    return members

@router.get("/{id}")
def get_member(id:int):
    member = Members.get_member_by_id(id)
    if not member:
        raise HTTPException(status_code=404, detail="No matching member id")
    else:
        return member

@router.patch("/{id}")
def update_member(data:dict, id:int):
    member = Members.get_member_by_id(id)
    if not member:
        raise HTTPException(status_code=404, detail="No matching member id")
    try:
        update = Members.update_member(data, id)
        if not update:
            return False
        else:
            return update
    except KeyError as e:
        raise HTTPException(status_code=409, detail=f"{e}")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"{e}")


@router.patch("/{id}/deactivate")
def deactivate_member(id:int):
    try:
        return Members.deactivate_member(id)
    except ValueError:
        raise HTTPException(status_code=404, detail="No matching member id")


@router.patch("/{id}/activate")
def activate_member(id:int):
    try:
        return Members.activate_member(id)
    except ValueError:
        raise HTTPException(status_code=404, detail="No matching member id")