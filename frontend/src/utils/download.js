export async function downloadReport(id,token){
 const response=await fetch(`/api/reports/${id}/export`,{headers:{Authorization:`Bearer ${token}`}});
 if(!response.ok) throw new Error('导出失败，请确认报告已完成');
 const url=URL.createObjectURL(await response.blob());const a=document.createElement('a');a.href=url;a.download=`tutor-effect-report-${id}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
