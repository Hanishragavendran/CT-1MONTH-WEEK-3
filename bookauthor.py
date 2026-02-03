from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# 1. Our "Database"
books_db = [
    {"id": 1, "title": "The Hobbit", "author": "J.R.R. Tolkien", "read": True},
    {"id": 2, "title": "Atomic Habits", "author": "James Clear", "read": False}
]

# 2. The Model (The 'Rules' for our data)
class Book(BaseModel):
    id: int
    title: str 
    author: str
    read: bool = False

# --- THE 6 ENDPOINTS ---

# 1. READ ALL: Get every book in the list
@app.get("/books")
def get_all_books():
    return books_db

# 5. FILTER: Search for books by author (Query Param)
@app.get("/books/search")
def search_author(author: str):
    results = [b for b in books_db if author.lower() in b["author"].lower()]
    return {"results": results}

# 2. READ ONE: Get a specific book using its ID
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# 3. CREATE: Add a new book to the list
@app.post("/books")
def add_book(new_book: Book):
    books_db.append(new_book.dict())
    return {"message": "Book added successfully!"}

# 4. UPDATE: Change the info of an existing book
@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books_db):
        if book["id"] == book_id:
            books_db[index] = updated_book.dict()
            return {"message": "Book updated"}
    raise HTTPException(status_code=404, detail="Book not found")



# 6. DELETE: Remove a book from the list
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books_db):
        if book["id"] == book_id:
            books_db.pop(index)
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")