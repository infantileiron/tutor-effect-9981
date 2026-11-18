from sqlalchemy import select
from src.models.entities import Student
from fastapi import HTTPException
def list_students(db): return db.scalars(select(Student).order_by(Student.id)).all()
def save_student(db,data,id=None):
    item=db.get(Student,id) if id else Student()
    if not item: raise HTTPException(404,'学员不存在')
    for k,v in data.model_dump().items(): setattr(item,k,v)
    db.add(item);db.commit();db.refresh(item)
    return item
