from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Usage, User
from ..auth import require_admin


router = APIRouter()

# Track API usage
@router.post("/usage/{username}/{api_name}")
def track_usage(username: str, api_name: str, db: Session = Depends(get_db)):
    # Find the user
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if a usage entry exists
    usage = db.query(Usage).filter(Usage.user_id == user.id, Usage.api_name == api_name).first()
    if usage:
        usage.request_count += 1
    else:
        usage = Usage(user_id=user.id, api_name=api_name, request_count=1)
        db.add(usage)

    db.commit()
    return {"message": "Usage tracked successfully", "usage": {"api_name": api_name, "request_count": usage.request_count}}

# View usage limits
@router.get("/usage/{username}")
def get_usage(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    usage = db.query(Usage).filter(Usage.user_id == user.id).all()
    return {"usage": [{"api_name": u.api_name, "request_count": u.request_count} for u in usage]}


@router.put("/usage/reset/{username}/{api_name}", dependencies=[Depends(require_admin)])
def reset_usage(username: str, api_name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    usage = db.query(Usage).filter(Usage.user_id == user.id, Usage.api_name == api_name).first()
    if usage:
        usage.request_count = 0
        db.commit()
        return {"message": f"Usage reset successfully for {api_name}"}

    raise HTTPException(status_code=404, detail="Usage record not found")

@router.get("/usage/all", dependencies=[Depends(require_admin)])
def get_all_usage(db: Session = Depends(get_db)):
    usage_records = db.query(Usage).all()
    return {"usage": [{"user_id": u.user_id, "api_name": u.api_name, "request_count": u.request_count} for u in usage_records]}

@router.put("/usage/reset/{username}", dependencies=[Depends(require_admin)])
def reset_user_usage(username: str, db: Session = Depends(get_db)):
    # Find the user
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Reset usage for the user
    db.query(Usage).filter(Usage.user_id == user.id).delete()
    db.commit()
    return {"message": f"Usage data reset successfully for user '{username}'"}


@router.get("/usage/overview", dependencies=[Depends(require_admin)])
def get_usage_overview(db: Session = Depends(get_db)):
    usage_records = db.query(Usage).all()
    usage_summary = [
        {"username": db.query(User).filter(User.id == u.user_id).first().username, 
         "api_name": u.api_name, 
         "request_count": u.request_count}
        for u in usage_records
    ]
    return {"usage_overview": usage_summary}
