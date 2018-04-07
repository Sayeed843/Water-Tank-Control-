import paho.mqtt.client as mqtt
import sys
import pymysql as pymymql


class DBoperation():

    def __init__(self, user='root', password='1', host='127.0.0.1',
                 port=3306, dbName='TankControl'):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dbName = dbName

    def dbConnection(self):
        try:
            self.db = pymymql.connect(user=self.user, password=self.password,
                                      host=self.host, port=self.port, db=self.dbName)
            print("Database Connection")
        except pymymql.Error as e:
            print(e)
            print("Could Not connect to the database")
            print("Close...")
            sys.exit()
        self.cursor = self.db.cursor()

    def executeData(self, sql, args):
        try:
            self.cursor.execute(sql, args)
            self.db.commit()
            print("Execute Data into Database.......OK")
        except pymymql.Error as e:
            self.db.rollback()
            print(e)
            print("Execute Data into Database.......Failed")

    def returnCursor(self):
        return self.cursor

    def display(self):
        for element in self.cursor:
            print(element)


class MqttBroker():
    db = DBoperation()

    def __init__(self, server="m12.cloudmqtt.com", port=13348, username="wvxwjqte", password="EbeW6HIvrbuS"):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.client = mqtt.Client()

    def mqttConnection(self):
        try:
            self.client.username_pw_set(self.username, self.password)
            self.client.connect(self.server, self.port)
        except self.client.Error as e:
            print(e)
            print("Could not connect to the MQTT broker....")
            print("Closing....")
            sys.exit()

    def on_connect(self, client, userdata, flags, rc):
        print("Connedted -Result code: " + str(rc))

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        sensorValue = str(msg.payload).split("/")

        sensorTableInsert = "INSERT INTO `TankControl`.`wpc_sensor`\
        (`upperSensor`,`lowerSensor`,`mac_id`) \
        VALUES(%s,%s ,\
        (SELECT `wpc_bdwaterboard`.`id`\
        FROM `TankControl`.`wpc_bdwaterboard` \
        WHERE `wpc_bdwaterboard`.`mac` = %s))"

        args = (sensorValue[0], sensorValue[1], msg.topic)
        self.db.dbConnection()
        self.db.executeData(sensorTableInsert, args)

    def mqttLoopForever(self):
        self.client.on_connect = self.on_connect
        self.client.subscribe("/#")
        self.client.on_message = self.on_message
        try:
            self.client.loop_forever()
            print("Okay Man")
        except KeyboardInterrupt:
            print("Closing...")


# database = DBoperation()
broker = MqttBroker()
# database.dbConnection()
broker.mqttConnection()
broker.mqttLoopForever()
