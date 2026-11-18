import os,hashlib,hmac,secrets
from datetime import datetime,timedelta,timezone
import jwt
from fastapi import Depends,HTTPException,Request
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from src.config.database import get_db
from src.models.entities import User
from sqlalchemy.orm import Session
bearer=HTTPBearer(auto_error=False)
def hash_password(password):
    salt=secrets.token_hex(16)
    return salt+':'+hashlib.pbkdf2_hmac('sha256',password.encode(),salt.encode(),180000).hex()
def verify_password(password,stored):
    salt,digest=stored.split(':')
    return hmac.compare_digest(digest,hashlib.pbkdf2_hmac('sha256',password.encode(),salt.encode(),180000).hex())
def token_for(user):
    return jwt.encode({'sub':str(user.id),'exp':datetime.now(timezone.utc)+timedelta(hours=8)},os.environ['JWT_SECRET'],algorithm='HS256')
def current_user(request:Request,auth:HTTPAuthorizationCredentials|None=Depends(bearer),db:Session=Depends(get_db)):
    try:
        payload=jwt.decode(auth.credentials,os.environ['JWT_SECRET'],algorithms=['HS256'])
        user=db.get(User,int(payload['sub']))
        if not user: raise ValueError()
    except Exception: raise HTTPException(401,'登录已失效，请重新登录')
    request.state.actor=user.email
    return user
def editor(user:User=Depends(current_user)):
    if user.role not in ('admin','analyst'): raise HTTPException(403,'只读账号不能修改或提交计算')
    return user
def admin(user:User=Depends(current_user)):
    if user.role!='admin': raise HTTPException(403,'仅管理员可访问审计或签核发布')
    return user
