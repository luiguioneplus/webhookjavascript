<?php
// Habilitar CORS si es necesario (para peticiones desde otros dominios)
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
$json = file_get_contents('php://input');
$datos = json_decode($json, true);
echo $datos;
// Manejar preflight request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

// Método 1: Recibir datos JSON
if ($_SERVER['REQUEST_METHOD'] === 'POST' && 
    isset($_SERVER['CONTENT_TYPE']) && 
    strpos($_SERVER['CONTENT_TYPE'], 'application/json') !== false) {
    
    $json = file_get_contents('php://input');
    $datos = json_decode($json, true);
    
    $estado = $datos['status'] ?? '';
    $mensaje = $datos['mensaje'] ?? '';
    $metodo = $datos['metodo'] ?? 0;
    
    // Procesar datos...
    
    echo datos ;
    print_r($datos);
    echo("hola");
 # Inicia el servidor PHP y verás todo en tiempo real


# Luego abre tu HTML con JavaScript en el navegador
# Los datos aparecerán en la terminal automáticamente





    // Responder con JSON
    header('Content-Type: application/json');
    echo json_encode([
        'success' => true,
        'mensaje' => 'Datos recibidos correctamente',
        'datos_recibidos' => $datos
    ]);
    exit;
}