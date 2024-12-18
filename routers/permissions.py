from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..models import Permission
from ..auth import require_admin

router = APIRouter()

# Pydantic models for request validation
class PermissionCreate(BaseModel):
    name: str
    api_endpoint: str
    description: str

# Add a permission (Admin only)
@router.post("/permissions", dependencies=[Depends(require_admin)])
def add_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    existing_permission = db.query(Permission).filter(Permission.name == permission.name).first()
    if existing_permission:
        raise HTTPException(status_code=400, detail="Permission with this name already exists")

    new_permission = Permission(
        name=permission.name,
        api_endpoint=permission.api_endpoint,
        description=permission.description
    )
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return {"message": "Permission added successfully", "permission": new_permission}

# Modify a permission (Admin only)
@router.put("/permissions/{permission_id}", dependencies=[Depends(require_admin)])
def modify_permission(permission_id: int, permission: PermissionCreate, db: Session = Depends(get_db)):
    existing_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not existing_permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    existing_permission.name = permission.name
    existing_permission.api_endpoint = permission.api_endpoint
    existing_permission.description = permission.description
    db.commit()
    return {"message": "Permission updated successfully", "permission": existing_permission}

# Delete a permission (Admin only)
@router.delete("/permissions/{permission_id}", dependencies=[Depends(require_admin)])
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    existing_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not existing_permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    db.delete(existing_permission)
    db.commit()
    return {"message": "Permission deleted successfully"}

# Get all permissions (Admin only)
@router.get("/permissions", dependencies=[Depends(require_admin)])
def get_all_permissions(db: Session = Depends(get_db)):
    permissions = db.query(Permission).all()
    return {"permissions": permissions}
