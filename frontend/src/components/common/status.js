import{STATUS}from'../../constants/enums.js';export const badge=(status)=>`<span class="badge ${status}">${STATUS[status]||status}</span>`;
