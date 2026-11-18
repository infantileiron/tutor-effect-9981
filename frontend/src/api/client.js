export async function request(path,options={}){
 const token=sessionStorage.getItem('tutor-token');
 const response=await fetch('/api'+path,{...options,headers:{'Content-Type':'application/json',...(token?{Authorization:`Bearer ${token}`} :{}),...options.headers}});
 const data=await response.json().catch(()=>({}));
 if(!response.ok){let detail=data.detail;if(Array.isArray(detail))detail=detail.map(x=>x.msg).join('；');throw new Error(detail||'请求失败，请重试');}
 return data;
}
export const post=(path,data)=>request(path,{method:'POST',body:JSON.stringify(data)});
