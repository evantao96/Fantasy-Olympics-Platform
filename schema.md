Player 
+-----------+--------------+------+-----+---------+----------------+
| Field     | Type         | Null | Key | Default | Extra          |
+-----------+--------------+------+-----+---------+----------------+
| id        | int          | NO   | PRI | NULL    | auto_increment |
| name      | varchar(255) | NO   |     | NULL    |                |
| team_name | varchar(255) | NO   |     | NULL    |                |
| ready     | tinyint(1)   | YES  |     | NULL    |                |
+-----------+--------------+------+-----+---------+----------------+

CREATE TABLE Player (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, team_name VARCHAR(255) NOT NULL, ready TINYINT(1)); 

Athlete
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| id         | int          | NO   | PRI | NULL    | auto_increment |
| name       | varchar(255) | NO   |     | NULL    |                |
| country_id | varchar(3)   | YES  |     | NULL    |                |
| bio        | varchar(255) | YES  |     | NULL    |                |
+------------+--------------+------+-----+---------+----------------+

CREATE TABLE Athlete (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, country_id VARCHAR(3), bio VARCHAR(255));

Event 
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | int          | NO   | PRI | NULL    | auto_increment |
| name  | varchar(255) | NO   |     | NULL    |                |
+-------+--------------+------+-----+---------+----------------+

CREATE TABLE Event (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL);

Athlete_Participates
+------------+------+------+-----+---------+-------+
| Field      | Type | Null | Key | Default | Extra |
+------------+------+------+-----+---------+-------+
| athlete_id | int  | NO   | PRI | NULL    |       |
| event_id   | int  | NO   | PRI | NULL    |       |
+------------+------+------+-----+---------+-------+

CREATE TABLE Athlete_Participates (athlete_id INT NOT NULL, event_id INT NOT NULL, PRIMARY KEY (athlete_id, event_id), FOREIGN KEY (athlete_id) REFERENCES Athlete(id), FOREIGN KEY (event_id) REFERENCES Event(id));

Country
+---------+--------------+------+-----+---------+----------------+
| Field   | Type         | Null | Key | Default | Extra          |
+---------+--------------+------+-----+---------+----------------+
| id      | int          | NO   | PRI | NULL    | auto_increment |
| name    | varchar(255) | NO   |     | NULL    |                |
| weather | varchar(255) | NO   |     | NULL    |                |
+---------+--------------+------+-----+---------+----------------+

CREATE TABLE Country (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, weather VARCHAR(255) NOT NULL);