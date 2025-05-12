document.addEventListener("DOMContentLoaded", () => {
  fetch("/api/estudiantes")
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector("#tabla-estudiantes tbody");

      if (data.length === 0) {
        tbody.innerHTML = "<tr><td colspan='4'>No hay estudiantes registrados.</td></tr>";
        return;
      }

      data.forEach(est => {
        const fila = `
          <tr>
            <td>${est.id}</td>
            <td>${est.nombre}</td>
            <td>${est.correo}</td>
            <td>${est.fecha_nacimiento}</td>
          </tr>
        `;
        tbody.innerHTML += fila;
      });
    })
    .catch(err => {
      console.error("Error al obtener estudiantes:", err);
    });
});