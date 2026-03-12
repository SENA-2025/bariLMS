const demoUsers = [
  {
    role: "Administrador",
    email: "admin@senalearn.edu.co",
    password: "Admin123*",
    name: "Laura Moreno",
    dashboard: "dashboard-admin.html",
  },
  {
    role: "Administrativo",
    email: "administrativo@senalearn.edu.co",
    password: "Adminvo123*",
    name: "Carlos Ruiz",
    dashboard: "dashboard-administrativo.html",
  },
  {
    role: "Instructor",
    email: "instructor@senalearn.edu.co",
    password: "Instructor123*",
    name: "Diana Beltran",
    dashboard: "dashboard-instructor.html",
  },
  {
    role: "Aprendiz",
    email: "aprendiz@senalearn.edu.co",
    password: "Aprendiz123*",
    name: "Miguel Torres",
    dashboard: "dashboard-aprendiz.html",
  },
];

const storageKey = "senaLearnSession";

function getSession() {
  const rawSession = localStorage.getItem(storageKey);
  if (!rawSession) {
    return null;
  }

  try {
    return JSON.parse(rawSession);
  } catch (error) {
    localStorage.removeItem(storageKey);
    return null;
  }
}

function saveSession(user) {
  localStorage.setItem(
    storageKey,
    JSON.stringify({
      role: user.role,
      email: user.email,
      name: user.name,
      dashboard: user.dashboard,
      loginAt: new Date().toISOString(),
    }),
  );
}

function clearSession() {
  localStorage.removeItem(storageKey);
}

function resolveUser(email, password, role) {
  return demoUsers.find(
    (user) =>
      user.email.toLowerCase() === email.toLowerCase() &&
      user.password === password &&
      user.role === role,
  );
}

function redirectToDashboard(session) {
  if (!session || !session.dashboard) {
    window.location.href = "login.html";
    return;
  }

  window.location.href = session.dashboard;
}

function setupLogin() {
  const loginForm = document.getElementById("loginForm");
  if (!loginForm) {
    return;
  }

  const currentSession = getSession();
  if (currentSession) {
    redirectToDashboard(currentSession);
    return;
  }

  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const roleInput = document.getElementById("role");
  const feedback = document.getElementById("loginFeedback");
  const quickAccessButtons = document.querySelectorAll("[data-demo-role]");

  quickAccessButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const demoRole = button.getAttribute("data-demo-role");
      const user = demoUsers.find((item) => item.role === demoRole);
      if (!user) {
        return;
      }

      emailInput.value = user.email;
      passwordInput.value = user.password;
      roleInput.value = user.role;
      feedback.classList.add("d-none");
    });
  });

  loginForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const user = resolveUser(emailInput.value.trim(), passwordInput.value, roleInput.value);

    if (!user) {
      feedback.textContent = "Credenciales o perfil incorrectos. Usa uno de los accesos demo listados.";
      feedback.classList.remove("d-none");
      return;
    }

    saveSession(user);
    redirectToDashboard(user);
  });
}

function requireRole(expectedRole) {
  const session = getSession();
  if (!session) {
    window.location.href = "login.html";
    return null;
  }

  if (expectedRole && session.role !== expectedRole) {
    redirectToDashboard(session);
    return null;
  }

  return session;
}

function setupLogout() {
  document.querySelectorAll("[data-action='logout']").forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      clearSession();
      window.location.href = "login.html";
    });
  });
}

setupLogin();
setupLogout();
