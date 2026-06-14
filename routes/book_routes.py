from fastapi import APIRouter, HTTPException
from database.book_db import BookDB

router = APIRouter()


@router.post("", status_code=201)
def add_book(data:dict):
    try:
        return BookDB.add_book(data)
    except KeyError as e:
        raise HTTPException(status_code=422, detail=f"{e}")


@router.get("")
def get_all_books() -> list:
    return BookDB.get_all_book()

@router.get("/{id}")
def get_book(id:int):
    book = BookDB.get_book_by_id(id)
    if not book:
        raise HTTPException(status_code=404, detail="There is no book with this ID")
    else:
        return book

@router.patch("/{id}")
def update_book(data:dict, id:int):
    try:
        return BookDB.update_book(data, id)
    except ValueError:
        raise HTTPException(status_code=404, detail="There is no book with this ID")
    except KeyError as e:
        raise HTTPException(status_code=422, detail=f"{e}")

@router.patch("/{id}/borrow/{member_id}")
def borrow_book(id:int, member_id:int):
    details = BookDB.borrow_book(id, member_id)
    return details

@router.patch("/{id}/return/{member_id}")
def return_book(id:int, member_id:int):
    details = BookDB.return_book(id, member_id)
    return details