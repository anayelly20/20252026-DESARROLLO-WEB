// ALERTA
document.getElementById('btnAlerta').addEventListener('click', () => {
  alert('Bienvenido a mi proyecto interactivo 🚀');
});

// FORMULARIO CONTACTO
document.getElementById('formContacto').addEventListener('submit', e => {
  e.preventDefault();

  const nombre = document.getElementById('nombre').value;
  const correo = document.getElementById('correo').value;
  const mensaje = document.getElementById('mensaje').value;

  if (!nombre || !correo || !mensaje) {
    alert('Todos los campos son obligatorios');
    return;
  }

  alert('Mensaje enviado correctamente ✅');
  e.target.reset();
});

// AÑADIR PRODUCTOS
const formProducto = document.getElementById('formProducto');
const tabla = document.getElementById('tablaProductos');

formProducto.addEventListener('submit', e => {
  e.preventDefault();

  const nombre = document.getElementById('nombreProducto').value;
  const precio = document.getElementById('precioProducto').value;

  if (!nombre || !precio) {
    alert('Complete los datos del producto');
    return;
  }

  const fila = document.createElement('tr');
  fila.innerHTML = `
    <td>${tabla.children.length + 1}</td>
    <td>${nombre}</td>
    <td>$${precio}</td>
  `;

  fila.addEventListener('click', () => {
    alert(`Producto: ${nombre}\nPrecio: $${precio}`);
  });

  tabla.appendChild(fila);
  formProducto.reset();
});
