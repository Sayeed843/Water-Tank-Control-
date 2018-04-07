import paho.mqtt.client as mqtt
import sys
import pymysql as pymymql


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

    def getCursor(self):
        return (self.cursor.fetchall())

    def display(self):
        for element in self.cursor:
            print(element[0])


class WaterTankControl():
    db = DBoperation()

    def insertSensorTable(self, upperSensor, lowerSensor, motorMac):
        sql = "INSERT INTO `WaterPump`.`wpc_sensor`\
        (`upperSensor`,`lowerSensor`,`wpc_sensor`.`date`,`mac_id`) \
        VALUES(%s,%s ,CURRENT_TIMESTAMP,\
        (SELECT `wpc_bdwaterboard`.`id`\
        FROM `WaterPump`.`wpc_bdwaterboard` \
        WHERE `wpc_bdwaterboard`.`mac` = %s))"

        args = (upperSensor, lowerSensor, motorMac)
        self.db.dbConnection()
        self.db.executeData(sql, args)

        # Agent Function
    def waterPumpSwitchControl(self, upperValue, lowerValue):
        upperSensor = int(upperValue)
        lowerSensor = int(lowerValue)
        print("Upper Value: " + str(upperSensor))
        print("Lower Value: " + str(lowerSensor))
        if (lowerSensor > 800):
            print("Motor-True")
            return True
        elif(upperSensor < 800 and lowerSensor < 800):
            print("Motor-False")
            return False

    def retrieveDailyStatusData(self, motorMac):
        sql = "SELECT `wpc_dailystatus`.`motorStatus` \
        FROM `WaterPump`.`wpc_dailystatus` \
        JOIN `WaterPump`.`wpc_bdwaterboard` \
        ON `wpc_dailystatus`.`mac_id_id` = `wpc_bdwaterboard`.`id`\
 WHERE `wpc_bdwaterboard`.`mac`=%s ORDER BY\
 `wpc_dailystatus`.`time` DESC LIMIT 1;"
        args = (motorMac)
        self.db.dbConnection()
        self.db.executeData(sql, args)
        self.db.display()
        return (self.db.getCursor())

    def insertDailyStatusTable(self, motorAction, motorMac):
        dailyStatus = self.retrieveDailyStatusData(motorMac)
        print("Motor Action: " + str(motorAction))
        if (((dailyStatus is True) and (motorAction is not True)) or
                ((dailyStatus is not True) and (motorAction is True))):
            print("Enter the Condition")
            sql = "INSERT INTO `WaterPump`.`wpc_dailystatus`\
                     (`motorStatus`,`time`,`mac_id_id`)\
                     VALUES(%s, CURRENT_TIMESTAMP,\
                     (SELECT `wpc_bdwaterboard`.`id`\
                     FROM `WaterPump`.`wpc_bdwaterboard` \
                     WHERE `wpc_bdwaterboard`.`mac` = %s))"
            args = (motorAction, motorMac)
            self.db.dbConnection()
            self.db.executeData(sql, args)


class MqttBroker():
    wtc = WaterTankControl()
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
        self.wtc.insertSensorTable(sensorValue[0], sensorValue[1], msg.topic)
        self.wtc.retrieveDailyStatusData(msg.topic)
        self.wtc.insertDailyStatusTable(self.wtc.waterPumpSwitchControl(
            sensorValue[0], sensorValue[1]), msg.topic)

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
