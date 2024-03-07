from flask import Flask, request, jsonify
import pika

app = Flask(__name__)

# Configuração da conexão com o RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declara a fila
channel.queue_declare(queue='input_queue')

@app.route('/send', methods=['POST'])
def send_to_queue():
    # Obtém os dados do JSON enviado
    data = request.json

    # Verifica se os dados estão no formato correto
    if 'name' in data and 'subject' in data:
        # Publica os dados na fila
        channel.basic_publish(exchange='', routing_key='input_queue', body=str(data))
        return jsonify({'message': 'Data sent to RabbitMQ queue'}), 200
    else:
        return jsonify({'error': 'Invalid input format'}), 400

if __name__ == '__main__':
    app.run(debug=True)
