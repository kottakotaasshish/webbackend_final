from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..models import User, SubscriptionPlan
from ..auth import get_current_user, require_admin

router = APIRouter()

# Pydantic models for request validation
class SubscriptionCreate(BaseModel):
    username: str
    subscription_plan_id: int

class SubscriptionUpdate(BaseModel):
    subscription_plan_id: int

# Subscribe to a plan (Authenticated User)
@router.post("/subscriptions", dependencies=[Depends(get_current_user)])
def subscribe_to_plan(subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == subscription.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == subscription.subscription_plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Subscription plan not found")

    user.subscription_plan_id = subscription.subscription_plan_id
    db.commit()
    return {"message": "Subscription updated successfully", "user": user}

# View subscription details (Authenticated User)
@router.get("/subscriptions/{username}", dependencies=[Depends(get_current_user)])
def get_subscription_details(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.subscription_plan_id:
        raise HTTPException(status_code=400, detail="User is not subscribed to any plan")

    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == user.subscription_plan_id).first()
    return {"username": user.username, "subscription_plan": plan}

# Assign/Modify user plan (Admin only)
@router.put("/subscriptions/{user_id}", dependencies=[Depends(require_admin)])
def assign_modify_user_plan(user_id: int, subscription: SubscriptionUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == subscription.subscription_plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Subscription plan not found")

    user.subscription_plan_id = subscription.subscription_plan_id
    db.commit()
    return {"message": "Subscription plan assigned/modified successfully", "user": user}
