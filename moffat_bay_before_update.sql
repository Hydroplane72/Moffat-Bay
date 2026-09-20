-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: 127.0.0.1    Database: moffat_bay
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `contactmessages`
--

DROP TABLE IF EXISTS `contactmessages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contactmessages` (
  `message_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`message_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contactmessages`
--

LOCK TABLES `contactmessages` WRITE;
/*!40000 ALTER TABLE `contactmessages` DISABLE KEYS */;
INSERT INTO `contactmessages` VALUES (1,'Demo User','demo@moffatbay.com','Inquiry','I have a question about my reservation.','2026-09-13 12:11:26'),(2,'Alice Smith','alice@example.com','Feedback','Great service!','2026-09-13 12:11:26'),(3,'Bob Jones','bob@example.com','Issue','I encountered a problem with my booking.','2026-09-13 12:11:26');
/*!40000 ALTER TABLE `contactmessages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customers` (
  `customer_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Demo','User','demo@moffatbay.com','555-0101','07b2ec23ebecd12e9a6a1cbfec51f74ad4cdf9f42ac21d88eac9adc3795f41a6','2026-09-13 12:11:26','2026-09-13 12:11:26'),(2,'Alice','Smith','alice@example.com','555-0192','008c70392e3abfbd0fa47bbc2ed96aa99bd49e159727fcba0f2e6abeb3a9d601','2026-09-13 12:11:26','2026-09-13 12:11:26'),(3,'Bob','Jones','bob@example.com','555-0144','008c70392e3abfbd0fa47bbc2ed96aa99bd49e159727fcba0f2e6abeb3a9d601','2026-09-13 12:11:26','2026-09-13 12:11:26'),(4,'Maria','Garcia','maria@example.com','555-0117','008c70392e3abfbd0fa47bbc2ed96aa99bd49e159727fcba0f2e6abeb3a9d601','2026-09-13 12:11:26','2026-09-13 12:11:26'),(5,'Lucia','Collins','lucia@example.com','555-0139','008c70392e3abfbd0fa47bbc2ed96aa99bd49e159727fcba0f2e6abeb3a9d601','2026-09-13 12:11:26','2026-09-13 12:11:26'),(6,'Tiffany','Davidson','tiffanylaurine@gmail.com','4793407740','3d14e8c38eee66eabac451301260b99f357a019b624b474ce78a5fd25dd43b00','2026-09-19 22:10:09','2026-09-19 22:10:09'),(7,'Tiffany','Davidson','tiffanylaurine1@gmail.com','4793407740','fba2aa2c8ba4373369eb64df1bd4f8c3df947a66d67812d114113954f712936f','2026-09-19 22:24:30','2026-09-19 22:24:30');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservationrooms`
--

DROP TABLE IF EXISTS `reservationrooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reservationrooms` (
  `reservation_room_id` int(11) NOT NULL AUTO_INCREMENT,
  `reservation_id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `nightly_rate` decimal(10,2) NOT NULL CHECK (`nightly_rate` >= 0),
  PRIMARY KEY (`reservation_room_id`),
  KEY `reservation_id` (`reservation_id`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `reservationrooms_ibfk_1` FOREIGN KEY (`reservation_id`) REFERENCES `reservations` (`reservation_id`) ON DELETE CASCADE,
  CONSTRAINT `reservationrooms_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`room_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservationrooms`
--

LOCK TABLES `reservationrooms` WRITE;
/*!40000 ALTER TABLE `reservationrooms` DISABLE KEYS */;
INSERT INTO `reservationrooms` VALUES (1,1,1,126.00),(2,2,6,141.75),(3,3,11,157.50),(4,4,16,168.00),(5,5,16,168.00),(6,6,6,141.75),(7,7,6,141.75),(8,8,16,168.00),(9,9,11,157.50),(10,9,12,157.50);
/*!40000 ALTER TABLE `reservationrooms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservations`
--

DROP TABLE IF EXISTS `reservations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reservations` (
  `reservation_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  `num_guests` int(11) NOT NULL CHECK (`num_guests` > 0),
  `check_in_date` date NOT NULL,
  `check_out_date` date NOT NULL,
  `total_price` decimal(10,2) NOT NULL CHECK (`total_price` >= 0),
  `reservation_status` varchar(20) NOT NULL DEFAULT 'confirmed',
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`reservation_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`) ON DELETE CASCADE,
  CONSTRAINT `CONSTRAINT_1` CHECK (`check_out_date` > `check_in_date`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservations`
--

LOCK TABLES `reservations` WRITE;
/*!40000 ALTER TABLE `reservations` DISABLE KEYS */;
INSERT INTO `reservations` VALUES (1,1,2,'2026-09-10','2026-09-13',360.00,'confirmed','2026-09-13 12:11:26','2026-09-13 12:11:26'),(2,2,2,'2026-09-15','2026-09-18',405.00,'confirmed','2026-09-13 12:11:26','2026-09-13 12:11:26'),(3,3,4,'2026-09-20','2026-09-23',600.00,'pending','2026-09-13 12:11:26','2026-09-13 12:11:26'),(4,5,2,'2026-09-25','2026-09-28',270.00,'confirmed','2026-09-13 12:11:26','2026-09-13 12:11:26'),(5,1,2,'2027-01-10','2027-01-12',336.00,'confirmed','2026-09-13 12:14:48','2026-09-13 12:14:48'),(6,1,2,'2027-04-01','2027-04-03',283.50,'confirmed','2026-09-13 12:48:16','2026-09-13 12:48:16'),(7,1,2,'2027-03-01','2027-03-03',283.50,'confirmed','2026-09-13 12:51:50','2026-09-13 12:51:50'),(8,6,2,'2027-03-01','2027-03-08',1176.00,'confirmed','2026-09-19 22:10:54','2026-09-19 22:10:54'),(9,6,3,'2027-04-01','2027-04-05',1260.00,'confirmed','2026-09-19 22:15:58','2026-09-19 22:15:58');
/*!40000 ALTER TABLE `reservations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `room_availability_base`
--

DROP TABLE IF EXISTS `room_availability_base`;
/*!50001 DROP VIEW IF EXISTS `room_availability_base`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `room_availability_base` AS SELECT
 1 AS `room_id`,
  1 AS `room_number`,
  1 AS `room_type_name`,
  1 AS `allow_reservations`,
  1 AS `reservation_id`,
  1 AS `check_in_date`,
  1 AS `check_out_date`,
  1 AS `reservation_status` */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `rooms`
--

DROP TABLE IF EXISTS `rooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rooms` (
  `room_id` int(11) NOT NULL AUTO_INCREMENT,
  `room_type_id` int(11) NOT NULL,
  `room_number` varchar(20) NOT NULL,
  `allow_reservations` bit(1) NOT NULL DEFAULT b'1',
  PRIMARY KEY (`room_id`),
  UNIQUE KEY `room_number` (`room_number`),
  KEY `room_type_id` (`room_type_id`),
  CONSTRAINT `rooms_ibfk_1` FOREIGN KEY (`room_type_id`) REFERENCES `roomtypes` (`room_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rooms`
--

LOCK TABLES `rooms` WRITE;
/*!40000 ALTER TABLE `rooms` DISABLE KEYS */;
INSERT INTO `rooms` VALUES (1,1,'101','\0'),(2,1,'102',''),(3,1,'103',''),(4,1,'104',''),(5,1,'105',''),(6,2,'201',''),(7,2,'202',''),(8,2,'203',''),(9,2,'204',''),(10,2,'205',''),(11,3,'301',''),(12,3,'302',''),(13,3,'303',''),(14,3,'304',''),(15,3,'305',''),(16,4,'401',''),(17,4,'402',''),(18,4,'403',''),(19,4,'404',''),(20,4,'405','');
/*!40000 ALTER TABLE `rooms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roomtypes`
--

DROP TABLE IF EXISTS `roomtypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roomtypes` (
  `room_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `room_type_name` varchar(50) NOT NULL,
  `price_per_night` decimal(10,2) NOT NULL CHECK (`price_per_night` > 0),
  `max_occupancy` int(11) NOT NULL CHECK (`max_occupancy` > 0),
  PRIMARY KEY (`room_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roomtypes`
--

LOCK TABLES `roomtypes` WRITE;
/*!40000 ALTER TABLE `roomtypes` DISABLE KEYS */;
INSERT INTO `roomtypes` VALUES (1,'Double Full Beds',126.00,2),(2,'Queen',141.75,2),(3,'Double Queen Beds',157.50,4),(4,'King',168.00,2);
/*!40000 ALTER TABLE `roomtypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `room_availability_base`
--

/*!50001 DROP VIEW IF EXISTS `room_availability_base`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = cp850 */;
/*!50001 SET character_set_results     = cp850 */;
/*!50001 SET collation_connection      = cp850_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `room_availability_base` AS select `r`.`room_id` AS `room_id`,`r`.`room_number` AS `room_number`,`rt`.`room_type_name` AS `room_type_name`,`r`.`allow_reservations` AS `allow_reservations`,`res`.`reservation_id` AS `reservation_id`,`res`.`check_in_date` AS `check_in_date`,`res`.`check_out_date` AS `check_out_date`,`res`.`reservation_status` AS `reservation_status` from (((`rooms` `r` left join `roomtypes` `rt` on(`r`.`room_type_id` = `rt`.`room_type_id`)) left join `reservationrooms` `rr` on(`r`.`room_id` = `rr`.`room_id`)) left join `reservations` `res` on(`rr`.`reservation_id` = `res`.`reservation_id`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-19 22:30:30
