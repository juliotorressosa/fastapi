from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

BOOKS = [
    {'title':'Title One', 'author':'Author One', 'category':'science'},
    {'title':'Title Two', 'author':'Author Two', 'category':'science'},
    {'title':'Title Three', 'author':'Author Three', 'category':'history'},
    {'title':'Title Four', 'author':'Author Four', 'category':'math'},
    {'title':'Title Five', 'author':'Author Five', 'category':'math'},
    {'title':'Title Six', 'author':'Author Two', 'category':'math'},
]


@app.get("/")
async def first_api():
    return {"message": "Hello Julio"}

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{dynamic_param}")
async def read_all_books(dynamic_param:str):
    return{'dynamic_param':dynamic_param}


#This function will fetch the books by title dynamically
@app.get("/books/{book_title}")
async def read_book(book_title:str):
    for book in BOOKS:
        if book.get('title').casfold() == book_title.casefold():
            return book
        
#This function will fetch all the books by parameter 'category'
@app.get("/books/")
async def read_category_by_query(category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# Thiss function will fetch all the books by parameter 'author'and 'category'
@app.get("/books/{book_author}")
async def read_books_by_author_and_category(book_author: str, book_category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == book_category.casefold():
            books_to_return.append(book)
    return books_to_return

### POST the create command
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    
## PUT the UPDATE command
@app.put("/books/uptdate_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
             BOOKS.pop(i)
             break
         
