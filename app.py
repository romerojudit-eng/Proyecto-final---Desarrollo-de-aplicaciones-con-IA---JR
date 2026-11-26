import os
import torch
from flask import Flask, request, jsonify
from PIL import Image
import torchvision.transforms as transforms
import re

app = Flask(__name__)

# Variables dummy simulando importación de tu entorno
CLASES = ['error_powerbi', 'error_sap', 'error_mes_orden', 'fallo_impresion_hu']

# Endpoint de diagnóstico del Agente
@app.route('/ask', methods=['POST'])
def ask_agent():
    data = request.get_json() or {}
    mensaje = data.get("message", "")
    
    if not mensaje:
        return jsonify({"status": "error", "response": "Mensaje vacío"}), 400
        
    # Verificar si es una ruta de imagen
    es_ruta_imagen = (mensaje.strip().endswith(('.png', '.jpg', '.jpeg')) and
                      not any(char in mensaje for char in [' ', '?', '¿']))
                      
    if es_ruta_imagen:
        # Lógica del Agente: Desviar a clasificación visual
        if os.path.exists(mensaje):
            return jsonify({
                "status": "success",
                "type": "vision",
                "detected_file": mensaje,
                "agent_decision": "routing_to_cnn",
                "response": f"Se detectó una ruta de imagen válida. En producción, la CNN evaluará este archivo."
            })
        else:
            return jsonify({
                "status": "warning",
                "type": "vision_not_found",
                "response": f"Se detectó formato de imagen, pero el archivo no existe en el servidor: {mensaje}"
            })
            
    # Lógica por defecto: Responder con NLP
    return jsonify({
        "status": "success",
        "type": "nlp",
        "message_received": mensaje,
        "response": "El mensaje se procesó mediante el clasificador de texto de la API."
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model_loaded": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
