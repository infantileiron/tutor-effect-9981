export function formData(form){return Object.fromEntries(new FormData(form));}export function busy(form,value){for(const button of form.querySelectorAll('button'))button.disabled=value;}
