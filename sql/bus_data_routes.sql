-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: bus_data
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `routes`
--

DROP TABLE IF EXISTS `routes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `routes` (
  `route_id` text,
  `description` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `routes`
--

LOCK TABLES `routes` WRITE;
/*!40000 ALTER TABLE `routes` DISABLE KEYS */;
INSERT INTO `routes` VALUES ('rt_0000','No route description available'),('rt_0001','No route description available'),('rt_0002','No route description available'),('rt_0003','No route description available'),('rt_0004','No route description available'),('rt_0005','No route description available'),('rt_0006','No route description available'),('rt_0007','No route description available'),('rt_0008','No route description available'),('rt_0009','No route description available'),('rt_00010','No route description available'),('rt_00011','No route description available'),('rt_00012','No route description available'),('rt_00013','No route description available'),('rt_00014','No route description available'),('rt_00015','No route description available'),('rt_00016','No route description available'),('rt_00017','No route description available'),('rt_00018','No route description available'),('rt_00019','No route description available'),('rt_00020','No route description available'),('rt_00021','No route description available'),('rt_00022','No route description available'),('rt_00023','No route description available'),('rt_00024','No route description available'),('rt_00025','No route description available'),('rt_00026','No route description available'),('rt_00027','No route description available'),('rt_00028','No route description available'),('rt_00029','No route description available'),('R_21-404-_-y05-6-I-1','Westway Caterham - Crawford Crescent'),('R_21-404-_-y05-6-O-2','Crawford Crescent - Westway Caterham'),('R_21-404-_-y05-7-I-1','Westway Caterham - Crawford Crescent'),('R_21-404-_-y05-7-O-2','Crawford Crescent - Westway Caterham'),('R_21-404-_-y05-8-I-1','Westway Caterham - Crawford Crescent'),('R_21-404-_-y05-8-O-2','Crawford Crescent - Westway Caterham'),('R_21-407-_-y05-11-I-1','Caterham Valley - Sutton / Marshalls Road'),('R_21-407-_-y05-11-O-2','Sutton / Marshalls Road - Caterham Valley'),('R_21-407-_-y05-14-I-1','Caterham Valley - Sutton / Marshalls Road'),('R_21-407-_-y05-14-O-2','Sutton / Marshalls Road - Caterham Valley'),('R_21-464-_-y05-55538-I-1','New Addington Tram Stop - Biggin Hill / Black Horse'),('R_21-464-_-y05-55538-I-2','New Addington Tram Stop - Tatsfield Village / Old Ship'),('R_21-464-_-y05-55538-O-3','Tatsfield Village / Old Ship - New Addington Tram Stop'),('R_21-464-_-y05-55539-I-1','New Addington Tram Stop - Biggin Hill / Black Horse'),('R_21-464-_-y05-55539-I-2','New Addington Tram Stop - Tatsfield Village / Old Ship'),('R_21-464-_-y05-55539-O-3','Tatsfield Village / Old Ship - New Addington Tram Stop'),('R_21-464-_-y05-55541-I-1','New Addington Tram Stop - Biggin Hill / Black Horse'),('R_21-464-_-y05-55541-I-2','New Addington Tram Stop - Tatsfield Village / Old Ship'),('R_21-464-_-y05-55541-O-3','Biggin Hill / Black Horse - New Addington Tram Stop'),('R_21-464-_-y05-55541-O-4','Tatsfield Village / Old Ship - New Addington Tram Stop'),('R_21-465-_-y05-7-I-1','Townfield Court - Cromwell Road Bus Station'),('R_21-465-_-y05-7-I-2','Townfield Court - Cromwell Road Bus Station'),('R_21-465-_-y05-7-O-3','Cromwell Road Bus Station - South Street/ Rose Hill'),('R_21-R68-_-y05-58885-I-1','Hampton Court - Kew Retail Park'),('R_21-R68-_-y05-58885-O-2','Kew Retail Park - Hampton Court'),('R_21-S1-_-y05-59996-I-1','Victoria Road / Lavender Fields - Banstead / Marks & Spencer'),('R_21-S1-_-y05-59996-O-2','Banstead / Marks & Spencer - Victoria Road / Lavender Fields');
/*!40000 ALTER TABLE `routes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-02 22:12:45
