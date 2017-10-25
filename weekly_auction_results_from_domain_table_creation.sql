CREATE TABLE IF NOT EXISTS `weekly_auction_results_from_domain` (
  `Id` bigint(20) NOT NULL,
  `retrieval_date` varchar(4000) DEFAULT NULL,
  `suburb` varchar(5000) DEFAULT NULL,
  `address` varchar(5000) DEFAULT NULL,
  `price` varchar(5000) DEFAULT NULL,
  `property_type` varchar(5000) DEFAULT NULL,
  `result` varchar(4000) DEFAULT NULL,
  `agent` varchar(4000) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=4162 DEFAULT CHARSET=latin1;