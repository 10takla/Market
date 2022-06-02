-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: localhost    Database: market
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `клиент`
--

DROP TABLE IF EXISTS клиент;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `клиент` (
  `id_клиента` int NOT NULL AUTO_INCREMENT,
  `Фамилия` varchar(45) DEFAULT NULL,
  `Имя` varchar(45) DEFAULT NULL,
  `номер_телефона` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_клиента`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `клиент`
--

INSERT INTO клиент (id_клиента, Фамилия, Имя, номер_телефона) VALUES (1,'Андреев','Андрей','8 (932) 409 4234');
INSERT INTO клиент (id_клиента, Фамилия, Имя, номер_телефона) VALUES (2,'Иванов','Иван','8 (932) 221 9382');
INSERT INTO клиент (id_клиента, Фамилия, Имя, номер_телефона) VALUES (3,'Алексеев','Алексей','8 (932) 569 8392');
INSERT INTO клиент (id_клиента, Фамилия, Имя, номер_телефона) VALUES (4,'Шамилев','Шамиль','8 (932) 429 3232');
INSERT INTO клиент (id_клиента, Фамилия, Имя, номер_телефона) VALUES (5,'Абакаров','Абакар','8 (932) 239 4544');
INSERT INTO клиент (id_клиента, Фамилия, Имя, номер_телефона) VALUES (6,'Денисов','Денис','8 (932) 329 6422');
INSERT INTO клиент (id_клиента, Фамилия, Имя, номер_телефона) VALUES (7,'Михаилов','Михаил','8 (952) 409 1534');

--
-- Table structure for table `поставка`
--

DROP TABLE IF EXISTS поставка;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `поставка` (
  `id_поставки` int NOT NULL AUTO_INCREMENT,
  `id_поставщика` int DEFAULT NULL,
  `дата_поставки` date DEFAULT NULL,
  `количество_поставки` int DEFAULT NULL,
  `стоимость_поставки` float DEFAULT NULL,
  PRIMARY KEY (`id_поставки`),
  KEY `поставщик_idx` (`id_поставщика`),
  CONSTRAINT `поставщик` FOREIGN KEY (`id_поставщика`) REFERENCES `поставщик` (`id_поставщика`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `поставка`
--

INSERT INTO поставка (id_поставки, id_поставщика, дата_поставки, количество_поставки, стоимость_поставки) VALUES (1,2,'2022-02-20',12,5000);
INSERT INTO поставка (id_поставки, id_поставщика, дата_поставки, количество_поставки, стоимость_поставки) VALUES (2,1,'2022-02-20',2,2500);
INSERT INTO поставка (id_поставки, id_поставщика, дата_поставки, количество_поставки, стоимость_поставки) VALUES (3,3,'2021-01-20',34,7600);
INSERT INTO поставка (id_поставки, id_поставщика, дата_поставки, количество_поставки, стоимость_поставки) VALUES (4,2,'2012-02-20',5,2000);

--
-- Table structure for table `поставщик`
--

DROP TABLE IF EXISTS поставщик;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `поставщик` (
  `id_поставщика` int NOT NULL AUTO_INCREMENT,
  `название_фирмы` varchar(45) DEFAULT NULL,
  `номер_телефона` varchar(45) DEFAULT NULL,
  `страна` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_поставщика`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `поставщик`
--

INSERT INTO поставщик (id_поставщика, название_фирмы, номер_телефона, страна) VALUES (1,'Биртранс','8 (123) 453 2343','Китай');
INSERT INTO поставщик (id_поставщика, название_фирмы, номер_телефона, страна) VALUES (2,'Егор Авто','8 (423) 553 2523','Германия');
INSERT INTO поставщик (id_поставщика, название_фирмы, номер_телефона, страна) VALUES (3,'Инжелтранс','8 (213) 123 8453','Китай');

--
-- Table structure for table `продажа`
--

DROP TABLE IF EXISTS продажа;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `продажа` (
  `id_продажи` int NOT NULL AUTO_INCREMENT,
  `id_товара` int DEFAULT NULL,
  `id_клиента` int DEFAULT NULL,
  `id_сотрудника` int DEFAULT NULL,
  `дата_продажи` date DEFAULT NULL,
  `количество` int DEFAULT NULL,
  `скидка` float DEFAULT NULL,
  `сумма` float DEFAULT NULL,
  PRIMARY KEY (`id_продажи`),
  KEY `товар_idx` (`id_товара`),
  KEY `клиент_idx` (`id_клиента`),
  KEY `сотрудник_idx` (`id_сотрудника`),
  CONSTRAINT `клиент` FOREIGN KEY (`id_клиента`) REFERENCES `клиент` (`id_клиента`),
  CONSTRAINT `сотрудник` FOREIGN KEY (`id_сотрудника`) REFERENCES `сотрудник` (`id_сотрудника`),
  CONSTRAINT `товар` FOREIGN KEY (`id_товара`) REFERENCES `товар` (`id_товара`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `продажа`
--

INSERT INTO продажа (id_продажи, id_товара, id_клиента, id_сотрудника, дата_продажи, количество, скидка, сумма) VALUES (1,2,1,2,'2012-04-20',2,10,12500);
INSERT INTO продажа (id_продажи, id_товара, id_клиента, id_сотрудника, дата_продажи, количество, скидка, сумма) VALUES (2,5,2,2,'2004-05-20',12,10,7500);
INSERT INTO продажа (id_продажи, id_товара, id_клиента, id_сотрудника, дата_продажи, количество, скидка, сумма) VALUES (3,1,3,1,'2004-05-20',1,15,2000);
INSERT INTO продажа (id_продажи, id_товара, id_клиента, id_сотрудника, дата_продажи, количество, скидка, сумма) VALUES (4,3,4,3,'2004-05-20',7,10,34000);
INSERT INTO продажа (id_продажи, id_товара, id_клиента, id_сотрудника, дата_продажи, количество, скидка, сумма) VALUES (5,2,5,2,'2004-05-20',5,30,24000);
INSERT INTO продажа (id_продажи, id_товара, id_клиента, id_сотрудника, дата_продажи, количество, скидка, сумма) VALUES (6,6,6,3,'2004-05-20',3,10,17000);
INSERT INTO продажа (id_продажи, id_товара, id_клиента, id_сотрудника, дата_продажи, количество, скидка, сумма) VALUES (7,3,7,2,'2004-05-20',1,10,2500);

--
-- Table structure for table `производитель`
--

DROP TABLE IF EXISTS производитель;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `производитель` (
  `id_производителя` int NOT NULL AUTO_INCREMENT,
  `фирма` varchar(45) DEFAULT NULL,
  `страна` varchar(45) DEFAULT NULL,
  `лицензия` varchar(45) DEFAULT NULL,
  `товарный_знак` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_производителя`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `производитель`
--

INSERT INTO производитель (id_производителя, фирма, страна, лицензия, товарный_знак) VALUES (1,'Samsung','Южная Корея',NULL,NULL);
INSERT INTO производитель (id_производителя, фирма, страна, лицензия, товарный_знак) VALUES (2,'Xiaomi','Китай',NULL,NULL);
INSERT INTO производитель (id_производителя, фирма, страна, лицензия, товарный_знак) VALUES (3,'Apple','США',NULL,NULL);
INSERT INTO производитель (id_производителя, фирма, страна, лицензия, товарный_знак) VALUES (4,'Acer','Тайвань',NULL,NULL);
INSERT INTO производитель (id_производителя, фирма, страна, лицензия, товарный_знак) VALUES (5,'ASUS','Тайвань',NULL,NULL);
INSERT INTO производитель (id_производителя, фирма, страна, лицензия, товарный_знак) VALUES (6,'LG','Южная Корея',NULL,NULL);

--
-- Table structure for table `сотрудник`
--

DROP TABLE IF EXISTS сотрудник;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `сотрудник` (
  `id_сотрудника` int NOT NULL AUTO_INCREMENT,
  `Фамилия` varchar(45) DEFAULT NULL,
  `Имя` varchar(45) DEFAULT NULL,
  `Должность` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_сотрудника`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `сотрудник`
--

INSERT INTO сотрудник (id_сотрудника, Фамилия, Имя, Должность) VALUES (1,'Артемов','Артем','Кассир');
INSERT INTO сотрудник (id_сотрудника, Фамилия, Имя, Должность) VALUES (2,'Афанасьев','Афанасий','Продавец-консультант');
INSERT INTO сотрудник (id_сотрудника, Фамилия, Имя, Должность) VALUES (3,'Ильясов','Ильяс','Кассир');

--
-- Table structure for table `товар`
--

DROP TABLE IF EXISTS товар;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `товар` (
  `id_товара` int NOT NULL AUTO_INCREMENT,
  `id_производителя` int DEFAULT NULL,
  `id_поставки` int DEFAULT NULL,
  `назвакние_товара` varchar(45) DEFAULT NULL,
  `категория` varchar(45) DEFAULT NULL,
  `дата_выпуска` date DEFAULT NULL,
  `в_наличии` int DEFAULT NULL,
  `гарантия` varchar(45) DEFAULT NULL,
  `цена` float DEFAULT NULL,
  PRIMARY KEY (`id_товара`),
  KEY `производитель_idx` (`id_производителя`),
  KEY `поставка_idx` (`id_поставки`),
  CONSTRAINT `поставка` FOREIGN KEY (`id_поставки`) REFERENCES `поставка` (`id_поставки`),
  CONSTRAINT `производитель` FOREIGN KEY (`id_производителя`) REFERENCES `производитель` (`id_производителя`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `товар`
--

INSERT INTO товар (id_товара, id_производителя, id_поставки, назвакние_товара, категория, дата_выпуска, в_наличии, гарантия, цена) VALUES (1,5,3,'Ноутбук ASUS Laptop E210MA-GJ001T','Ноутбуки','2001-02-20',14,'2',12000);
INSERT INTO товар (id_товара, id_производителя, id_поставки, назвакние_товара, категория, дата_выпуска, в_наличии, гарантия, цена) VALUES (2,3,NULL,'Смартфон Apple iPhone SE','Смартфоны','2002-02-20',0,'1',34000);
INSERT INTO товар (id_товара, id_производителя, id_поставки, назвакние_товара, категория, дата_выпуска, в_наличии, гарантия, цена) VALUES (3,1,2,'Смартфон Samsung Galaxy A12','Смартфоны','2003-02-20',10,'2',22000);
INSERT INTO товар (id_товара, id_производителя, id_поставки, назвакние_товара, категория, дата_выпуска, в_наличии, гарантия, цена) VALUES (4,4,NULL,'Ноутбук Acer Aspire 1 A114-33-C913','Ноутбуки','2004-02-20',27,'2',27000);
INSERT INTO товар (id_товара, id_производителя, id_поставки, назвакние_товара, категория, дата_выпуска, в_наличии, гарантия, цена) VALUES (5,6,4,'Телевизор LED LG 22TN410V-PZ','ТВ','2025-02-20',1,'0',2000);
INSERT INTO товар (id_товара, id_производителя, id_поставки, назвакние_товара, категория, дата_выпуска, в_наличии, гарантия, цена) VALUES (6,1,NULL,'Смартфон Samsung Galaxy A03','Смартфоны','2021-02-20',0,'1',14000);
INSERT INTO товар (id_товара, id_производителя, id_поставки, назвакние_товара, категория, дата_выпуска, в_наличии, гарантия, цена) VALUES (7,1,1,'Телевизор LED Samsung UE24N4500AUXRU','ТВ','2025-02-20',24,'2',34009);
INSERT INTO товар (id_товара, id_производителя, id_поставки, назвакние_товара, категория, дата_выпуска, в_наличии, гарантия, цена) VALUES (8,2,NULL,'Смартфон Xiaomi Redmi 9C NF','Смартфоны','2008-02-20',0,'3',18450);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed
