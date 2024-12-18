from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, SubscriptionPlan
from datetime import datetime
from ..models import Usage


router = APIRouter()

# Check API access for a user
@router.get("/access/{username}/{api_name}")
def check_access(username: str, api_name: str, db: Session = Depends(get_db)):
    # Find the user
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Ensure the user is subscribed to a plan
    if not user.subscription_plan_id:
        raise HTTPException(status_code=403, detail="User is not subscribed to any plan")

    # Get the user's subscription plan
    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == user.subscription_plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Subscription plan not found")

    # Check if the API is in the permissions list
    if api_name not in plan.permissions.split(","):
        raise HTTPException(status_code=403, detail="Access to this API is not allowed for the user's plan")

    # Query the Usage table for the user's current API usage
    usage = db.query(Usage).filter(Usage.user_id == user.id, Usage.api_name == api_name).first()

    # Check if the user has exceeded their usage limits
    if plan.limits != -1:  # -1 means unlimited usage
        if usage and usage.request_count >= plan.limits:
            raise HTTPException(status_code=403, detail="API usage limit exceeded")

    # If the user hasn't exceeded their limits, track the usage
    if usage:
        usage.request_count += 1
    else:
        usage = Usage(user_id=user.id, api_name=api_name, request_count=1)
        db.add(usage)

    db.commit()

    # Allow access
    return {
        "message": "Access granted",
        "api_name": api_name,
        "username": username,
        "current_usage": usage.request_count if usage else 0,
        "limit": plan.limits
    }
