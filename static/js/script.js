// VARIABLES//
var menu = document.querySelector('#hamburger-menu .hamburger-list');
var overlay = document.querySelector('#overlay');

/*abrir el menu hamburgesa */
document.getElementById('hamburger-button').addEventListener('click', function() {
    menu.classList.toggle('open');
    overlay.style.display = 'block'; // Muestra el overlay cuando se abre el menú
});

/*cerrar el menu hamburgesa */
document.getElementById('close-button').addEventListener('click', function() {
    menu.classList.remove('open');
    overlay.style.display = 'none'; // Oculta el overlay cuando se cierra el menú
});

// Seleccionar el botón interactivo y el contenedor del formulario
const botonInteractivo = document.querySelector('.boton-interactivo');
const contenedorFormulario = document.querySelector('.contenedor-formulario');

// Agregar evento click al botón interactivo
botonInteractivo.addEventListener('click', () => {
// Toggle para abrir y cerrar el formulario
contenedorFormulario.classList.toggle('abierto');
  
// efecto de transición
contenedorFormulario.style.transition = 'opacity 0.5s';
    if (contenedorFormulario.classList.contains('abierto')) {
      contenedorFormulario.style.opacity = '1';
      contenedorFormulario.style.display = 'block'; 
// Mostrar el contenedor del formulario
    } else {
      contenedorFormulario.style.opacity = '0';
      setTimeout(() => {
        contenedorFormulario.style.display = 'none'; 
// Ocultar el contenedor del formulario
      }, 500); 
// Esperar 500ms para ocultar el formulario
}});

// Corvette Carousel
const images = document.querySelectorAll('.imagenes-corvette-images');
let currentIndex = 0;

function showNextImage() {
  images[currentIndex].classList.remove('imagenes-corvette-images-1');
  currentIndex = (currentIndex + 1) % images.length;
  images[currentIndex].classList.add('imagenes-corvette-images-1');
  images[(currentIndex - 1 + images.length) % images.length].classList.remove('imagenes-corvette-images-2');
  images[currentIndex].classList.add('imagenes-corvette-images-2');
}
setInterval(showNextImage, 3500);

//nuevo2
document.addEventListener('DOMContentLoaded', function() {
  const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

  dropdownToggles.forEach(toggle => {
    toggle.addEventListener('mouseover', function() {
      this.classList.add('active');
      const dropdownMenu = this.nextElementSibling;
      dropdownMenu.style.display = 'flex';
    });

    toggle.addEventListener('mouseout', function() {
      this.classList.remove('active');
      const dropdownMenu = this.nextElementSibling;
      dropdownMenu.style.display = 'none';
    });
  });
});


