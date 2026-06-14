# Library api

This system manages databases of books and members for a library (server-side only)



## Create command for the Docker container required for this project

```
docker run --name library_api -e MYSQL_ROOT_PASSWORD=secret -e MYSQL_DATABASE=library_db -p3306:3306 -d mysql:8
```

## File structure
```
library-api/  
│  
├── app/  
│   ├── main.py  
│   ├── database/  
│   │   ├── db\_connection.py  
│   │   ├── book\_db.py  
│   │   └── member\_db.py  
│   ├── routes/  
│   │   ├── book\_routes.py  
│   │   ├── member\_routes.py  
│   │   └── report\_routes.py  
│   └── logs/  
│       └── app.log  
│  
├── README.md  
├── requirements.txt  
└── .gitignore
```


## Table structure


### books

|key   |   Value|
|---   | :---------------:|  
|`id`    |  master key|
|`title` | The title of the book|
|`author`| the author of the book|
|`genre` | The genre of the book|
|`is_available`| Is the book available for loan|
|`borrowed_by_member_id`| The ID of the member holding the book|


### members
key | value
:-- | :-- 
`id` | master key
`name`| member's name
`email`| email address
`is_active`| Is the member active
`total_borrows`|Total borrowings count




## system rules

|subject | role|
| :--    | :-----|
|Creating a book| User sends title/author/genre — system adds is_available=True, borrowed_by=NULL
|genre|Must be Fiction / Non-Fiction / Science / History / Other — any other value returns an error. Must be verified on both POST and PATCH.|
Create member| User sends name/email — system adds is_active=True, total_borrows=0|
email| Must be unique — if it already exists returns an error|
Inactive member|If is_active=False — book cannot be borrowed|
Book not available|It is not possible to borrow a book that is already borrowed (is_available=False)|
|Maximum books|A member cannot hold more than 3 books at a time|
|Returning a book|A book can only be returned if it is lent to the same friend who is returning it|









## Endpoints

|Endpoints | what is she doing|
|:----     | :--------        |
|POST /members| INSERT to the members table — is_active=True, total_borrows=0|
|GET /members|Returns a list of all members|
|GET /members/{id}|Returns one member by ID or None|
|PATCH /members/{id}|Updating submitted fields|
|PATCH /members/{id}/deactivate|Updates is_active=False|
|PATCH /members/{id}/activate|Updates is_active=True|
|PATCH /books/{id}/borrow/{member_id}|Increases the number of borrowed books by 1|
|GET /reports/summary|Count friends with is_active=True|
|GET /reports/top-member|Returns the member with the highest total_borrows|
|POST /books| Creating a book|
|GET /books|All the books|
|GET /books/{id}|Book by ID|
|PATCH /books/{id}|Book update|
|PATCH /books/{id}/return/{member_id}|Returning a book from a member |
|PATCH /books/{id}/borrow/{member_id}|Lending a book to a member|




## flow
HTTP Request -> FastAPI Endpoint -> Database Function -> Database

## Running instructions
1.  run this on your CMD

    ```
    docker run --name library_api -e MYSQL_ROOT_PASSWORD=secret -e MYSQL_DATABASE=library_db -p3306:3306 -d mysql:8
    ```
2.  open the CMD on your library-api dir end run the next commend

    ```
    python -m venv venv
    ```
3. now run this in the same location in the terminal
    ```
    venv\Scripts\activate
    ```
4. now you can install the requirements only on the ven
    ```
    pip install -r requirements.txt
    ```
5. the project is ready, now you can run it with
    ```
    python main.py
    ```