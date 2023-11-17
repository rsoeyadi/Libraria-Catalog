from fastapi import FastAPI
import uvicorn
import pymysql
from pydantic import BaseModel, Field
from typing import Optional


class Book(BaseModel):
    isbn: str = Field(..., max_length=50)
    title: str = Field(..., max_length=45)
    author: str = Field(..., max_length=45)
    genre: str = Field(..., max_length=45)
    category: str = Field(..., max_length=45)
    edition: str = Field(..., max_length=45)
    status: str = Field(..., max_length=45)
    transaction_id: Optional[str] = Field(default=None, max_length=45)


# Set the database credentials
host = 'database-1.cwruyiuygx34.us-east-2.rds.amazonaws.com'
port = 3306
user = 'admin'
password = 'password'
database = 'library_system'

# Connect to the database
connection = pymysql.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)
app = FastAPI()


# The response model is a list of strings since you're only returning titles
@app.get("/books/titles", response_model=list[str])
async def get_book_titles():
    # Using a with statement ensures the cursor is closed automatically
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        # Select only the 'title' column
        cursor.execute("SELECT title FROM books")
        result = cursor.fetchall()  # Fetch all the results
        # Extract the titles from the result
        titles = [row["title"] for row in result]
    return titles


@app.get("/")
async def root():
    return {"message": "This microservice is for our library catalog."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
