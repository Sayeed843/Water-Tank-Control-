-- MySQL dump 10.13  Distrib 5.7.21, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: WaterPump
-- ------------------------------------------------------
-- Server version	5.7.21-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2018-04-07 07:57:33.893104','1','Sayeed',1,'[{\"added\": {}}]',4,1),(2,'2018-04-07 07:59:34.124322','1','False',1,'[{\"added\": {}}]',2,1),(3,'2018-04-07 07:59:51.703566','1','Sayeed',1,'[{\"added\": {}}]',5,1),(4,'2018-04-07 08:00:19.550809','1','Sayeed',1,'[{\"added\": {}}]',1,1),(5,'2018-04-07 08:00:55.685402','1','Sayeed Bin Mozahid',1,'[{\"added\": {}}]',3,1),(6,'2018-04-07 08:01:26.127641','2','Masud',1,'[{\"added\": {}}]',4,1),(7,'2018-04-07 08:02:06.990682','3','Asad',1,'[{\"added\": {}}]',4,1),(8,'2018-04-07 08:03:08.362326','2','False',1,'[{\"added\": {}}]',2,1),(9,'2018-04-07 08:03:17.179871','3','False',1,'[{\"added\": {}}]',2,1),(10,'2018-04-07 08:03:59.427008','2','Masud',1,'[{\"added\": {}}]',5,1),(11,'2018-04-07 08:04:06.670879','3','Asad',1,'[{\"added\": {}}]',5,1),(12,'2018-04-07 08:07:14.146417','1','Sayeed Bin Mozahid',3,'',3,1),(13,'2018-04-07 08:07:32.770203','2','Sayeed Bin Mozahid',1,'[{\"added\": {}}]',3,1),(14,'2018-04-08 17:57:08.616868','1','Sayeed',2,'[{\"changed\": {\"fields\": [\"waterSupply\"]}}]',5,1),(15,'2018-04-09 05:23:35.953547','1','Sayeed',2,'[{\"changed\": {\"fields\": [\"waterSupply\"]}}]',5,1),(16,'2018-04-10 16:48:14.733215','1','Sayeed',2,'[{\"changed\": {\"fields\": [\"waterSupply\"]}}]',5,1),(17,'2018-04-10 17:23:39.447927','1','Sayeed',2,'[{\"changed\": {\"fields\": [\"waterSupply\"]}}]',5,1),(18,'2018-04-10 17:23:48.199144','1','Sayeed',2,'[{\"changed\": {\"fields\": [\"waterSupply\"]}}]',5,1),(19,'2018-04-10 17:46:06.900398','1','Sayeed',2,'[{\"changed\": {\"fields\": [\"waterSupply\"]}}]',5,1),(20,'2018-04-10 17:46:15.139674','1','Sayeed',2,'[{\"changed\": {\"fields\": [\"waterSupply\"]}}]',5,1),(21,'2018-04-10 18:00:53.000916','1','Sayeed',2,'[]',5,1),(22,'2018-04-11 03:43:00.639312','1','Sayeed',2,'[]',5,1),(23,'2018-04-11 04:00:34.273954','1','Sayeed',2,'[{\"changed\": {\"fields\": [\"use\", \"remaining\"]}}]',4,1),(24,'2018-04-11 04:19:01.266052','1','Sayeed',2,'[{\"changed\": {\"fields\": [\"waterSupply\"]}}]',5,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-11 16:05:43
