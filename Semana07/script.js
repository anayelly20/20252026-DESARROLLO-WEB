// Productos iniciales
const productos = [
    {
        nombre: "Laptop HP",
        precio: 899.99,
        descripcion: "Laptop con procesador Intel Core i7, 16GB RAM y 512GB SSD."
    },
    {
        nombre: "Mouse Inalámbrico",
        precio: 25.99,
        descripcion: "Mouse ergonómico con conexión Bluetooth."
    },
    {
        nombre: "Teclado Mecánico",
        precio: 79.99,
        descripcion: "Teclado mecánico RGB con switches Cherry MX."
    },
    {
        nombre: "Monitor 27 pulgadas",
        precio: 299.99,
        descripcion: "Monitor Full HD con tecnología IPS."
    }
];

// Crear HTML de un producto
function crearProductoHTML(producto) {
    return `
        <li class="producto">
            <h3>${producto.nombre}</h3>
            <p class="precio">$${producto.precio.toFixed(2)}</p>
            <p>${producto.descripcion}</p>
        </li>
    `;
}

// Mostrar productos en pantalla
function renderizarProductos() {
    const lista = document.getElementById("listaProductos");
    lista.innerHTML = "";

    productos.forEach(producto => {
        lista.innerHTML += crearProductoHTML(producto);
    });
}

// Agregar producto nuevo
function agregarProducto() {
    const nuevosProductos = [
        {
            nombre: "Auriculares Bluetooth",
            precio: 59.99,
            descripcion: "Auriculares inalámbricos con cancelación de ruido."
        },
        {
            nombre: "Webcam HD",
            precio: 89.99,
            descripcion: "Cámara web Full HD con micrófono."
        },
        {
            nombre: "Disco Duro Externo 1TB",
            precio: 65.99,
            descripcion: "Almacenamiento portátil USB 3.0."
        }
    ];

    const productoAleatorio =
        nuevosProductos[Math.floor(Math.random() * nuevosProductos.length)];

    productos.push(productoAleatorio);
    renderizarProductos();
}

// Evento del botón
document.getElementById("btnAgregar")
    .addEventListener("click", agregarProducto);

// Mostrar productos al cargar la página
renderizarProductos();
