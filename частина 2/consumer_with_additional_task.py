import pika
from mongoengine import connect
from model_for_additional_task import Contactadd

# Підключення до RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

# Створення черг для email та SMS
channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')

# Підключення до MongoDB
connect('mydatabase2', host='mongodb+srv://userweb10:567234@cluster0.h9yiutj.mongodb.net/?retryWrites=true&w=majority')

def send_email(email):
    print(f'Sending email to {email}...')
    print('Email sent.')

def send_sms(phone_number):
    print(f'Sending SMS to {phone_number}...')
    print('SMS sent.')


# Обробка повідомлень з черги RabbitMQ для email
def callback_email(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contactadd.objects.get(id=contact_id)
    if not contact.email_sent and contact.preferred_method == 'email':
        send_email(contact.email)
        contact.email_sent = True
        contact.save()
        print(f'Email sent to {contact.email}')

# Обробка повідомлень з черги RabbitMQ для SMS
def callback_sms(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contactadd.objects.get(id=contact_id)
    if not contact.sms_sent and contact.preferred_method == 'sms':
        send_sms(contact.phone_number)
        contact.sms_sent = True
        contact.save()
        print(f'SMS sent to {contact.phone_number}')

# Обробка повідомлень з черги RabbitMQ для email
channel.basic_consume(queue='email_queue', on_message_callback=callback_email, auto_ack=True)

# Обробка повідомлень з черги RabbitMQ для SMS
channel.basic_consume(queue='sms_queue', on_message_callback=callback_sms, auto_ack=True)

# Запуск обробки повідомлень з черги RabbitMQ
print('Waiting for messages...')

# Постійне очікування повідомлень
channel.start_consuming()
