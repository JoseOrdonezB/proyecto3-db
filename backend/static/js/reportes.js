document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("reporte-select");
  const filtrosForm = document.getElementById("filtros-form");
  const btnGenerar = document.getElementById("generar-reporte");
  const resultado = document.getElementById("resultado-reporte");

  select.addEventListener("change", () => {
    const tipo = select.value;
    filtrosForm.innerHTML = generarFiltros(tipo);
    resultado.innerHTML = "";
  });

  btnGenerar.addEventListener("click", () => {
    const tipo = select.value;
    if (!tipo) return alert("Selecciona un reporte primero.");

    const filtros = new FormData(filtrosForm);
    const params = new URLSearchParams();
    filtros.forEach((value, key) => {
      if (value) params.append(key, value);
    });

    fetch(`/api/reportes/${tipo}?${params.toString()}`)
      .then((res) => res.json())
      .then((data) => mostrarTabla(tipo, data))
      .catch((err) => console.error("Error generando reporte:", err));
  });
});

function generarFiltros(tipo) {
  switch (tipo) {
    case "avance":
      return `
        <input name="curso_id" placeholder="ID del curso">
        <input name="porcentaje_min" placeholder="% mínimo" type="number">
        <input name="porcentaje_max" placeholder="% máximo" type="number">
        <input name="fecha_inicio" placeholder="Fecha inicio" type="date">
        <input name="fecha_fin" placeholder="Fecha fin" type="date">
      `;
    case "ranking":
      return `
        <input name="curso_id" placeholder="ID del curso">
        <input name="calificacion_min" placeholder="Calificación mínima" type="number">
        <input name="fecha_inicio" placeholder="Fecha inicio" type="date">
        <input name="fecha_fin" placeholder="Fecha fin" type="date">
        <input name="top_n" placeholder="Top N" type="number">
      `;
    case "entregas":
      return `
        <input name="curso_id" placeholder="ID del curso">
        <input name="puntaje_min" placeholder="Puntaje mínimo" type="number">
        <input name="puntaje_max" placeholder="Puntaje máximo" type="number">
        <input name="fecha_inicio" placeholder="Fecha entrega inicio" type="date">
        <input name="fecha_fin" placeholder="Fecha entrega fin" type="date">
      `;
    case "inscripciones":
      return `
        <input name="curso_id" placeholder="ID del curso">
        <input name="instructor_id" placeholder="ID del instructor">
        <input name="fecha_inicio" placeholder="Fecha inicio" type="date">
        <input name="fecha_fin" placeholder="Fecha fin" type="date">
      `;
    case "cursos":
      return `
        <input name="id_categoria" placeholder="ID categoría">
        <input name="duracion_min" placeholder="Duración mínima" type="number">
        <input name="duracion_max" placeholder="Duración máxima" type="number">
        <input name="instructor_id" placeholder="ID instructor">
        <input name="nombre_like" placeholder="Nombre contiene...">
      `;
    default:
      return "";
  }
}

function mostrarTabla(tipo, datos) {
  const resultado = document.getElementById("resultado-reporte");

  if (!Array.isArray(datos) || datos.length === 0) {
    resultado.innerHTML = "<p>No hay resultados para mostrar.</p>";
    return;
  }

  const keys = Object.keys(datos[0]);
  let html = "<table class='tabla-estudiantes'><thead><tr>";
  keys.forEach((k) => (html += `<th>${k}</th>`));
  html += "</tr></thead><tbody>";

  datos.forEach((item) => {
    html += "<tr>";
    keys.forEach((k) => (html += `<td>${item[k] ?? ""}</td>`));
    html += "</tr>";
  });

  html += "</tbody></table>";
  resultado.innerHTML = html;

}

document.getElementById("exportar-csv").addEventListener("click", () => {
  const table = document.querySelector("#resultado-reporte table");
  if (!table) return alert("Genera un reporte primero.");

  let csv = [];
  const rows = table.querySelectorAll("tr");

  rows.forEach(row => {
    const cols = Array.from(row.querySelectorAll("th, td"))
      .map(col => `"${col.innerText}"`);
    csv.push(cols.join(","));
  });

  const blob = new Blob([csv.join("\\n")], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "reporte.csv";
  a.click();
  URL.revokeObjectURL(url);
});

document.getElementById("exportar-pdf").addEventListener("click", () => {
  const table = document.querySelector("#resultado-reporte table");
  if (!table) return alert("Genera un reporte primero.");

  const ventana = window.open("", "_blank");
  ventana.document.write("<html><head><title>Reporte PDF</title>");
  ventana.document.write("<style>table {width: 100%; border-collapse: collapse;} th, td {border: 1px solid #000; padding: 6px; text-align: left;}</style>");
  ventana.document.write("</head><body>");
  ventana.document.write("<h2>Reporte Exportado</h2>");
  ventana.document.write(table.outerHTML);
  ventana.document.write("</body></html>");
  ventana.document.close();
  ventana.print();
});
