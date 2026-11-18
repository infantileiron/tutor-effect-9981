from fastapi import APIRouter,Depends
from src.config.database import get_db
from src.utils.security import current_user,editor
from src.schemas.business import StudentInput
from src.services import students
from src.controllers.business import serialize,serialize_many
router=APIRouter()
@router.get('/students')
def listing(db=Depends(get_db),user=Depends(current_user)): return serialize_many(students.list_students(db))
@router.post('/students',status_code=201)
def create(data:StudentInput,db=Depends(get_db),user=Depends(editor)): return serialize(students.save_student(db,data))
@router.put('/students/{id}')
def update(id:int,data:StudentInput,db=Depends(get_db),user=Depends(editor)): return serialize(students.save_student(db,data,id))
