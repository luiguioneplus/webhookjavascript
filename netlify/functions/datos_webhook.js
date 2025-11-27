
exports.handler = async (event, context) => {
    if (event.httpMethod !== "POST") {
        return { 
            statusCode: 405, 
            body: "Method Not Allowed" 
        };
    }

    let datosRecibidos;
    try {
        datosRecibidos = JSON.parse(event.body);

        // --- 1. CONVERTIR DATOS A PARÁMETROS DE URL ---
        // Convertimos el objeto JSON a una cadena de texto (string)
        const datosComoString = JSON.stringify(datosRecibidos);
        
        // Codificamos la cadena para que sea segura en la URL (ej. maneja espacios, símbolos)
        const datosCodificados = encodeURIComponent(datosComoString);

        // --- 2. DEFINIR LA URL DE REDIRECCIÓN ---
        // IMPORTANTE: Cambia 'https://tu-sitio.netlify.app/vista' por la URL de tu vista
        const urlVista = "https://sage-pie-4597de.netlify.app"; 
        
        // Creamos la URL final con los datos adjuntos como parámetro 'data'
        const urlRedireccion = `${urlVista}?data=${datosCodificados}`;

        // --- 3. RESPUESTA DE REDIRECCIÓN (HTTP 302) ---
        return {
            statusCode: 302, // Código HTTP para "Found" o "Redireccionado Temporalmente"
            headers: {
                // Le dice al cliente (navegador/servicio) que vaya a esta nueva URL
                "Location": urlRedireccion
            },
            // El cuerpo es opcional en una redirección, pero lo incluimos por buena práctica
            body: "Redirigiendo a la vista con los datos..."
        };

    } catch (error) {
        console.error("Error al procesar/redirigir:", error);
        return { 
            statusCode: 500, 
            body: JSON.stringify({ error: "Error interno al procesar el webhook." }) 
        };
    }
};