const inputUrl = document.getElementById("inputUrl");
const btnAgregar = document.getElementById("btnAgregar");
const btnEliminar = document.getElementById("btnEliminar");
const galeria = document.getElementById("galeria");

let imagenSeleccionada = null;

function agregarImagen(){
    const url = inputUrl.value.trim();
    if(!url) return alert("Ingresa una URL válida");

    galeria.querySelector(".mensaje-vacio")?.remove();

    const cont = document.createElement("div");
    cont.className = "imagen-container";

    const img = document.createElement("img");
    img.src = url;
    img.alt = "Imagen de galería";

    img.onerror = () =>{
        alert("No se pudo cargar la imagen");
        cont.remove();
        if(!galeria.children.length) mostrarMensajeVacio();
    };

    cont.onclick = () => seleccionarImagen(cont);

    cont.appendChild(img);
    galeria.appendChild(cont);
    inputUrl.value = "";
}

function seleccionarImagen(contenedor){
    imagenSeleccionada?.classList.remove("seleccionada");
    contenedor.classList.add("seleccionada");
    imagenSeleccionada = contenedor;
    btnEliminar.disabled = false;
}

function eliminarImagenSeleccionada(){
    if(!imagenSeleccionada) return;
    imagenSeleccionada.remove();
    imagenSeleccionada = null;
    btnEliminar.disabled = true;
    if(!galeria.children.length) mostrarMensajeVacio();
}

function mostrarMensajeVacio(){
    galeria.innerHTML =
        '<div class="mensaje-vacio">No hay imágenes. ¡Agrega una!</div>';
}

btnAgregar.onclick = agregarImagen;
btnEliminar.onclick = eliminarImagenSeleccionada;

inputUrl.addEventListener("keydown",e=>{
    if(e.key==="Enter") agregarImagen();
});

document.addEventListener("keydown",e=>{
    if((e.key==="Delete"||e.key==="Backspace") && imagenSeleccionada){
        if(e.key==="Backspace" && document.activeElement!==inputUrl)
            e.preventDefault();
        eliminarImagenSeleccionada();
    }
});