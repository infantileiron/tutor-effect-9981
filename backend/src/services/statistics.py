import math,hashlib,json
from scipy import stats

def welch(students,plan):
    selected=[s for s in students if plan.campus=='全部' or s.campus==plan.campus]
    kept=[s for s in selected if s.score is not None and (not plan.exclude_absent or not s.absent)]
    control=[s.score for s in kept if s.group=='control']
    treatment=[s.score for s in kept if s.group=='intervention']
    n0,n1=len(control),len(treatment)
    if min(n0,n1)<2: raise ValueError('每组至少需要 2 个有效成绩；请调整教学点或补录样本')
    m0,m1=sum(control)/n0,sum(treatment)/n1
    v0=sum((x-m0)**2 for x in control)/(n0-1)
    v1=sum((x-m1)**2 for x in treatment)/(n1-1)
    se2=v0/n0+v1/n1
    if se2<=0: raise ValueError('两组方差均为零，无法进行 Welch 检验')
    df=se2**2/((v0/n0)**2/(n0-1)+(v1/n1)**2/(n1-1))
    se=math.sqrt(se2);delta=m1-m0;t=delta/se
    p=float(2*stats.t.sf(abs(t),df))
    margin=float(stats.t.ppf(.975,df))*se
    pooled=math.sqrt(((n0-1)*v0+(n1-1)*v1)/(n0+n1-2))
    digest=hashlib.sha256(json.dumps([(s.code,s.score,s.group,s.absent) for s in kept],ensure_ascii=False).encode()).hexdigest()
    return {'control_n':n0,'intervention_n':n1,'excluded':len(selected)-len(kept),'total_selected':len(selected),'control_mean':m0,'intervention_mean':m1,'difference':delta,'t':t,'df':df,'p_value':p,'ci_low':delta-margin,'ci_high':delta+margin,'cohen_d':delta/pooled if pooled else None,'significant':p<.05,'checksum':digest,'sample_snapshot':[{'code':s.code,'group':s.group,'score':s.score,'campus':s.campus} for s in kept],'method':'Welch 独立样本 t 检验；双侧 α=0.05；干预组减对照组；95% CI'}
