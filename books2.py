from fastapi import FastAPI, Body
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

    def __init__(self,id,title,author,description,rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

BOOKS = [
    Book(1,"Computer science","Codingwithroby","A very nice book",5),
    Book(2,"Be fast with FastAPI","Codingwithroby","A great book",5),
    Book(3,"Master end points","Codingwithroby","Awsome book",5), 
    Book(4,"HP1","Author 1 ","Book Description",2),
    Book(5,"HP2","Author 2 ","Book Description",3),
    Book(6,"HP3","Author 3 ","Book Description",1),
]

class BookRequest(BaseModel):
    id: Optional[int] = Field(description= 'ID is not needed on CREATE', default=None)
    title: str = Field(min_length = 3)
    author:str = Field(min_length=1)
    description:str = Field(min_length=1,max_length=100)
    rating:int = Field(gt=0,lt=6)
    
    model_config = {
        "json_schema_extra": {
           "example":{
               "title":"The title of a new book",
               "author":"The name of the author",
               "description":"A description of the book",
               "rating":"1-5 being 5 the highest"
           }
        }
    }

@app.get("/books")
async def read_all_books():
    return BOOKS

#find a book based on the book_id
@app.get("/books/{book_id}")
async def read_book(book_id:int):
    for book in BOOKS:
        if book.id==book_id:
            return book

#Fetch all the books based on the rating
@app.get("/books/")
async def read_book_by_rating(book_rating:int):
    books_to_return = []
    for book in BOOKS:
        if book_rating>0 and book_rating<6:
            if book.rating == book_rating:
                books_to_return.append(book)
            else:
                print("Rating must be between 1 and 5")
        return books_to_return

@app.post("/create_book")
async def create_book(book_request:BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    
def find_book_id(book:Book):
    if len(BOOKS)>0:
        book.id = BOOKS[-1].id + 1 
    else:
        book.id = 1
    ## or in just one line of code:
    # book.id = 1 if len(BOOKS)==0 else BOOKS[-1].id+1    
    return book
