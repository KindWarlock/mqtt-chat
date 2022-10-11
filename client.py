import paho.mqtt.client as mqtt_client
import random
import sys
 
def on_message(client, payload, message):
    data = str(message.payload.decode('utf-8'))
    topic = str(message.topic)
    name = topic.split("/")[-1]
    # я не нашла, как перенаправить input, чтобы введенное сообщение не отображалось, 
    # поэтому оно просто не дублируется при получении
    if name != username:
        print(f'{name}: {data}')


broker = 'broker.emqx.io'

client_id = f'test_{random.randint(10000,99999)}'
client = mqtt_client.Client(client_id)
client.on_message = on_message

try:
    client.connect(broker)
except Exception:
    print('Failed to connect')
    exit()

room = sys.argv[1]
username = sys.argv[2]
client.loop_start()

print('\nWELCOME TO THE CLUB, BUDDY')

client.subscribe(room + '/+')
room = room + '/' + username
client.publish(room, 'HAS JOINED THE ROOM'.encode('utf-8'))
print()
while True:
    try:
        msg = input()
        client.publish(room, msg)
    except KeyboardInterrupt:
        print()
        client.publish(room, 'HAS LEFT THE ROOM'.encode('utf-8'))
        client.disconnect()
        client.loop_stop()
        print('\nSTOPPED')
        print()
        exit()
