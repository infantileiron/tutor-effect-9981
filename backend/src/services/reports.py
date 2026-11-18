import os
from datetime import datetime,timezone
from sqlalchemy import select
from fastapi import HTTPException
import redis
from src.models.entities import Report,Plan
queue=redis.Redis.from_url(os.environ['REDIS_URL'])
def list_reports(db): return db.scalars(select(Report).order_by(Report.id.desc())).all()
def create_report(db,plan_id):
    if not db.get(Plan,plan_id): raise HTTPException(404,'辅导方案不存在')
    running=db.scalars(select(Report).where(Report.status.in_(['queued','running']))).all()
    if len(running)>=10: raise HTTPException(429,'待执行任务已达10个，请稍后再试')
    item=Report(plan_id=plan_id,status='queued',created_at=datetime.now(timezone.utc).isoformat())
    db.add(item);db.commit();db.refresh(item)
    queue.lpush('tutor:reports',item.id)
    return item
def get_report(db,id):
    item=db.get(Report,id)
    if not item: raise HTTPException(404,'报告不存在')
    return item
def save_conclusion(db,id,data,user):
    item=get_report(db,id)
    if item.status!='completed': raise HTTPException(409,'计算完成后才能起草结论')
    if item.published and user.role!='admin': raise HTTPException(403,'已签核报告仅管理员可更改')
    if data.published and user.role!='admin': raise HTTPException(403,'仅管理员可签核发布')
    item.conclusion=data.conclusion;item.published=data.published
    db.commit();db.refresh(item)
    return item
