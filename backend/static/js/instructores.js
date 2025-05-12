document.addEventListener("DOMContentLoaded", () => {
  fetch("/api/instructores")
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector("#tabla-instructores tbody");

      if (data.length === 0) {
        tbody.innerHTML = "<tr><td colspan='4'>No hay instructores registrados.</td></tr>";
        return;
      }

      data.forEach(inst => {
        const fila = `
          <tr>
            <td>${inst.id}</td>
            <td>${inst.nombre}</td>
            <td>${inst.correo}</td>
            <td>${inst.especialidad}</td>
          </tr>
        `;
        tbody.innerHTML += fila;
      });
    })
    .catch(err => {
      console.error("Error al obtener instructores:", err);
    });
});