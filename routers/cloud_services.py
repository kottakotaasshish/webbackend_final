from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import get_current_user
from ..models import SubscriptionPlan, User, Usage

router = APIRouter()

# Helper function to enforce access control and usage tracking
def enforce_access_control(user: User, api_name: str, db: Session):
    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == user.subscription_plan_id).first()
    if not plan or api_name not in plan.permissions.split(","):
        raise HTTPException(status_code=403, detail=f"Access denied to {api_name}")

    # Track and update usage
    usage = db.query(Usage).filter(Usage.user_id == user.id, Usage.api_name == api_name).first()
    if usage:
        usage.request_count += 1
    else:
        usage = Usage(user_id=user.id, api_name=api_name, request_count=1)
        db.add(usage)

    db.commit()

    # Enforce usage limits
    if plan.limits != -1 and usage.request_count > plan.limits:
        raise HTTPException(status_code=403, detail=f"API usage limit exceeded for {api_name}")

    return usage

# Service 1
@router.get("/service1")
def service1(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    usage = enforce_access_control(user, "api1", db)
    return {
        "message": f"Hello {user.username}, welcome to Service 1!",
        "usage_count": usage.request_count,
        "limit": db.query(SubscriptionPlan).filter(SubscriptionPlan.id == user.subscription_plan_id).first().limits,
    }

# Service 2
@router.get("/service2")
def service2(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    usage = enforce_access_control(user, "api2", db)
    return {
        "message": f"Hello {user.username}, welcome to Service 2!",
        "usage_count": usage.request_count,
        "limit": db.query(SubscriptionPlan).filter(SubscriptionPlan.id == user.subscription_plan_id).first().limits,
    }

# Service 3
@router.get("/service3")
def service3(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    usage = enforce_access_control(user, "api3", db)
    return {
        "message": f"Hello {user.username}, welcome to Service 3!",
        "usage_count": usage.request_count,
        "limit": db.query(SubscriptionPlan).filter(SubscriptionPlan.id == user.subscription_plan_id).first().limits,
    }

# Service 4
@router.get("/service4")
def service4(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    usage = enforce_access_control(user, "api4", db)
    return {
        "message": f"Hello {user.username}, welcome to Service 4!",
        "usage_count": usage.request_count,
        "limit": db.query(SubscriptionPlan).filter(SubscriptionPlan.id == user.subscription_plan_id).first().limits,
    }

# Service 5
@router.get("/service5")
def service5(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    usage = enforce_access_control(user, "api5", db)
    return {
        "message": f"Hello {user.username}, welcome to Service 5!",
        "usage_count": usage.request_count,
        "limit": db.query(SubscriptionPlan).filter(SubscriptionPlan.id == user.subscription_plan_id).first().limits,
    }

# Service 6
@router.get("/service6")
def service6(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    usage = enforce_access_control(user, "api6", db)
    return {
        "message": f"Hello {user.username}, welcome to Service 6!",
        "usage_count": usage.request_count,
        "limit": db.query(SubscriptionPlan).filter(SubscriptionPlan.id == user.subscription_plan_id).first().limits,
    }
