-- MySQL dump 10.13  Distrib 9.1.0, for Win64 (x86_64)
--
-- Host: localhost    Database: user
-- ------------------------------------------------------
-- Server version 9.1.0
 
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
 
--
-- Table structure for table `alembic_version`
--
 
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
 
--
-- Dumping data for table `alembic_version`
--
 
LOCK TABLES `alembic_version` WRITE;
INSERT INTO `alembic_version` VALUES ('21a281c7ad3a');
UNLOCK TABLES;
 
--
-- Table structure for table `ingredient`
--
 
DROP TABLE IF EXISTS `ingredient`;
CREATE TABLE `ingredient` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=196 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
 
--
-- Dumping data for table `ingredient`
--
 
LOCK TABLES `ingredient` WRITE;
INSERT INTO `ingredient` VALUES 
(1, '牛肉', '肉'),
(2, '豚肉', '肉'),
(3, '鶏肉', '肉'),
(4, 'キャベツ', '野菜'),
(5, 'ニンジン', '野菜'),
(6, 'じゃがいも', '野菜'),
(7, 'トマト', '野菜'),
(8, '玉ねぎ', '野菜'),
(9, '大根', '野菜'),
(10, 'ほうれん草', '野菜');
UNLOCK TABLES;
 
--
-- Table structure for table `users`
--
 
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(150) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(255) NOT NULL,
  `age` int NOT NULL,
  `gender` varchar(3) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
 
--
-- Dumping data for table `users`
--
 
LOCK TABLES `users` WRITE;
INSERT INTO `users` VALUES 
(1, '田中太郎', 'taro@example.com', '$2b$12$T.MvSAZrCHkGFDomtTcTKukIID/jH6AVvRAS8j.bp3xaIbXYx4oUq', 20, 'M'),
(2, '山田花子', 'hanako@example.com', 'pbkdf2:sha256:1000000$AdXiPSzFPVO55mzG$0264c1214b4f8d814c8c50cc9d820ec68398135b53aa0d16e0f5ccc2e563b7fc', 20, 'F');
UNLOCK TABLES;
 
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
 
-- Dump completed on 2024-12-05 15:38:36