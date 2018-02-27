import paho.mqtt.client as mqtt
import sys
import pymysql

# Open connection with databases
try:
    db = pymysql.connect(user='root', password='1', host='127.0.0.1',
                         port=3306, db='WaterTankControl')
    print("DB is connected")
except:
    print("Could not connect to the database")
    print("Close...")
    sys.exit()

# Preparing cursor
cursor = db.cursor()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected - Result code: " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/#")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

    sql = "INSERT INTO `WaterTankControl`.`wpc_motor`(`mac`,`motorStatus`)VALUES(%s,%s);"
    args = (msg.topic, str(msg.payload))

    try:
        # Execute a SQL command
        cursor.execute(sql, args)
        db.commit()
        print("Saving in database ... OK")
    except:
        db.rollback()
        print("Saving in database ... Failed")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect("CLOUD_SERVER", 13348)
except:
    print("Could not connect to the MQTT Broker ...")
    print("Closing...")
    sys.exit()

client.username_pw_set("YOUR_CLOUD_SERVER_USERNAME", "YOUR_CLOUD_SERVER_PASSWORD")

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Closing...")
