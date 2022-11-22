from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import dcr, user, auth, vote
from config import settings

# generate DB tables when the server is started up for the first time
# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dcr.router)

app.include_router(user.router)

app.include_router(auth.router)

app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "hello world prod"}

# class DCR(BaseModel):
#     language: str
#     source: str
#     ticket_number: str
#     emails: Optional[int] = 0
#     calls: Optional[int] = 0
#     chats: Optional[int] = 0

# class DCRResponse(DCR):
#     created_at: datetime

#     # to automaticaly convert to dict and avoid error during API calling
#     class Config:
#         orm_mode = True


# @app.get('/dcr', response_model=List[DCRResponse])
# def get_all_items(db: Session = Depends(get_db)):
#     # cursor.execute("""SELECT * FROM dcr_entries """)
#     # dcr_entries = cursor.fetchall()
#     dcr_entries = db.query(models.DCR).all()
#     return dcr_entries

# @app.post('/dcr', status_code=status.HTTP_201_CREATED, response_model=DCRResponse)
# def create_dcr(dcr: DCR, db: Session = Depends(get_db)):
#     # cursor.execute("""INSERT INTO dcr_entries (language, source, ticket_number, calls, emails, chats)
#     # VALUES (%s, %s, %s, %s, %s, %s) RETURNING *""", (dcr.language, dcr.source, dcr.ticket_number, dcr.calls, dcr.emails, dcr.chats))
#     # new_dcr = cursor.fetchone()
#     # conn.commit()
#     new_dcr = models.DCR(**dcr.dict())
#     db.add(new_dcr)
#     db.commit()
#     db.refresh(new_dcr)
#     return new_dcr


# @app.get('/dcr/{id}', response_model=DCRResponse)
# def get_one_item(id: int, db: Session = Depends(get_db)):
#     # cursor.execute("""SELECT * FROM dcr_entries WHERE id = %s""", (str(id)))
#     # dcr_entry = cursor.fetchone()
#     dcr_entry = db.query(models.DCR).filter(models.DCR.id == id).first()

#     print(dcr_entry)
#     if not dcr_entry:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"dcr with the id {id} is not found")
#     return dcr_entry

# @app.delete('/dcr/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_item(id: int, db: Session = Depends(get_db)):
#     # cursor.execute("""DELETE FROM dcr_entries WHERE id = %s RETURNING * """, (str(id)))
#     # deleted_dcr_entry = cursor.fetchone()
#     # conn.commit()
#     dcr = db.query(models.DCR).filter(models.DCR.id == id)
#     if dcr.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"dcr with the id {id} is not found")
    
#     dcr.delete(synchronize_session=False)
#     db.commit()

# @app.put('/dcr/{id}', response_model=DCRResponse)
# def update_item(id: int, updated_dcr: DCR, db: Session = Depends(get_db)):
#     # cursor.execute("""UPDATE dcr_entries SET language = %s , source = %s, ticket_number = %s, calls = %s, emails = %s, chats = %s WHERE id = %s RETURNING *""",
#     # (dcr.language, dcr.source, dcr.ticket_number, dcr.calls, dcr.emails, dcr.chats, str(id)))
#     # updated_dcr_entry = cursor.fetchone()
#     # conn.commit()
#     dcr_query = db.query(models.DCR).filter(models.DCR.id == id)
#     dcr = dcr_query.first()

#     if dcr == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"dcr with the id {id} is not found")

#     dcr_query.update(updated_dcr.dict(), synchronize_session=False)

#     db.commit()

#     return dcr_query.first()


# @app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     # hash the password - user.password

#     hashed_password = utils.hash(user.password)
#     user.password = hashed_password

#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user


# @app.get("/users/{id}", response_model=schemas.UserOut)
# def get_user(id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
    

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} does not exist")
    
#     return user