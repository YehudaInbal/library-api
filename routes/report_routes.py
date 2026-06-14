from fastapi import APIRouter, Query
from database.book_db import BookDB
from database.member_db import Members

router = APIRouter()


@router.get("/summary")
def get_summary():
    return{
    'amount_of_book': BookDB.count_books_total(),
    'available_books': BookDB.count_available_books(),
    'borrowed_books': BookDB.count_borrowed_books(),
    'active_members': Members.count_active_members()
    }
@router.get("/books-by-genre")
def book_by_genre(genre: str):
    return BookDB.count_by_genre(genre)

@router.get("/top-member")
def get_top_member():
    return Members.get_top_member()