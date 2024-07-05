// static/js/user/validations.js
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("registerForm");

    // Agregar eventos de entrada para limitar la entrada solo a números
    const numericFields = ["doc", "phone"];
    numericFields.forEach(function(fieldId) {
        const field = document.getElementById(fieldId);
        field.addEventListener("input", function () {
            this.value = this.value.replace(/\D/g, ''); // Eliminar caracteres no numéricos
        });
    });

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        if (!validateForm()) {
            return;
        }

        // Realizar la solicitud de registro
        const formData = new FormData(form);
        fetch(form.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                Swal.fire({
                    icon: 'success',
                    title: 'Registro Exitoso pudiste rellenar esto sin confundirte  toma un premio 🏆 :D ',
                    text: data.message,
                }).then(() => {
                    window.location.href = data.redirect_url; // Redirigir al inicio de sesión
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: data.message,
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Hubo un problema con el registro. Inténtalo de nuevo más tarde.',
            });
        });
    });

    function validateForm() {
        const doc = document.getElementById("doc");
        const phone = document.getElementById("phone");
        const email = document.getElementById("email");
        const password = document.getElementById("password");
        const confirmPassword = document.getElementById("confirm_password");

        // Validación de documento
        if (!/^\d{8}$/.test(doc.value)) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'El documento debe tener 8 dígitos.',
            });
            doc.focus();
            return false;
        }

        // Validación de teléfono
        if (!/^\d{9}$/.test(phone.value)) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'El teléfono debe tener 9 dígitos.',
            });
            phone.focus();
            return false;
        }

        // Validación de correo electrónico
        if (!/\S+@\S+\.\S+/.test(email.value)) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Ingrese un correo electrónico válido.',
            });
            email.focus();
            return false;
        }

        // Validación de contraseñas
        if (password.value !== confirmPassword.value) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Las contraseñas no coinciden.',
            });
            password.focus();
            return false;
        }

        return true;
    }
});
