-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 02, 2025 at 02:30 PM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_web_showroom`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `email`, `password`, `created_at`, `updated_at`) VALUES
(1, 'admin@mail.com', 'admin123', '2025-06-24 21:22:38', '2025-06-24 21:22:38');

-- --------------------------------------------------------

--
-- Table structure for table `articles`
--

CREATE TABLE `articles` (
  `id` int NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `published_date` date DEFAULT NULL,
  `content` text,
  `image` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `articles`
--

INSERT INTO `articles` (`id`, `title`, `published_date`, `content`, `image`, `created_at`, `updated_at`) VALUES
(1, 'CARA MERAWAT MOBIL TUA - update', '2025-07-01', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', NULL, '2025-07-01 23:46:10', '2025-07-01 23:50:42');

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `vehicle_id` int DEFAULT NULL,
  `booking_date` date DEFAULT NULL,
  `method` enum('buy','test_drive') NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `dealers`
--

CREATE TABLE `dealers` (
  `user_id` int NOT NULL,
  `dealer_name` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `dealers`
--

INSERT INTO `dealers` (`user_id`, `dealer_name`, `phone`, `address`, `created_at`, `updated_at`) VALUES
(2, 'Honda Kasih', '78564987', 'Paris', '2025-07-02 22:29:09', '2025-07-02 22:29:09'),
(8, 'Toyota Jaya', '98745632', 'Penarukan', '2025-07-02 22:07:37', '2025-07-02 22:07:37');

-- --------------------------------------------------------

--
-- Table structure for table `individuals`
--

CREATE TABLE `individuals` (
  `user_id` int NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `individuals`
--

INSERT INTO `individuals` (`user_id`, `phone`, `address`, `created_at`, `updated_at`) VALUES
(1, '12797553', 'Sambangan', '2025-07-02 22:30:22', '2025-07-02 22:30:22'),
(3, '3342980', 'Banjar Tegal', '2025-07-02 22:25:49', '2025-07-02 22:25:49'),
(7, '123456788', 'Banyuasri', '2025-07-02 22:04:25', '2025-07-02 22:04:25');

-- --------------------------------------------------------

--
-- Table structure for table `new_vehicles`
--

CREATE TABLE `new_vehicles` (
  `vehicle_id` int NOT NULL,
  `transmission` varchar(50) DEFAULT NULL,
  `seats` int DEFAULT NULL,
  `color` varchar(50) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `fuel_type` varchar(50) DEFAULT NULL,
  `stock` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `new_vehicles`
--

INSERT INTO `new_vehicles` (`vehicle_id`, `transmission`, `seats`, `color`, `year`, `location`, `fuel_type`, `stock`, `created_at`, `updated_at`) VALUES
(2, 'Manual', 5, 'Merah', 2021, 'Singaraja', 'Pertamax', 4, '2025-07-02 21:29:36', '2025-07-02 21:29:36');

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int NOT NULL,
  `receiver_id` int DEFAULT NULL,
  `booking_id` int DEFAULT NULL,
  `message` text,
  `is_read` tinyint(1) DEFAULT '0',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `used_vehicles`
--

CREATE TABLE `used_vehicles` (
  `vehicle_id` int NOT NULL,
  `transmission` varchar(50) DEFAULT NULL,
  `seats` int DEFAULT NULL,
  `color` varchar(50) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `fuel_type` varchar(50) DEFAULT NULL,
  `mileage` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `used_vehicles`
--

INSERT INTO `used_vehicles` (`vehicle_id`, `transmission`, `seats`, `color`, `year`, `location`, `fuel_type`, `mileage`, `created_at`, `updated_at`) VALUES
(1, 'Manual', 5, 'Putih', 2021, 'Singaraja', 'Pertamax', 75000, '2025-07-02 21:27:29', '2025-07-02 21:27:29'),
(4, 'Manual', 5, 'Putih', 2021, 'Singaraja', 'Pertamax', 75000, '2025-07-02 21:49:54', '2025-07-02 21:49:54');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `type` enum('dealer','individual') NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `type`, `created_at`, `updated_at`) VALUES
(1, 'John Doe', 'johndoe@mail.com', 'johndoe123', 'individual', '2025-06-24 20:47:51', '2025-06-24 20:47:51'),
(2, 'Honda Kasih', 'honda@mail.com', 'honda123', 'dealer', '2025-06-24 21:03:07', '2025-07-02 22:29:09'),
(3, 'Alexander', 'alex@mail.com', 'alex123', 'individual', '2025-07-01 22:55:24', '2025-07-01 22:59:20'),
(7, 'Ucup', 'ucup@mail.com', 'ucup123', 'individual', '2025-07-02 22:04:25', '2025-07-02 22:04:25'),
(8, 'Toyota Jaya', 'toyotajaya@mail.com', 'toyotajaya123', 'dealer', '2025-07-02 22:07:37', '2025-07-02 22:07:37');

-- --------------------------------------------------------

--
-- Table structure for table `vehicles`
--

CREATE TABLE `vehicles` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `description` text,
  `price` decimal(15,2) DEFAULT NULL,
  `brand` varchar(100) DEFAULT NULL,
  `type` enum('new','used') NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `vehicles`
--

INSERT INTO `vehicles` (`id`, `user_id`, `name`, `description`, `price`, `brand`, `type`, `image`, `created_at`, `updated_at`) VALUES
(1, 3, 'Jazz', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum', '197000000.00', 'Honda', 'used', NULL, '2025-07-02 21:27:29', '2025-07-02 21:27:29'),
(2, 2, 'Jazz', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum', '293000000.00', 'Honda', 'new', NULL, '2025-07-02 21:29:36', '2025-07-02 21:31:42'),
(4, 3, 'Avanza', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum', '197000000.00', 'Toyota', 'used', NULL, '2025-07-02 21:49:54', '2025-07-02 21:49:54');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `vehicle_id` (`vehicle_id`);

--
-- Indexes for table `dealers`
--
ALTER TABLE `dealers`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `individuals`
--
ALTER TABLE `individuals`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `new_vehicles`
--
ALTER TABLE `new_vehicles`
  ADD PRIMARY KEY (`vehicle_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `receiver_id` (`receiver_id`),
  ADD KEY `booking_id` (`booking_id`);

--
-- Indexes for table `used_vehicles`
--
ALTER TABLE `used_vehicles`
  ADD PRIMARY KEY (`vehicle_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `vehicles`
--
ALTER TABLE `vehicles`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`);

--
-- Constraints for table `dealers`
--
ALTER TABLE `dealers`
  ADD CONSTRAINT `dealers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `individuals`
--
ALTER TABLE `individuals`
  ADD CONSTRAINT `individuals_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `new_vehicles`
--
ALTER TABLE `new_vehicles`
  ADD CONSTRAINT `new_vehicles_ibfk_1` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`);

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `notifications_ibfk_2` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`id`);

--
-- Constraints for table `used_vehicles`
--
ALTER TABLE `used_vehicles`
  ADD CONSTRAINT `used_vehicles_ibfk_1` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`);

--
-- Constraints for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD CONSTRAINT `vehicles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
