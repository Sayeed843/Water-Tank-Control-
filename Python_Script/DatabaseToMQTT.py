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

    def executeData(self, sql):
        try:
            self.cursor.execute(sql)
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
    wtc = WaterTankControl()

    def __init__(self, server="m13.cloudmqtt.com", port=16144, username="tuzdocic", password="Eg9MQUEajoeR"):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.client = mqtt.Client()

    def mqttConnection(self):
        try:
            self.client.username_pw_set(self.username, self.password)
            self.client.connect(self.server, self.port)
            # print("Easy-peasy Man")
        except self.client.Error as e:
            print(e)
            print("Could not connect to the MQTT broker....")
            print("Closing....")
            sys.exit()

    def on_connect(self, client, userdata, flags, rc):
        print("Connedted -Result code: " + str(rc))

    def mqttLoopForever(self):
        self.client.on_connect = self.on_connect
        data = self.wtc.retrieveSensorData()
        self.client.publish()
        self.client.on_message = self.on_message
        try:
            self.client.loop_forever()
            print("Okay Man")
        except KeyboardInterrupt:
            print("Closing...")


class WaterTankControl():

    db = DBoperation()

    def retrieveSensorData(self):
        self.db.dbConnection()
        retrieveSql = "SELECT `wpc_sensor`.`id`,\
                                        `wpc_sensor`.`upperSensor`,\
                                        `wpc_sensor`.`lowerSensor`,\
                                        `wpc_sensor`.`mac_id`\
                                        FROM `TankControl`.`wpc_sensor`; "
        self.db.executeData(retrieveSql)
        return self.db.returnCursor()



        # database = DBoperation()
broker = MqttBroker()
# database.dbConnection()
broker.mqttConnection()
broker.mqttLoopForever()
