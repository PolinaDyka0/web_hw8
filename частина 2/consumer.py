import pika
from mongoengine import connect
from model import Contact

# Підключення до RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

# Створення черги
channel.queue_declare(queue='contacts_queue')

# Підключення до MongoDB
connect('mydatabase2', host='mongodb+srv://userweb10:567234@cluster0.h9yiutj.mongodb.net/?retryWrites=true&w=majority')

# Функція-заглушка для імітації надсилання email
def send_email(email):
    print(f'Sending email to {email}...')

# Обробка повідомлень з черги RabbitMQ
def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects.get(id=contact_id)
    if not contact.email_sent:
        send_email(contact.email)
        contact.email_sent = True
        contact.save()
        print(f'Email sent to {contact.email}')

# Очікування повідомлень з черги
channel.basic_consume(queue='contacts_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages...')

# Постійне очікування повідомлень
channel.start_consuming()
