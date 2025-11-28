// La función principal que se exporta y es invocada por Netlify
exports.handler = async (event, context) => {
    // 1. **Verificación de Método:** Un webhook casi siempre usa el método POST.
    if (event.httpMethod !== "POST") {
        return { 
            statusCode: 405, 
            body: "Method Not Allowed. Solo se permiten solicitudes POST." 
        };
    }

    // 2. **Procesar el Cuerpo (Body) de la Solicitud:**
    let datosRecibidos;
    try {
        // Los datos del webhook vienen en event.body como una cadena de texto.
        // Se debe parsear a un objeto JSON.
        datosRecibidos = JSON.parse(event.body);

    } catch (error) {
        console.error("Error al parsear el JSON:", error);
        return { 
            statusCode: 400, 
            body: JSON.stringify({ message: "Solicitud inválida. Se espera un JSON válido." }) 
        };
    }

    // 3. **Lógica del Webhook (El Corazón de la Función):**
    console.log("--- Webhook Recibido ---");
    console.log("Datos de la carga (payload):", datosRecibidos);
    
    // *******************************************************************
    // AQUÍ es donde iría tu lógica:
    // - Almacenar los 'datosRecibidos' en una base de datos (FaunaDB, Supabase, etc.).
    // - Enviar un email de notificación.
    // - Disparar otra acción o microservicio.
    // *******************************************************************
    
    // 4. **Respuesta Exitosa (¡Crucial!):**
    // Debes devolver un 200 OK rápidamente para que el servicio remitente sepa
    // que el webhook fue recibido exitosamente.
    enviarDatosJSON(datosRecibidos)
    async function enviarDatosJSON() {
         
        try {
            const response = await fetch('write_data.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(datosRecibidos)
            });
    
            const resultado = await response.json();
            console.log('Respuesta:', resultado);
        } catch (error) {
            console.error('Error:', error);
        }
    }
    return {
        statusCode: 200,
        body: JSON.stringify({ 
            message: "Webhook de Netlify procesado exitosamente.",
            idRecibido: datosRecibidos.status || "N/A" // Ejemplo de respuesta
        })
    };
};