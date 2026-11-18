import csv,io,json
from fastapi import APIRouter,Depends,HTTPException
from fastapi.responses import Response
from src.config.database import get_db
from src.utils.security import current_user,editor,admin
from src.schemas.business import RunInput,ConclusionInput
from src.services import reports
from src.controllers.business import serialize,serialize_many
from src.models.entities import Audit
from sqlalchemy import select
router=APIRouter()
@router.get('/reports')
def listing(db=Depends(get_db),user=Depends(current_user)): return serialize_many(reports.list_reports(db))
@router.post('/reports',status_code=202)
def create(data:RunInput,db=Depends(get_db),user=Depends(editor)): return serialize(reports.create_report(db,data.plan_id))
@router.get('/reports/{id}')
def detail(id:int,db=Depends(get_db),user=Depends(current_user)): return serialize(reports.get_report(db,id))
@router.patch('/reports/{id}/conclusion')
def conclusion(id:int,data:ConclusionInput,db=Depends(get_db),user=Depends(editor)): return serialize(reports.save_conclusion(db,id,data,user))
@router.get('/reports/{id}/export')
def export(id:int,db=Depends(get_db),user=Depends(current_user)):
    item=reports.get_report(db,id)
    if item.status!='completed': raise HTTPException(409,'报告尚未完成')
    result=dict(item.result);result.pop('sample_snapshot',None)
    content={'report_id':item.id,'plan_id':item.plan_id,'created_at':item.created_at,'published':item.published,'conclusion':item.conclusion,'statistics':result,'sample_snapshot':item.result['sample_snapshot']}
    return Response(json.dumps(content,ensure_ascii=False,indent=2),media_type='application/json',headers={'Content-Disposition':f'attachment; filename="tutor-effect-report-{id}.json"'})
@router.get('/audit')
def audit(db=Depends(get_db),user=Depends(admin)): return serialize_many(db.scalars(select(Audit).order_by(Audit.id.desc()).limit(100)).all())
