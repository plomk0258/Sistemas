document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const gameFile = document.getElementById('gameFile').files[0];
    const gameName = document.getElementById('gameName').value;
    const category = document.getElementById('category').value;
    const description = document.getElementById('description').value;

    if (!gameFile || !gameName) {
        alert('Por favor, completa todos los campos obligatorios.');
        return;
    }

    const formData = new FormData();
    formData.append('gameFile', gameFile);
    formData.append('gameName', gameName);
    formData.append('category', category);
    formData.append('description', description);

    try {
        const response = await fetch('/games', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Error al subir el archivo.');
        }

        const data = await response.json();
        alert(data.mensaje);
        cargarJuegos(); // Recargar la lista de juegos
    } catch (error) {
        alert('Error al subir el archivo: ' + error.message);
    }
});

async function cargarJuegos() {
    try {
        const response = await fetch('/games');
        const juegos = await response.json();

        const gamesList = document.getElementById('games-list');
        gamesList.innerHTML = ''; // Limpiar la lista

        juegos.forEach(juego => {
            const gameCard = document.createElement('div');
            gameCard.className = 'game-card';

            gameCard.innerHTML = `
                <img src="${juego.icono}" alt="${juego.nombre}" class="game-img">
                <h3>${juego.nombre}</h3>
                <p><strong>Categoría:</strong> ${juego.categoria}</p>
                <p>${juego.descripcion}</p>
                <button class="btn-play" data-file="${juego.archivo_html}">▶️ Jugar</button>
                <button class="btn-delete" data-id="${juego.id}">❌ Eliminar</button>
            `;

            gamesList.appendChild(gameCard);

            // Funcionalidad del botón "Jugar"
            gameCard.querySelector('.btn-play').addEventListener('click', () => {
                window.open(juego.archivo_html, '_blank');
            });

            // Funcionalidad del botón "Eliminar"
            gameCard.querySelector('.btn-delete').addEventListener('click', async () => {
                const confirmDelete = confirm(`¿Estás seguro de que deseas eliminar el juego "${juego.nombre}"?`);
                if (confirmDelete) {
                    try {
                        const deleteResponse = await fetch(`/games/${juego.id}`, { method: 'DELETE' });
                        if (!deleteResponse.ok) throw new Error('Error al eliminar el juego');
                        alert('Juego eliminado correctamente');
                        cargarJuegos(); // Recargar la lista de juegos
                    } catch (error) {
                        alert('Error al eliminar el juego: ' + error.message);
                    }
                }
            });
        });
    } catch (error) {
        console.error('Error al cargar los juegos:', error);
    }
}