const lista = document.getElementById('lista');
const tareas = JSON.parse(localStorage.getItem('tareas') || '[]');
tareas.forEach((t) => { const li = document.createElement('li'); li.textContent = t; lista.append(li); });
document.getElementById('exportar').addEventListener('click', () => {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(tareas)], { type: 'application/json' }));
  a.download = 'tareas.json';
  a.click();
});
if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js');
