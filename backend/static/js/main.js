window.onload = function() {
    fetch('/api/estudiantes')
      .then(response => response.json())
      .then(data => {
        const contenido = document.getElementById('contenido');
        contenido.innerHTML = data.map(est => `
          <p>${est.id} - ${est.nombre} (${est.correo})</p>
        `).join('');
      });
};