from fastapi import APIRouter, Body, FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
import schemas, database, models, oauth2


router = APIRouter(
  prefix="/vote",
  tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
  
  dcr = db.query(models.DCR).filter(models.DCR.id == vote.dcr_id).first()

  if not dcr:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"dcr with the id {vote.dcr_id} does not exist")
  
  vote_query = db.query(models.Vote).filter(models.Vote.dcr_id == vote.dcr_id, models.Vote.user_id == current_user.id)
  found_vote = vote_query.first()

  if (vote.dir == 1):
    if found_vote:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on dcr {vote.dcr_id}")
    new_vote = models.Vote(dcr_id = vote.dcr_id, user_id=current_user.id)
    db.add(new_vote)
    db.commit()
    return {"message": "sccessfully added vote"}
  else:
    if not found_vote:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote does not exist")

    vote_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "sccessfully deleted vote"}