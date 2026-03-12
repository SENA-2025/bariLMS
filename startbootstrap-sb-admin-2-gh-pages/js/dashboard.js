const dashboardContent = {
  Administrador: {
    area: "Direccionamiento institucional",
    heroTitle: "Tablero del Administrador",
    heroText:
      "Supervisa la operacion general de SENALearn, define lineamientos y controla el acceso de los perfiles del LMS.",
    metrics: [
      { label: "Usuarios activos", value: "1,284", icon: "fa-users" },
      { label: "Centros vinculados", value: "14", icon: "fa-building" },
      { label: "Roles configurados", value: "4", icon: "fa-user-shield" },
      { label: "Sesiones hoy", value: "326", icon: "fa-sign-in-alt" },
    ],
    tasks: [
      ["Gestion de usuarios", "Aprobar nuevas cuentas y validar asignacion de perfiles."],
      ["Configuracion LMS", "Definir parametros base, regionales y politicas institucionales."],
      ["Seguimiento", "Consultar indicadores de uso, permanencia y actividad por centro."],
    ],
    table: [
      ["Regional Distrito Capital", "98%", "Sin novedades"],
      ["Regional Antioquia", "94%", "Actualizar instructores"],
      ["Regional Valle", "91%", "Revision de permisos"],
    ],
  },
  Administrativo: {
    area: "Apoyo academico y operativo",
    heroTitle: "Tablero Administrativo",
    heroText:
      "Consolida fichas, programas, ambientes y apoyo documental para el despliegue de la formacion por proyectos.",
    metrics: [
      { label: "Fichas activas", value: "86", icon: "fa-id-badge" },
      { label: "Programas", value: "27", icon: "fa-graduation-cap" },
      { label: "Ambientes", value: "49", icon: "fa-door-open" },
      { label: "Solicitudes", value: "12", icon: "fa-clipboard-list" },
    ],
    tasks: [
      ["Matricula", "Consolidar aprendices por ficha y programa."],
      ["Ambientes", "Validar capacidad y disponibilidad por sede."],
      ["Soporte documental", "Publicar formatos y circulares internas."],
    ],
    table: [
      ["ADSI 2675854", "Analisis y Desarrollo", "Completa"],
      ["SST 2675921", "Seguridad y Salud", "Pendiente soporte"],
      ["Cocina 2676018", "Tecnico en Cocina", "Actualizada"],
    ],
  },
  Instructor: {
    area: "Ejecucion formativa",
    heroTitle: "Tablero del Instructor",
    heroText:
      "Organiza resultados de aprendizaje, evidencias, proyectos y seguimiento del avance de cada ficha.",
    metrics: [
      { label: "Fichas a cargo", value: "6", icon: "fa-layer-group" },
      { label: "Proyectos activos", value: "18", icon: "fa-project-diagram" },
      { label: "Evidencias por revisar", value: "43", icon: "fa-tasks" },
      { label: "Alertas de asistencia", value: "5", icon: "fa-user-clock" },
    ],
    tasks: [
      ["Planeacion", "Programar actividades alineadas al proyecto formativo."],
      ["Seguimiento", "Retroalimentar evidencias y avances semanales."],
      ["Evaluacion", "Registrar desempeno por resultado de aprendizaje."],
    ],
    table: [
      ["Ficha 2675854", "Sprint de prototipo", "15 entregas pendientes"],
      ["Ficha 2675860", "Sustentacion parcial", "Programada"],
      ["Ficha 2675902", "Bitacora de proyecto", "Al dia"],
    ],
  },
  Aprendiz: {
    area: "Ruta de aprendizaje",
    heroTitle: "Tablero del Aprendiz",
    heroText:
      "Consulta tu avance del proyecto, entregas, evidencias, horario y comunicados del proceso formativo.",
    metrics: [
      { label: "Avance general", value: "72%", icon: "fa-chart-line" },
      { label: "Evidencias pendientes", value: "4", icon: "fa-file-upload" },
      { label: "Resultados aprobados", value: "11", icon: "fa-check-circle" },
      { label: "Mensajes nuevos", value: "3", icon: "fa-comments" },
    ],
    tasks: [
      ["Proyecto formativo", "Consultar entregables y fechas de corte."],
      ["Ruta individual", "Ver resultados alcanzados y faltantes."],
      ["Comunicacion", "Revisar mensajes de instructor y coordinacion."],
    ],
    table: [
      ["Bitacora semanal", "14 de marzo de 2026", "Pendiente"],
      ["Prototipo funcional", "18 de marzo de 2026", "En progreso"],
      ["Autoevaluacion", "20 de marzo de 2026", "No iniciada"],
    ],
  },
};

function populateDashboard(expectedRole) {
  const session = requireRole(expectedRole);
  if (!session) {
    return;
  }

  const roleData = dashboardContent[expectedRole];
  document.querySelectorAll("[data-session-name]").forEach((node) => {
    node.textContent = session.name;
  });
  document.querySelectorAll("[data-session-role]").forEach((node) => {
    node.textContent = session.role;
  });
  document.querySelectorAll("[data-session-email]").forEach((node) => {
    node.textContent = session.email;
  });
  document.querySelectorAll("[data-dashboard-title]").forEach((node) => {
    node.textContent = roleData.heroTitle;
  });
  document.querySelectorAll("[data-dashboard-area]").forEach((node) => {
    node.textContent = roleData.area;
  });
  document.querySelectorAll("[data-dashboard-text]").forEach((node) => {
    node.textContent = roleData.heroText;
  });

  const metricsContainer = document.getElementById("metricCards");
  const tasksContainer = document.getElementById("taskList");
  const tableBody = document.getElementById("dashboardTableBody");

  if (metricsContainer) {
    metricsContainer.innerHTML = roleData.metrics
      .map(
        (metric) => `
          <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-sena shadow h-100 py-2">
              <div class="card-body">
                <div class="row no-gutters align-items-center">
                  <div class="col mr-2">
                    <div class="text-xs font-weight-bold text-sena text-uppercase mb-1">${metric.label}</div>
                    <div class="h4 mb-0 font-weight-bold text-gray-800">${metric.value}</div>
                  </div>
                  <div class="col-auto">
                    <div class="sena-stat-icon">
                      <i class="fas ${metric.icon}"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>`,
      )
      .join("");
  }

  if (tasksContainer) {
    tasksContainer.innerHTML = roleData.tasks
      .map(
        (task) => `
          <div class="mb-3">
            <div class="font-weight-bold text-gray-800">${task[0]}</div>
            <div class="small text-muted">${task[1]}</div>
          </div>`,
      )
      .join("");
  }

  if (tableBody) {
    tableBody.innerHTML = roleData.table
      .map(
        (row) => `
          <tr>
            <td>${row[0]}</td>
            <td>${row[1]}</td>
            <td>${row[2]}</td>
          </tr>`,
      )
      .join("");
  }
}
