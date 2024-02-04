CREATE TABLE Player (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, team_name VARCHAR(255) NOT NULL, ready TINYINT(1)); 
+-----------+--------------+------+-----+---------+----------------+
| Field     | Type         | Null | Key | Default | Extra          |
+-----------+--------------+------+-----+---------+----------------+
| id        | int          | NO   | PRI | NULL    | auto_increment |
| name      | varchar(255) | NO   |     | NULL    |                |
| team_name | varchar(255) | NO   |     | NULL    |                |
| ready     | tinyint(1)   | YES  |     | NULL    |                |
+-----------+--------------+------+-----+---------+----------------+

CREATE TABLE Athlete (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, country_id VARCHAR(3), bio VARCHAR(255));
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| id         | int          | NO   | PRI | NULL    | auto_increment |
| name       | varchar(255) | NO   |     | NULL    |                |
| country_id | varchar(3)   | YES  |     | NULL    |                |
| bio        | varchar(255) | YES  |     | NULL    |                |
+------------+--------------+------+-----+---------+----------------+

CREATE TABLE Event (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL);
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | int          | NO   | PRI | NULL    | auto_increment |
| name  | varchar(255) | NO   |     | NULL    |                |
+-------+--------------+------+-----+---------+----------------+

CREATE TABLE Athlete_Participates (athlete_id INT NOT NULL, event_id INT NOT NULL, medal INT NOT NULL, PRIMARY KEY (athlete_id, event_id), FOREIGN KEY (athlete_id) REFERENCES Athlete(id), FOREIGN KEY (event_id) REFERENCES Event(id));
+------------+------+------+-----+---------+-------+
| Field      | Type | Null | Key | Default | Extra |
+------------+------+------+-----+---------+-------+
| athlete_id | int  | NO   | PRI | NULL    |       |
| event_id   | int  | NO   | PRI | NULL    |       |
| medal      | int  | NO   |     | NULL    |       |
+------------+------+------+-----+---------+-------+

CREATE TABLE Country (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, climate VARCHAR(4) NOT NULL);
+---------+--------------+------+-----+---------+----------------+
| Field   | Type         | Null | Key | Default | Extra          |
+---------+--------------+------+-----+---------+----------------+
| id      | int          | NO   | PRI | NULL    | auto_increment |
| name    | varchar(255) | NO   |     | NULL    |                |
| climate | varchar(4)   | NO   |     | NULL    |                |
+---------+--------------+------+-----+---------+----------------+

CREATE Table Weather (id INT AUTO_INCREMENT PRIMARY KEY, city VARCHAR(255) NOT NULL, country VARCHAR(255) NOT NULL, month INT NOT NULL, year INT NOT NULL, temp INT NOT NULL, humidity INT NOT NULL); 
+----------+--------------+------+-----+---------+----------------+
| Field    | Type         | Null | Key | Default | Extra          |
+----------+--------------+------+-----+---------+----------------+
| id       | int          | NO   | PRI | NULL    | auto_increment |
| city     | varchar(255) | NO   |     | NULL    |                |
| country  | varchar(255) | NO   |     | NULL    |                |
| month    | int          | NO   |     | NULL    |                |
| year     | int          | NO   |     | NULL    |                |
| temp     | int          | NO   |     | NULL    |                |
| humidity | int          | NO   |     | NULL    |                |
+----------+--------------+------+-----+---------+----------------+

CREATE TABLE Player_Drafts_Athlete (athlete_id INT NOT NULL, event_id INT NOT NULL, player_id INT NOT NULL, PRIMARY KEY (athlete_id, event_id, player_id), FOREIGN KEY (athlete_id) REFERENCES Athlete(id), FOREIGN KEY (event_id) REFERENCES Event(id), FOREIGN KEY (player_id) REFERENCES Player(id));
+------------+------+------+-----+---------+-------+
| Field      | Type | Null | Key | Default | Extra |
+------------+------+------+-----+---------+-------+
| athlete_id | int  | NO   | PRI | NULL    |       |
| event_id   | int  | NO   | PRI | NULL    |       |
| player_id  | int  | NO   | PRI | NULL    |       |
+------------+------+------+-----+---------+-------+