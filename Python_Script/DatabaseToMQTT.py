import paho.mqtt.client as mqtt
import sys
import pymysql as pymymql
from time import sleep


class DBoperation():

    def __init__(self, user='root', password='1', host='127.0.0.1',
                 port=3306, dbName='WaterPump'):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dbName = dbName

    def dbConnection(self):
        try:
            self.db = pymymql.connect(user=self.user, password=self.password,
                                      host=self.host, port=self.port, db=self.dbName)
            # print("Database Connection")
        except pymymql.Error as e:
            print(e)
            print("Could Not connect to the database")
            print("Close...")
            sys.exit()
        self.cursor = self.db.cursor()

    def executeData(self, sql, args=None):
        try:
            self.cursor.execute(sql, args)
            self.db.commit()
            # print("Execute Data into Database.......OK")
        except pymymql.Error as e:
            self.db.rollback()
            print(e)
            print("Execute Data into Database.......Failed")

    def getCursor(self):
        cursorList = []
        for cur in self.cursor:
            cursorList.append(cur[0])
        return cursorList

    def display(self):
        for element in self.cursor:
            print(element)


class WaterTankControl():

    db = DBoperation()

    def retrieveMotorMac(self):
        sql = "SELECT `wpc_bdwaterboard`.`mac`\
        FROM `WaterPump`.`wpc_bdwaterboard`;"

        self.db.dbConnection()
        self.db.executeData(sql)
        # self.db.display()
        return (self.db.getCursor())

    def retrieveDailyStatusData(self):
        dailyStatusDictionary = {}
        for mac in self.retrieveMotorMac():
            print("Mac: " + mac)
            sql = "SELECT `wpc_dailystatus`.`motorStatus` \
            FROM `WaterPump`.`wpc_dailystatus` \
            JOIN `WaterPump`.`wpc_bdwaterboard` \
            ON `wpc_dailystatus`.`mac_id_id` = `wpc_bdwaterboard`.`id`\
            WHERE `wpc_bdwaterboard`.`mac` = %s\
            ORDER BY`wpc_dailystatus`.`time` DESC LIMIT 1;"
            args = (mac)
            self.db.dbConnection()
            self.db.executeData(sql, args)
            dailyStatusDictionary[str(mac)] = self.db.getCursor()
            # self.db.display()
            # return (self.db.getCursor())
        return (dailyStatusDictionary)

    def retrieveBoardDecision(self, motorMac):
        sql = "SELECT `wpc_motor`.`waterSupply`\
        FROM `WaterPump`.`wpc_motor` JOIN `WaterPump`.`wpc_bdwaterboard`\
        ON `wpc_motor`.`mac_fk_id`=`wpc_bdwaterboard`.`id`\
        WHERE `wpc_bdwaterboard`.`mac`=%s;"

        args = (motorMac)
        self.db.dbConnection()
        self.db.executeData(sql, args)
        return(self.db.getCursor())


class MqttBroker():
    db = DBoperation()
    wtc = WaterTankControl()

    def __init__(self, server="m13.cloudmqtt.com", port=16144,
                 username="tuzdocic", password="Eg9MQUEajoeR"):
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

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def mqttLoopForever(self):
        self.client.on_connect = self.on_connect
        data = self.wtc.retrieveDailyStatusData()

        for d in data:
            # print("MAC: " + str(d) + "Result: " + str(self.wtc.retrieveBoardDecision(str(d))))
            decision = self.wtc.retrieveBoardDecision(str(d))
            # print(type(decision[0]))
            # print("Result: " + str(decision))
            print("Mac" + str(d) + "Ami Aci" + str(decision))
            self.client.publish(str(d), str(decision[0]))
            # if (decision[0] == 1):
            #     print("Ami Aci" + str(decision))
            #     self.client.publish(str(d), str(decision[0]))
            sleep(0.5)
            self.mqttLoopForever()
        # print(data)
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
