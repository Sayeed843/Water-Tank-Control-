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

        except pymymql.Error as e:
            self.db.rollback()
            print(e)
            print("Execute Data into Database.......Failed")

    def getCursor(self):
        cursorList = []
        # print(str(self.cursor.fetchall()))
        for cur in self.cursor.fetchall():
            cursorList.append(cur[0])
        return cursorList

    def returnCursor(self):
        cursorList = []
        for cur in self.cursor.fetchall():
            cursorList.append(cur)
        return cursorList

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
        if (lowerSensor > 800):
            return True
        elif(upperSensor < 800 and lowerSensor < 800):
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
        return (self.db.getCursor())

    def retrieveMotorRealData(self, motorMac):
        sql = "SELECT `wpc_motor`.`waterSupply`\
                FROM `WaterPump`.`wpc_motor` JOIN `WaterPump`.`wpc_bdwaterboard`\
                ON `wpc_motor`.`mac_fk_id`=`wpc_bdwaterboard`.`id`\
                WHERE `wpc_bdwaterboard`.`mac`=%s;"
        args = (motorMac)
        self.db.dbConnection()
        self.db.executeData(sql, args)
        return (self.db.getCursor())

    def retrieveBdWaterBoard(self, motorMac):
        sql = "SELECT `wpc_bdwaterboard`.`gallon`,\
        `wpc_bdwaterboard`.`use`,\
        `wpc_bdwaterboard`.`remaining`\
        FROM `WaterPump`.`wpc_bdwaterboard`\
        WHERE `wpc_bdwaterboard`.`mac`=%s ;"
        args = (motorMac)
        self.db.dbConnection()
        self.db.executeData(sql, args)

        # print(str(self.db.getCursor()))
        return (self.db.returnCursor())

    def updateBdWaterBoard(self, remaining, use, motorMac):
        sql = "UPDATE `WaterPump`.`wpc_bdwaterboard`\
                    SET `use` = %s,\
                    `remaining` = %s\
                    WHERE `mac` = %s;"
        args = (use, remaining, motorMac)
        self.db.dbConnection()
        self.db.executeData(sql, args)

    def insertDailyStatusTable(self, motorAction, motorMac):
        dailyStatus = self.retrieveDailyStatusData(motorMac)
        if (((dailyStatus is not False) and (motorAction is not True)) or
                ((dailyStatus is not True) and (motorAction is not False))):
            sql = "INSERT INTO `WaterPump`.`wpc_dailystatus`\
                     (`motorStatus`,`time`,`mac_id_id`)\
                     VALUES(%s, CURRENT_TIMESTAMP,\
                     (SELECT `wpc_bdwaterboard`.`id`\
                     FROM `WaterPump`.`wpc_bdwaterboard` \
                     WHERE `wpc_bdwaterboard`.`mac` = %s))"
            if (motorAction is not False):
                motorValue = "True"
                print("Motor Action Go: " + str(motorAction))
            else:
                motorValue = "False"
                print("Motor Action Go: " + str(motorAction))
            args = (motorValue, motorMac)
            self.db.dbConnection()
            self.db.executeData(sql, args)

    def gallonCalculation(self, upperValue, lowerValue, motorMac):
        print("Enter the Gallon")
        upperSensor = int(upperValue)
        lowerSensor = int(lowerValue)
        dailyStatus = self.retrieveDailyStatusData(motorMac)
        motorAction = self.waterPumpSwitchControl(upperSensor, lowerSensor)
        gallon = self.retrieveBdWaterBoard(motorMac)

        print("Daily Status: " + str(dailyStatus))
        print("Motor Real Action: " + str(motorAction))

        if (dailyStatus is not False and motorAction is not True):
            # print("Gallon: " + str(gallon))
            for item in gallon:
                # print("Wait " + str(item))
                # print("Total: " + str(item[0]))
                remaining = int(item[0]) - 1000
                # print("Remaining: " + str(remaining))
                # print("Total: " + str(item[1]))
                use = int(item[1]) + 1000
                # print("Now: " + str(use))
            self.updateBdWaterBoard(remaining, use, motorMac)


class MqttBroker():
    wtc = WaterTankControl()
    db = DBoperation()

    def __init__(self, server="m12.cloudmqtt.com", port=13348,
                 username="wvxwjqte", password="EbeW6HIvrbuS"):
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
        # self.wtc.retrieveDailyStatusData(msg.topic)
        self.wtc.gallonCalculation(sensorValue[0], sensorValue[1], msg.topic)
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
