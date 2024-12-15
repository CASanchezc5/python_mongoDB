from fastapi import FastAPI,HTTPException
from pymongo import MongoClient
from bson import ObjectId
from models import Book

app = FastAPI()

#client = MongoClient("mongodb+srv://<your_username>:<your_password>@<your_cluster>.mongodb.net/<your_database>?retryWrites=true&w=majority") -> es el cliente al cual nos vamos a conectar de forma remota
client = MongoClient("mongodb://localhost:27017") # es el cliente al cual nos vamos a conectar de forma local

db = client["dblibrary"] # es la base de datos
collectionBook = db["books"]

# EndPoints o rutas
@app.get("/")
async def home():
    return {"message":"Inicio del Backend"}

# Guardar Libro
@app.post("/books", response_model=Book)
async def create_book(book: Book):
  book_dict = book.dict()
  collectionBook.insert_one(book_dict)
  return book


# Recuperar todos los libros
@app.get("/books")
async def get_books():
  books = []
  for book in collectionBook.find():
    books.append(Book(**book)) # LOS * hacen que se creen los pares key-values
  return books

# Recuperar libro por id
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: str):
  book = collectionBook.find_one({"_id": ObjectId(book_id)})
  if book:
    return Book(**book)
  else:
    raise HTTPException(status_code=404, detail="Libro no encontrado. Inténtelo con otro")
  
# Recuperar libro por title
@app.get("/books/bytitle/{title}", response_model=Book)
async def get_book_bytitle(title: str):
  book = collectionBook.find_one({"title": title})
  if book:
    return Book(**book)
  else:
    raise HTTPException(status_code=404, detail="Título no encontrado. Inténtelo con otro")
  
# Actualizar un libro por Id
@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: str, book: Book):
  book_dict = book.dict()
  collectionBook.update_one({"_id": ObjectId(book_id)}, {"$set": book_dict})
  return book

# Eliminar un libro por Id
@app.delete("/books/{book_id}")
async def delete_book(book_id: str):
  collectionBook.delete_one({"_id": ObjectId(book_id)})
  return {"message": "Libro borrado exitosamente"}