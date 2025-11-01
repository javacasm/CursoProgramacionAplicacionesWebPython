// Opcional: Agregar interactividad adicional si es necesario
document.addEventListener('DOMContentLoaded', () => {
    // Ejemplo: Asegurar que las tarjetas tengan un efecto suave
    const cards = document.querySelectorAll('.receta-card');
    cards.forEach(card => {
        card.addEventListener('click', () => {
            const link = card.querySelector('a');
            if (link) {
                window.location.href = link.href;
            }
        });
    });
});