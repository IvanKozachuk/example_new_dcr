# from .. import schemas, models
from fastapi import APIRouter, Body, FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, outerjoin
from typing import List
# from ..database import get_db
from database import get_db
import schemas, oauth2
import models
from typing import Optional

router = APIRouter(
  prefix="/dcr",
  tags=['DCR']
)

# @router.get('/', response_model=List[schemas.DCRResponse])
@router.get('/', response_model=List[schemas.DCROut])
def get_all_items(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM dcr_entries """)
    # dcr_entries = cursor.fetchall()

    # dcr_entries = db.query(models.DCR).filter(models.DCR.ticket_number.contains(search)).limit(limit).offset(skip).all()
    # if we want to see only dcrs created by this user
    # dcr_entries = db.query(models.DCR).filter(models.DCR.owner_id == current_user.id).all()

    dcr_entries = db.query(models.DCR, func.count(models.Vote.dcr_id).label("votes")).join(models.Vote, models.Vote.dcr_id == models.DCR.id, isouter=True).group_by(models.DCR.id).filter(models.DCR.ticket_number.contains(search)).limit(limit).offset(skip).all()

    return dcr_entries

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.DCRResponse)
def create_dcr(dcr: schemas.DCR, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO dcr_entries (language, source, ticket_number, calls, emails, chats)
    # VALUES (%s, %s, %s, %s, %s, %s) RETURNING *""", (dcr.language, dcr.source, dcr.ticket_number, dcr.calls, dcr.emails, dcr.chats))
    # new_dcr = cursor.fetchone()
    # conn.commit()
    new_dcr = models.DCR(owner_id=current_user.id, **dcr.dict())
    db.add(new_dcr)
    db.commit()
    db.refresh(new_dcr)
    return new_dcr


@router.get('/{id}', response_model=schemas.DCROut)
def get_one_item(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM dcr_entries WHERE id = %s""", (str(id)))
    # dcr_entry = cursor.fetchone()
    # dcr_entry = db.query(models.DCR).filter(models.DCR.id == id).first()

    dcr_entry = db.query(models.DCR, func.count(models.Vote.dcr_id).label("votes")).join(models.Vote, models.Vote.dcr_id == models.DCR.id, isouter=True).group_by(models.DCR.id).filter(models.DCR.id == id).first()
    
    if not dcr_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"dcr with the id {id} is not found")
    
    # if we want to see only a dcr created by ourself
    # if dcr_entry.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #     detail="Not authorized to perform requested action")
    
    return dcr_entry

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM dcr_entries WHERE id = %s RETURNING * """, (str(id)))
    # deleted_dcr_entry = cursor.fetchone()
    # conn.commit()
    dcr_query = db.query(models.DCR).filter(models.DCR.id == id)

    dcr = dcr_query.first()

    if dcr_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"dcr with the id {id} is not found")
    
    if dcr.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to perform requested action")

    dcr_query.delete(synchronize_session=False)
    db.commit()

@router.put('/{id}', response_model=schemas.DCRResponse)
def update_item(id: int, updated_dcr: schemas.DCR, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE dcr_entries SET language = %s , source = %s, ticket_number = %s, calls = %s, emails = %s, chats = %s WHERE id = %s RETURNING *""",
    # (dcr.language, dcr.source, dcr.ticket_number, dcr.calls, dcr.emails, dcr.chats, str(id)))
    # updated_dcr_entry = cursor.fetchone()
    # conn.commit()
    dcr_query = db.query(models.DCR).filter(models.DCR.id == id)
    dcr = dcr_query.first()

    if dcr == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"dcr with the id {id} is not found")

    if dcr.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to perform requested action")
    
    dcr_query.update(updated_dcr.dict(), synchronize_session=False)

    db.commit()

    return dcr_query.first()