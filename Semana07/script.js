let productos = [
    {
        nombre: "Ana Lopez",
        precio: 30,
        descripcion: "cebolla",
        imagen: "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=300"
    },
    {
        nombre: "lapto",
        precio: 500,
        descripcion: "computadora",
        imagen: "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300"
    }
];

const lista = document.getElementById("listaProductos");
const btnAgregar = document.getElementById("btnAgregar");

function renderizarProductos() {
    lista.innerHTML = "";

    productos.forEach(producto => {
        const li = document.createElement("li");

        li.innerHTML = `
            <div class="producto-info">
                <div class="producto-nombre">${producto.nombre}</div>
                <div class="producto-precio">${producto.precio}</div>
                <div class="producto-descripcion">${producto.descripcion}</div>
            </div>
            ${producto.imagen ? `<img src="${producto.imagen}" class="producto-imagen">` : ""}
        `;

        lista.appendChild(li);
    });
}

function agregarProducto() {
    const nombre = document.getElementById("nombre").value;
    const precio = document.getElementById("precio").value;
    const descripcion = document.getElementById("descripcion").value;
    const imagen = document.getElementById("imagen").value;

    if (!nombre || !precio || !descripcion) {
        alert("Completa todos los campos obligatorios");
        return;
    }

    productos.push({ nombre, precio, descripcion, imagen });

    document.getElementById("nombre").value = "";
    document.getElementById("precio").value = "";
    document.getElementById("descripcion").value = "";
    document.getElementById("imagen").value = "";

    renderizarProductos();
}

btnAgregar.addEventListener("click", agregarProducto);

renderizarProductos();
