from sqlalchemy import select
from fastapi import HTTPException
from src.models.entities import Plan
def list_plans(db): return db.scalars(select(Plan).order_by(Plan.id.desc())).all()
def save_plan(db,data,id=None):
    item=db.get(Plan,id) if id else Plan()
    if not item: raise HTTPException(404,'方案不存在')
    for k,v in data.model_dump().items(): setattr(item,k,v)
    db.add(item);db.commit();db.refresh(item)
    return item
