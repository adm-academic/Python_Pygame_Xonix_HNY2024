PRAGMA foreign_keys=on;

CREATE table if not exists Player(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   name VARCHAR(500),
   score int,
   registration_date datetime
);


CREATE table if not exists  Possible_Level(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	enemies_count int,
	enemies_speed int, 
	backround_image VARCHAR(500)
);



CREATE table if not exists Completed_Levels(
	player_id int not null,
	possible_level_id int not null,
	score int,
	pl_datetime datetime,
	FOREIGN KEY (player_id) REFERENCES Player(id),
	FOREIGN KEY (possible_level_id) REFERENCES Possible_Level(id)
);




CREATE table if not exists Settings_Key_Value(
	key VARCHAR(500),
	value VARCHAR(500)
);