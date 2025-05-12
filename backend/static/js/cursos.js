document.addEventListener("DOMContentLoaded", () => {
  fetch("/api/cursos")
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector("#tabla-cursos tbody");

      if (data.length === 0) {
        tbody.innerHTML = "<tr><td colspan='5'>No hay cursos registrados.</td></tr>";
        return;
      }

      data.forEach(curso => {
        const fila = `
          <tr>
            <td>${curso.id}</td>
            <td>${curso.nombre}</td>
            <td>${curso.descripcion}</td>
            <td>${curso.duracion_horas}</td>
            <td>${curso.id_instructor}</td>
          </tr>
        `;
        tbody.innerHTML += fila;
      });
    })
    .catch(err => {
      console.error("Error al obtener cursos:", err);
    });
});