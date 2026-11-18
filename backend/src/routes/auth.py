from fastapi import APIRouter,Depends,HTTPException,Request
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.models.entities import User
from src.schemas.business import LoginInput
from src.utils.security import verify_password,token_for,current_user
router=APIRouter()
@router.post('/auth/login')
def login(data:LoginInput,request:Request,db:Session=Depends(get_db)):
    user=db.scalar(select(User).where(User.email==data.email))
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(401,'邮箱或密码不正确')
    request.state.actor=user.email
    return {'access_token':token_for(user),'user':{'email':user.email,'role':user.role}}
@router.get('/auth/me')
def me(user=Depends(current_user)): return {'email':user.email,'role':user.role}
