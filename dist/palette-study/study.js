const picker=document.getElementById('palette-picker');
const grid=document.querySelector('.study-grid');
picker.addEventListener('change',()=>{
  const value=picker.value;
  document.querySelectorAll('.palette-option').forEach(option=>{option.hidden=value!=='all'&&option.dataset.palette!==value;});
  grid.classList.toggle('is-single',value!=='all');
});
