$(document).ready(function() {
    $('#searchDniButton').click(function() {
        const dni = $('#doc').val();
        
        if (dni.length === 8 && $.isNumeric(dni)) {
            fetchDniInfo(dni);
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Por favor, ingrese un DNI válido de 8 dígitos.',
            });
        }
    });
    function fetchDniInfo(dni) {
        const apiKey = ''; // Reemplaza con tu clave de API
        const url = `https://apiperu.dev/api/dni/${dni}`;

        $.ajax({
            url: url,
            headers: {
                'Authorization': `Bearer ${apiKey}`
            },
            success: function(data) {
                if (data && data.data) {
                    const nombres = data.data.nombres.split(' ');
                    const nombre = nombres[0];
                    const apellidoPaterno = data.data.apellido_paterno;
                    const apellidoMaterno = data.data.apellido_materno;

                    console.log('Nombre:', nombre); // Log para depuración
                    console.log('Apellido Paterno:', apellidoPaterno); // Log para depuración
                    console.log('Apellido Materno:', apellidoMaterno); // Log para depuración

                    $('#username').val(nombre);
                    $('#last_name').val(apellidoPaterno);
                    $('#mother_last_name').val(apellidoMaterno);
                } else {
                    alert('No se encontró información para el DNI proporcionado.');
                }
            },
            error: function() {
                alert('Hubo un error al consultar la información del DNI.');
            }
        });
    }
});