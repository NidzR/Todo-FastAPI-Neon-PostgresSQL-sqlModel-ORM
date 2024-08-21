from typing import Optional
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, SQLModel, create_engine, Session
from pydantic import BaseModel

class Todos(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    is_complete: bool = Field(default=False)

class User_Data(BaseModel):
    content: str
    is_complete: bool = False
db_url = "postgresql://neondb_owner:9lRuZk0KUIaM@ep-twilight-haze-a5tdjjhe.us-east-2.aws.neon.tech/neondb?sslmode=require"
engine = create_engine(db_url, echo=True)

def create_table():
    SQLModel.metadata.create_all(engine)

def insert_data_into_table(content: str):
    with Session(engine) as session:
        data = Todos(content="Coding")
        session.add(data)
        session.commit()
app = FastAPI(
    title="prac-todo App"
)
@app.get("/")
def route_root():
    return {"message": "Todo App"}
@app.post("/todos")
def add_todos_route(user_todos: User_Data):
    if user_todos.content:
        return {"message": "Todos Added Successfully"}
    else:
        raise HTTPException(status_code=404, detail="No todos found")
