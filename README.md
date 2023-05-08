# How to run the Flood_Alarm 

After executing "sensor_db.py", "flood_alarm.py" must be executed simultaneously. 
"socket_connection.py" is executed in Raspberry Pi when connecting using 'Simple TCP Socket Tester' Application.

# Table DB create command
Create Table: CREATE TABLE `mysql` (
  `sensor` varchar(50) DEFAULT NULL,
  `daytime` varchar(50) NOT NULL,
  `value` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
