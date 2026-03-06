from fastapi import FastAPI, Body, Path, Query,HTTPException
from typing import Optional
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI()

class Book:
    id:int
    title:str
    author:str
    description: str
    rating:int
    published_date: int

    def __init__(self,id,title,author,description,rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

BOOKS = [
    Book(1,"Computer science","Codingwithroby","A very nice book",5, 2000),
    Book(2,"Be fast with FastAPI","Codingwithroby","A great book",5,2000),
    Book(3,"Master end points","Codingwithroby","Awsome book",5,2000), 
    Book(4,"HP1","Author 1 ","Book Description",2,2005),
    Book(5,"HP2","Author 2 ","Book Description",3,2005),
    Book(6,"HP3","Author 3 ","Book Description",1,2005),
]

class BookRequest(BaseModel):
    id: Optional[int] = Field(description= 'ID is not needed on CREATE', default=None)
    title: str = Field(min_length = 3)
    author:str = Field(min_length=1)
    description:str = Field(min_length=1,max_length=100)
    rating:int = Field(gt=0,lt=6)
    published_date:int = Field(gt=1900,lt=2031)
    
    model_config = {
        "json_schema_extra": {
           "example":{
               "title":"The title of a new book",
               "author":"The name of the author",
               "description":"A description of the book",
               "rating":"1-5 being 5 the highest",
               "published_date":"The year the book was published"
           }
        }
    }

@app.get("/books")
async def read_all_books():
    return BOOKS

#find a book based on the book_id
@app.get("/books/{book_id}")
async def read_book(book_id:int = Path(gt=0)): #Path parameter acts as a validation parameter to check the id gt 0 
    for book in BOOKS:
        if book.id==book_id:
            return book
    raise HTTPException(status_code=404, detail= 'Item not found')
        

#Fetch all the books based on the rating
@app.get("/books/rating/")
async def read_book_by_rating(book_rating:int = Query(gt=0,lt=6)): #the Query parameters substitute the if in the function
    books_to_return = []
    for book in BOOKS:
        #if book_rating>0 and book_rating<6:
        if book.rating == book_rating:
                books_to_return.append(book)
        #else:
        #return f"{book_rating} is not valid. Rating must be between 1 and 5"
    return books_to_return

#Fetch books by published_date
@app.get("/books/published/")
async def read_books_by_published_date(published_date:int=Query(gt=1900,lt=2031)):
    books_to_show = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_show.append(book)
    return books_to_show 

@app.post("/create_book")
async def create_book(book_request:BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    
#Update a book
@app.put("/books/updatebook/")
async def update_book(book:BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404,detail=('Item not found'))

#Delete method
@app.delete("/books/{book_id}")
async def delete_book(book_id:int = Path(gt=0)):
    book_deleted = False
    for i in range (len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_deleted = True
            break    
    if not book_deleted:
        raise HTTPException(status_code=404,detail='Book not found!')


def find_book_id(book:Book):
    if len(BOOKS)>0:
        book.id = BOOKS[-1].id + 1 
    else:
        book.id = 1
    ## or in just one line of code:
    # book.id = 1 if len(BOOKS)==0 else BOOKS[-1].id+1    
    return book
