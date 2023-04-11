import pika
from faker import Faker
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

# Генерація фейкових контактів та їх збереження в базу даних та чергу RabbitMQ
def generate_contacts(num_contacts):
    faker = Faker()
    for i in range(num_contacts):
        full_name = faker.name()
        email = faker.email()
        contact = Contact(full_name=full_name, email=email)
        contact.save()
        message = str(contact.id)
        channel.basic_publish(exchange='', routing_key='contacts_queue', body=message)
        print(f'Contact {i+1} added to the queue')

# Генерація 10 контактів
generate_contacts(10)

# Закриття підключення до RabbitMQ
connection.close()
