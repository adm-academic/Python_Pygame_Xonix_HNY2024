PRAGMA foreign_keys=on;

UPDATE sqlite_sequence SET seq =3 where name = "Player";
UPDATE sqlite_sequence SET seq = 16 where name = "Possible_Level";

DELETE FROM  Completed_Level;

DROP TABLE IF EXISTS Player;
CREATE table Player(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   name VARCHAR(500),
   score int,
   registration_date datetime
);
INSERT INTO Player (id,name,score,registration_date)
VALUES (1,'Just_a_Player',0,'2023-11-25 12:19:12');
INSERT INTO Player (id,name,score,registration_date)
VALUES (2,'adm-fil',0,'2023-11-25 15:12:22');
INSERT INTO Player (id,name,score,registration_date)
VALUES (3,'gamer',0,'2023-11-26 11:18:28');



DROP TABLE IF EXISTS Possible_Level;
CREATE table Possible_Level(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	enemies_count int,
	enemies_delay int, 
	backround_image VARCHAR(500)
);
INSERT INTO Possible_Level (id,enemies_count,enemies_delay,backround_image) 
VALUES (1,1,100,'dragon1.jpg');
INSERT INTO Possible_Level (id,enemies_count,enemies_delay,backround_image) 
VALUES (2,1,90,'dragon2.jpg');
INSERT INTO Possible_Level (id,enemies_count,enemies_delay,backround_image) 
VALUES (3,1,80,'dragon3.jpg');
INSERT INTO Possible_Level (id,enemies_count,enemies_delay,backround_image) 
VALUES (4,1,70,'dragon4.jpg');
INSERT INTO Possible_Level (id,enemies_count,enemies_delay,backround_image) 
VALUES (5,2,100,'dragon5.jpg');
INSERT INTO Possible_Level (id,enemies_count,enemies_delay,backround_image) 
VALUES (6,2,90,'dragon6.jpg');
INSERT INTO Possible_Level (id,enemies_count,enemies_delay,backround_image) 
VALUES (7,2,80,'dragon7.jpg');
INSERT INTO Possible_Level (id,enemies_count,enemies_delay,backround_image) 
VALUES (8,2,70,'dragon8.jpg');
INSERT INTO Possible_Level (id,enemies_count,enemies_delay,backround_image) 
VALUES (9,3,100,'dragon9.jpg');
INSERT INTO Possible_Level (id,enemies_count,enemies_delay,backround_image) 
VALUES (10,3,90,'dragon10.jpg');
INSERT INTO Possible_Level (id,enemies_count,enemies_delay,backround_image) 
VALUES (11,3,80,'dragon11.jpg');
INSERT INTO Possible_Level (id,enemies_count,enemies_delay,backround_image) 
VALUES (12,3,70,'dragon12.jpg');
INSERT INTO Possible_Level (id,enemies_count,enemies_delay,backround_image) 
VALUES (13,3,60,'dragon13.jpg');
INSERT INTO Possible_Level (id,enemies_count,enemies_delay,backround_image) 
VALUES (14,3,50,'dragon14.jpg');
INSERT INTO Possible_Level (id,enemies_count,enemies_delay,backround_image) 
VALUES (15,3,40,'dragon15.jpg');
INSERT INTO Possible_Level (id,enemies_count,enemies_delay,backround_image) 
VALUES (16,3,30,'dragon16.jpg');

DROP TABLE IF EXISTS Settings_Key_Value;
CREATE table Settings_Key_Value(
	key VARCHAR(500),
	value VARCHAR(500)
);
INSERT INTO Settings_Key_Value (key,value)
VALUES ('test1_key','test1_value');
INSERT INTO Settings_Key_Value (key,value)
VALUES ('player_last_name','Just_a_Player');
INSERT INTO Settings_Key_Value (key,value)
VALUES ('FPS','60');


DROP TABLE IF EXISTS Completed_Level;
CREATE table Completed_Level(
	player_id int not null,
	possible_level_id int not null,
	score int,
	pl_datetime datetime,
	FOREIGN KEY (player_id) REFERENCES Player(id),
	FOREIGN KEY (possible_level_id) REFERENCES Possible_Level(id)
);



