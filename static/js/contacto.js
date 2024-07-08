const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input');

const expresiones = {
    firstname:/^[a-zA-ZÀ-ÿ\s]{1,40}$/,
    lastname:/^[a-zA-ZÀ-ÿ\s]{1,40}$/,
    email: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
    phone: /^\d{7,14}$/
}

const campos = {
    firstname: false,
    lastname: false,
    email: false,
    phone: false
}


const validarFormulario = (e)=>{
    switch (e.target.name){
        case "firstname":
            validarCampo(expresiones.firstname, e.target, 'firstname');   
        break;
        case "lastname":
            validarCampo(expresiones.lastname, e.target, 'lastname');
        break;
        case "email":
            validarCampo(expresiones.email, e.target, 'email');
        break;
        case "phone":
            validarCampo(expresiones.phone, e.target, 'phone');
        break;
    }
}

const validarCampo = (expresion, input, campo)=>{
    if(expresion.test (input.value)){
        document.getElementById(`${campo}`).classList.remove('form-control-incorrecto');
        document.getElementById(`${campo}`).classList.add('form-control-correcto');
        document.querySelector(`#${campo} i`).classList.add('fa-circle-check');
        document.querySelector(`#${campo} i`).classList.remove('fa-circle-xmark');
        document.querySelector(`#error-${campo}.form-control-error`).classList.remove('form-control-error-activo');
        campos[campo] = true;
    } else {
        document.getElementById(`${campo}`).classList.add('form-control-incorrecto'); 
        document.getElementById(`${campo}`).classList.remove('form-control-correcto');
        document.querySelector(`#${campo} i`).classList.remove('fa-circle-check');
        document.querySelector(`#${campo} i`).classList.add('fa-circle-xmark');
        document.querySelector(`#error-${campo}.form-control-error`).classList.add('form-control-error-activo');
        campos[campo] = false;
    }
}

inputs.forEach((input) => {
    input.addEventListener('keyup', validarFormulario);
    input.addEventListener('blur', validarFormulario);
});


formulario.addEventListener('submit', (e) => {
    e.preventDefault();

    const terms = document.getElementById('terms');
    if(campos.firstname && campos.lastname && campos.email && campos.phone && terms.checked){
        formulario.reset();

        document.getElementById('form-control-msj').classList.add('form-control-msj-activo');
        setTimeout(() => {
            document.getElementById('form-control-msj').classList.remove('form-control-msj-activo');
        }, 5000);
        document.querySelectorAll('.form-control-correcto').forEach((icono) => {
           icono.classList.remove('form-control-correcto'); 
        });
    }  else {
		document.getElementById('form-control-error').classList.add('form-control-error-activo');
	}

});
  