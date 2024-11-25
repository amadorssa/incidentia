// Selección de elementos
const sidebar = document.getElementById('sidebar');
const toggleMenu = document.getElementById('toggleMenu');

// Alternar la clase 'collapsed' al hacer clic en el botón
toggleMenu.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed'); // Añade o quita la clase 'collapsed'
});
