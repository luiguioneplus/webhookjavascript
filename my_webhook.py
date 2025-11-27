from asyncio.windows_events import INFINITE
from flask import Flask, jsonify, request
import os
from datetime import datetime
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

@app.route("/", methods=["GET"])
def home():
    return jsonify(
        {"status": "running", "message": "API de Webhook funcionando correctamente"}
    )

# Endpoint para recibir el status del scrapper (POST)
@app.route("/webhook/scrapper_status", methods=["POST"])
def webhook_scrapper_status_post():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No se recibieron datos JSON"
            }), 400
        
        # Obtener el status del JSON recibido
        status = data.get("status", "unknown").lower()
        
        # Ruta absoluta del archivo
        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "scrapper_status.txt"
        )
        
        # Guardar el status con timestamp
        timestamp = datetime.now().isoformat()
        content = f"{status}\n{timestamp}\n{str(data)}"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        # También guardar log completo
        log_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "scrapper_log.txt"
        )
        
        log_entry = f"\n{'='*60}\n[{timestamp}]\nStatus: {status}\nData: {data}\n{'='*60}\n"
        
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
        
        return jsonify({
            "status": "success",
            "message": "Status recibido y guardado correctamente",
            "data_received": data,
            "timestamp": timestamp
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al guardar el status: {str(e)}"
        }), 500

# Endpoint para consultar el status del scrapper (GET) - CORREGIDO el nombre
@app.route("/webhook/scrapper_status", methods=["GET"])
def webhook_scrapper_status_get():
    try:
        # Usa una ruta absoluta para el archivo
        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "scrapper_status.txt"
        )
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        
        # Parsear el JSON del archivo
        import json
        data = json.loads(content)
        
        # Obtener status y mensaje del JSON
        status = data.get("status", "unknown").lower()
        mensaje = data.get("mensaje", "Sin mensaje")
        infinite= data.get("infinite", "Sin infinite")
        
        if status == "success":
            return jsonify({
                "status": "success",
                "message": mensaje,
                "infinite":infinite,
                "data": data
            })
        elif status == "error":
            return jsonify({
                "status": "error",
                "message": mensaje,
                "data": data
            })
        else:
            return jsonify({
                "status": "unknown",
                "message": f"Estado desconocido: {status}",
                "data": data
            })
            
    except FileNotFoundError:
        return jsonify({
            "status": "error",
            "message": "No se encontró el archivo de estado del scrapper."
        }), 404
    
    except json.JSONDecodeError as e:
        return jsonify({
            "status": "error",
            "message": f"Error al parsear JSON del archivo: {str(e)}"
        }), 500
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al consultar el estado: {str(e)}"
        }), 500

# Endpoint para ver todos los logs
@app.route("/webhook/logs", methods=["GET"])
def view_logs():
    try:
        log_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "scrapper_log.txt"
        )
        
        if not os.path.exists(log_path):
            return jsonify({
                "status": "info",
                "message": "No hay logs disponibles aún"
            }), 404
        
        with open(log_path, "r", encoding="utf-8") as f:
            logs = f.read()
        
        return jsonify({
            "status": "success",
            "logs": logs
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al leer logs: {str(e)}"
        }), 500

# Endpoint para limpiar logs
@app.route("/webhook/clear_logs", methods=["DELETE"])
def clear_logs():
    try:
        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "scrapper_status.txt"
        )
        log_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "scrapper_log.txt"
        )
        
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(log_path):
            os.remove(log_path)
        
        return jsonify({
            "status": "success",
            "message": "Logs eliminados correctamente"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al eliminar logs: {str(e)}"
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"""
╔════════════════════════════════════════════════╗
║   🚀 API Webhook Flask corriendo              ║
╚════════════════════════════════════════════════╝

📍 URL: http://0.0.0.0:{port}

📋 Endpoints disponibles:
   GET  /                           - Estado del API
   POST /webhook/scrapper_status    - Recibir status
   GET  /webhook/scrapper_status    - Consultar status
   GET  /webhook/logs               - Ver todos los logs
   DELETE /webhook/clear_logs       - Limpiar logs
    """)
    app.run(host="0.0.0.0", port=port, debug=DEBUG)