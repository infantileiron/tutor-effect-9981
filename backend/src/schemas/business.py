from typing import Literal
from pydantic import BaseModel,Field,model_validator
class LoginInput(BaseModel):
    email:str=Field(max_length=120)
    password:str=Field(max_length=200)
class StudentInput(BaseModel):
    code:str=Field(min_length=1,max_length=50)
    name:str=Field(min_length=1,max_length=80)
    campus:str=Field(min_length=1,max_length=50)
    group:Literal['control','intervention']
    score:float|None=Field(default=None,ge=0,le=100,allow_inf_nan=False)
    absent:bool=False
    @model_validator(mode='after')
    def score_required(self):
        if not self.absent and self.score is None: raise ValueError('非缺考学员必须填写成绩')
        return self
class PlanInput(BaseModel):
    title:str=Field(min_length=2,max_length=120)
    campus:str=Field(default='全部',max_length=50)
    exclude_absent:bool=True
    description:str=Field(default='',max_length=2000)
class RunInput(BaseModel):
    plan_id:int=Field(gt=0)
class ConclusionInput(BaseModel):
    conclusion:str=Field(min_length=4,max_length=3000)
    published:bool=False
