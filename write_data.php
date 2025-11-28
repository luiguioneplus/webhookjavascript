<?php
    // 1. Permitir acceso (CORS) - Importante si pruebas desde distintos puertos/dominios
    header("Access-Control-Allow-Origin: *");
    header("Content-Type: application/json; charset=UTF-8");
    header("Access-Control-Allow-Methods: POST");
    header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");

    // 2. Obtener los datos crudos (RAW)
    $jsonRecibido = file_get_contents('php://input');

    // 3. Decodificar el JSON a un Array asociativo de PHP
    $data = json_decode($jsonRecibido, true);

    // --- ZONA DE DEBUGGING ---
    // Como es un webhook, no verás un "echo" en pantalla. 
    // La mejor forma de verificar si llegó es guardarlo en un archivo de texto.
    if ($data) {
        $log = date("Y-m-d H:i:s") . " - Datos recibidos: " . print_r($data, true) . PHP_EOL;
        file_put_contents('webhook_log.txt', $log, FILE_APPEND);
        
        // Responder al JS que todo salió bien
        echo json_encode(["status" => "exito", "mensaje" => "Datos procesados"]);
    } else {
        echo json_encode(["status" => "error", "mensaje" => "No llegaron datos válidos"]);
    }
?>