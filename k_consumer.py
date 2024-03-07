import pika
import sqlite3
import telebot

# Telegram Bot API token
telegram_token = '6614911782:AAGzAsKCVOwKeQuwFkBSToZpfNq9foN-zHQ'
bot = telebot.TeleBot(telegram_token)

# Conexão com o RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declaração da fila
channel.queue_declare(queue='input_queue')

# Conexão com o SQLite
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Criação da tabela se não existir
c.execute('''CREATE TABLE IF NOT EXISTS messages
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, subject TEXT)''')

# Função para gravar mensagem no SQLite e enviar para o Telegram
def callback(ch, method, properties, body):
    message = eval(body)  # Converte a mensagem em um dicionário Python
    print("Received:", message)

    # Grava a mensagem no banco de dados SQLite
    c.execute("INSERT INTO messages (name, subject) VALUES (?, ?)", (message['name'], message['subject']))
    conn.commit()

    # Envia a mensagem para o Telegram
    send_telegram_message(message)

# Função para enviar mensagem para o Telegram
def send_telegram_message(message):
    chat_id = '1366944065'  # Replace with your chat ID
    text = f"New message:\nName: {message['name']}\nSubject: {message['subject']}"
    bot.send_message(chat_id, text)

# Consumindo mensagens da fila
channel.basic_consume(queue='input_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages...')
channel.start_consuming()
