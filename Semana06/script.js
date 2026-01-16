const f = id => document.getElementById(id);
const btn = f("btnEnviar");
const exito = f("mensajeExito");

const estado = {
  nombre: false,
  email: false,
  pass: false,
  confirm: false,
  edad: false
};

function activar() {
  btn.disabled = !Object.values(estado).every(v => v);
}

function validar(inputId, errorId, ok) {
  const input = f(inputId);
  const error = f(errorId);

  input.classList.remove("valid", "invalid");
  input.classList.add(ok ? "valid" : "invalid");
  error.classList.toggle("show", !ok);
  activar();
}

f("nombre").addEventListener("input", e => {
  estado.nombre = e.target.value.length >= 3;
  validar("nombre", "nombreError", estado.nombre);
});

f("email").addEventListener("input", e => {
  estado.email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e.target.value);
  validar("email", "emailError", estado.email);
});

f("password").addEventListener("input", e => {
  estado.pass = e.target.value.length >= 8;
  validar("password", "passwordError", estado.pass);
});

f("confirmPassword").addEventListener("input", e => {
  estado.confirm = e.target.value === f("password").value && estado.pass;
  validar("confirmPassword", "confirmPasswordError", estado.confirm);
});

f("edad").addEventListener("input", e => {
  estado.edad = e.target.value >= 18;
  validar("edad", "edadError", estado.edad);
});

f("registroForm").addEventListener("submit", e => {
  e.preventDefault();
  exito.style.display = "block";
  setTimeout(() => exito.style.display = "none", 3000);
});
