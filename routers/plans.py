from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..models import SubscriptionPlan
from ..auth import require_admin

router = APIRouter()

# Pydantic models for request validation
class PlanCreate(BaseModel):
    name: str
    description: str
    permissions: str
    limits: int

# Create a subscription plan (Admin only)
@router.post("/plans", dependencies=[Depends(require_admin)])
def create_plan(plan: PlanCreate, db: Session = Depends(get_db)):
    existing_plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.name == plan.name).first()
    if existing_plan:
        raise HTTPException(status_code=400, detail="Plan with this name already exists")

    new_plan = SubscriptionPlan(
        name=plan.name,
        description=plan.description,
        permissions=plan.permissions,
        limits=plan.limits
    )
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return {"message": "Plan created successfully", "plan": new_plan}

# Modify a subscription plan (Admin only)
@router.put("/plans/{plan_id}", dependencies=[Depends(require_admin)])
def modify_plan(plan_id: int, plan: PlanCreate, db: Session = Depends(get_db)):
    existing_plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == plan_id).first()
    if not existing_plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    existing_plan.name = plan.name
    existing_plan.description = plan.description
    existing_plan.permissions = plan.permissions
    existing_plan.limits = plan.limits
    db.commit()
    return {"message": "Plan updated successfully", "plan": existing_plan}

# Delete a subscription plan (Admin only)
@router.delete("/plans/{plan_id}", dependencies=[Depends(require_admin)])
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    existing_plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == plan_id).first()
    if not existing_plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    db.delete(existing_plan)
    db.commit()
    return {"message": "Plan deleted successfully"}

# Get all subscription plans (Admin only)
@router.get("/plans", dependencies=[Depends(require_admin)])
def get_all_plans(db: Session = Depends(get_db)):
    plans = db.query(SubscriptionPlan).all()
    return {"plans": plans}
