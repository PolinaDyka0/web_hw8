import pika
import random
from mongoengine import connect
from model_for_additional_task import Contactadd
from faker import Faker

# Підключення до RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

# Створення черг для email та SMS
channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')

# Підключення до MongoDB
connect('mydatabase2', host='mongodb+srv://userweb10:567234@cluster0.h9yiutj.mongodb.net/?retryWrites=true&w=majority')

# Генерація фейкових контактів та їх збереження в базу даних та черги RabbitMQ
def generate_contacts(num_contacts):
    faker = Faker()
    for i in range(num_contacts):
        full_name = faker.name()
        email = faker.email()
        phone_number = faker.phone_number()
        preferred_method = random.choice(['email', 'sms'])
        contact = Contactadd(full_name=full_name, email=email, phone_number=phone_number, preferred_method=preferred_method)
        contact.save()
        if preferred_method == 'email':
            queue_name = 'email_queue'
        else:
            queue_name = 'sms_queue'
        message = str(contact.id)
        channel.basic_publish(exchange='', routing_key=queue_name, body=message)
        print(f'Contact {i+1} added to the {queue_name}')

# Генерація 10 контактів
generate_contacts(10)

# Закриття підключення до RabbitMQ
connection.close()
