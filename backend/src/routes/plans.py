from fastapi import APIRouter,Depends
from src.config.database import get_db
from src.utils.security import current_user,editor
from src.schemas.business import PlanInput
from src.services import plans
from src.controllers.business import serialize,serialize_many
router=APIRouter()
@router.get('/plans')
def listing(db=Depends(get_db),user=Depends(current_user)): return serialize_many(plans.list_plans(db))
@router.post('/plans',status_code=201)
def create(data:PlanInput,db=Depends(get_db),user=Depends(editor)): return serialize(plans.save_plan(db,data))
@router.put('/plans/{id}')
def update(id:int,data:PlanInput,db=Depends(get_db),user=Depends(editor)): return serialize(plans.save_plan(db,data,id))
