--DON'T ADD VALUES WHERE PRIMARY KEY IS AUTO-INCREMENTED LIKE GIVE BELOW 
/*
CREATE  TABLE Team_Attack(
    Attack_id INT PRIMARY KEY AUTO_INCREMENT,
    match_id INT,
    team_id INT NOT NULL,
    points INT NOT NULL,
    inning INT CHECK(inning IN (1,2)),
    phase VARCHAR(10) CHECK(phase IN ('Early','Mid','End')),
    FOREIGN KEY (match_id) REFERENCES Match_details(match_id),
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
);

INSERT INTO Team_Attack (match_id, team_id, points, inning, phase)
VALUES
-- Inning 1
(1, 1, 3, 1, 'Early'),
(1, 2, 1, 1, 'Early'),
(1, 1, 4, 1, 'Mid'),
(1, 2, 3, 1, 'Mid'),

-- Inning 2
(1, 1, 2, 2, 'Early'),
(1, 2, 2, 2, 'Early'),
(1, 1, 3, 2, 'Mid'),
(1, 2, 5, 2, 'Mid');
*/

CREATE TABLE Player (
    player_id INT PRIMARY KEY AUTO_INCREMENT,
    team_id INT NOT NULL,
    player_name VARCHAR(50) NOT NULL,
    player_age INT CHECK (player_age > 0),
    role VARCHAR(20),
        CHECK (role IN ('Attacker','Defender','All-Rounder','Unknown')),

    jersey_no INT NOT NULL,
    
    CONSTRAINT chk_jersey_range 
        CHECK (jersey_no BETWEEN 1 AND 15),

    CONSTRAINT unique_team_jersey 
        UNIQUE (team_id, jersey_no),

    FOREIGN KEY (team_id) 
        REFERENCES Team(team_id)
);

INSERT INTO Player (player_id, team_id, player_name, player_age, role,jersey_no)
VALUES 
(1, 1, 'aayush yadav', 22, 'Defender',1),
(2, 1, 'dhaygude atharva', 16, 'All-Rounder',2),
(3, 1, 'varad pol', 14, 'Attacker',3),
(4, 1, 'vaibhav jadhav', 16, 'Attacker',4),
(5, 1, 'aayush panghare', 21, 'All-Rounder',5),
(6, 1, 'swaraj ghadhave', 15, 'Attacker',6),
(7, 1, 'pratik aadhav', 14, 'Defender',7),
(8, 1, 'raj pawar', 16, 'Attacker',8),
(9, 1, 'swaraj uttekar', 16, 'All-Rounder',9),
(10, 1, 'mayureshwar gosavi', 14, 'Defender',10),
(11, 1, 'vighnesh girme', 16, 'Attacker',11),
(12, 1, 'soham hipparkar', 16, 'All-Rounder',12),
(13, 1, 'soham bhamare', 15, 'Attacker',13),
(14, 1, 'Tej Shinde', 14, 'Attacker',14),
(15, 1, 'Sarthak Mahadik', 15, 'All-Rounder',15),
(16, 2, 'kartavya gandekr', 14, 'Defender',1),
(17, 2, 'soham deshmukh', 16, 'Attacker',2),
(18, 2, 'atul parde', 16, 'All-Rounder',3),
(19, 2, 'shreeyash maharugade', 15, 'Attacker',4),
(20, 2, 'om wagh', 14, 'Defender',5),
(21, 2, 'sangam thakur', 14, 'Attacker',6),
(22, 2, 'krushna mahanvar', 16, 'All-Rounder',7),
(23, 2, 'pranav mane', 15, 'Defender',8),
(24, 2, 'shreeraj tangade', 14, 'Defender',9),
(25, 2, 'satyam sakat', 16, 'Attacker',10),
(26, 2, 'tanmay nigudkar', 16, 'All-Rounder',11),
(27, 2, 'umesh dongare', 15, 'Attacker',12),
(28, 2, 'pallav sarade', 14, 'Defender',13),
(29, 2, 'arjun gorade', 16, 'Attacker',14),
(30, 2, 'vedant gaikwad', 16, 'All-Rounder',15);

CREATE TABLE Team(
    team_id INT PRIMARY KEY AUTO_INCREMENT,
    team_name VARCHAR(50) NOT NULL UNIQUE,
    No_of_attackers INT CHECK (No_of_attackers >= 0),
    No_of_defenders INT CHECK (No_of_defenders >= 0),
    No_of_all_arounders INT CHECK (No_of_all_arounders >= 0),
    City_name VARCHAR(50),
    Coach_name VARCHAR(30)
);

INSERT INTO TEAM (team_id, team_name, No_of_attackers, No_of_defenders, No_of_all_arounders, City_name, Coach_name)
VALUES 
(1, 'Satara Warriors', 5, 6, 4, 'satara', 'Coach gaikwad'),
(2, 'Pune Champions', 4, 6, 4, 'pune', 'Coach jagdale'),
(3, 'Solapur Royals', 7, 4, 4, 'solapur', 'Coach waghmare'),
(4, 'Dharashiv Marshals', 5, 5, 5, 'dharashiv', 'Coach valunj'),
(5, 'Chennai Guns', 4, 4, 7, 'chennai', 'Coach shinde'),
(6, 'Mumbai Khiladi', 3, 6, 6, 'mumbai', 'Coach pawar'),
(7, 'Delhi Deredevils', 2, 7, 6, 'delhi', 'Coach yadav'),
(8, 'Hyderabad Spartans', 4, 5, 6, 'hyderabad', 'Coach kalyankar');

CREATE TABLE Match_details(
    match_id INT PRIMARY KEY,
	match_name VARCHAR(20),
    tournament_id INT,
    venue VARCHAR(30) NOT NULL,
    home_team INT NOT NULL,
    away_team INT NOT NULL,
    match_date DATE NOT NULL,
    winning_team INT,
	home_team_score INT, --updated
	away_team_score INT, --updated
    result VARCHAR(40), --updated
	UNIQUE (tournament_id, match_name),
    FOREIGN KEY(home_team) REFERENCES Team(team_id),
    FOREIGN KEY(away_team) REFERENCES Team(team_id),
    FOREIGN KEY(winning_team) REFERENCES Team(team_id),
    FOREIGN KEY(tournament_id) REFERENCES Tournament(tournament_id) 
);

INSERT INTO Match_details (match_id, match_name, tournament_id,venue, home_team, away_team, match_date, winning_team, home_team_score, away_team_score, result)
VALUES 
(1, "M01", 1, 'Pune', 1, 2, '2026-01-10', 1, 18, 15, NULL),
(2, "M02", 1, 'Mumbai', 3, 4, '2026-01-12', 4, 20, 25, NULL),
(3, "M03", 1, 'Nashik', 5, 6, '2026-01-15', NULL, 15, 15, NULL),
(4, "M04", 1, 'Nagpur', 7, 8, '2026-01-18', 8, 10, 35, NULL),
(5, "M05", 1,' Kolhapur', 2, 3, '2026-01-20', 2, 28, 15, NULL);


CREATE TABLE Player_match_stat(
    stat_id INT PRIMARY KEY AUTO_INCREMENT,
	player_id INT,
	match_id INT,
	attack_points INT,
	defense_points INT,
	pole_dives INT,
	sky_dives INT,
	touches INT,
	tournament_id INT,
    FOREIGN KEY(player_id) REFERENCES Player(player_id),
    FOREIGN KEY(match_id) REFERENCES Match_details(match_id),
	FOREIGN KEY(tournament_id) REFERENCES Tournament(tournament_id)
);

INSERT INTO Player_match_stat (stat_id, player_id, match_id, attack_points, defense_points, pole_dives, sky_dives, touches)
VALUES 
(1, 1, 1, 0, 60, 0, 0, 0),
(2, 2, 1, 0, 0, 0, 0, 0),
(3, 3, 1, 2, 60, 0, 0, 0),
(4, 4, 1, 8, 150, 1, 0, 0),
(5, 5, 1, 0, 60, 0, 0, 0),
(6, 6, 1, 2, 180, 0, 0, 0),
(7, 7, 1, 0, 120, 1, 0, 0),
(8, 8, 1, 0, 40, 0, 0, 0),
(9, 9, 1, 2, 80, 0, 0, 0),
(10, 10, 1, 4, 90, 0, 0, 0),
(11, 11, 1, 2, 0, 0, 0, 0),
(12, 12, 1, 0, 0, 0, 0, 0),
(13, 13, 1, 0, 0, 0, 0, 0),
(14, 14, 1, 0, 0, 0, 0, 0),
(15, 15, 1, 0, 0, 0, 0, 0),
(16, 16, 1, 4, 260, 0, 0, 0),
(17, 17, 1, 6, 135, 1, 0, 0),
(18, 18, 1, 0, 0, 0, 0, 0),
(19, 19, 1, 0, 100, 0, 0, 0),
(20, 20, 1, 0, 60, 0, 0, 0),
(21, 21, 1, 0, 0, 0, 0, 0),
(22, 22, 1, 0, 10, 0, 0, 0),
(23, 23, 1, 2, 60, 0, 0, 0),
(24, 24, 1, 0, 0, 1, 0, 0),
(25, 25, 1, 6, 0, 0, 0, 0),
(26, 26, 1, 0, 20, 0, 0, 0),
(27, 27, 1, 0, 0, 0, 0, 0),
(28, 28, 1, 0, 0, 0, 0, 0),
(29, 29, 1, 0, 0, 0, 0, 0),
(30, 30, 1, 2, 90, 0, 1, 0);

CREATE  TABLE Team_stat(
	team_id INT ,
	matches_played INT,
	matches_wins INT,
	matches_lost INT,
	matches_draws INT,
	total_points INT,
	recent_form JSON,
    tournament_id INT, --updated
	PRIMARY KEY (team_id,tournament_id),
    FOREIGN KEY(team_id) REFERENCES Team(team_id),
    FOREIGN KEY(tournament_id) REFERENCES Tournament(tournament_id)
);

INSERT INTO team_stat (team_id, matches_played, matches_wins, matches_lost, matches_draws, total_points,recent_form,tournament_id)
VALUES 
(1, 7, 4, 3, 0, 8, ["W", "W", "W", "L", "W"], 1),
(2, 7, 7, 0, 0, 14, ["W", "W", "W", "W", "W"], 1),
(3, 7, 5, 1, 1, 11, ["D", "W", "W", "L", "W"], 1),
(4, 7, 1, 6, 0, 2, ["L", "L", "W", "L", "L"], 1),
(5, 7, 3, 4, 0, 6, ["L", "W", "W", "L", "W"], 1),
(6, 7, 0, 5, 2, 2, ["D", "L", "D", "L", "L"], 1),
(7, 7, 6, 1, 0, 12, ["L", "W", "W", "W", "W"], 1),
(8, 7, 5, 1, 1, 11, ["W", "D", "W", "L", "W"], 1);

/*CREATE TABLE Match_Stats (
	stat_id INT PRIMARY KEY AUTO_INCREMENT,
	match_id INT,
	category VARCHAR(50) NOT NULL,
	stat_type VARCHAR(50) NOT NULL,--changed
	home_team_count INT DEFAULT 0,
	away_team_count INT DEFAULT 0,
	FOREIGN KEY (match_id) REFERENCES Match_details(match_id));

INSERT INTO Match_Stats (stat_id, match_id, category, stat_type, home_team_count, away_team_count)
VALUES 
(1, 1, 'Attacker Skill', 'Simple Touch', 7, 7),
(2, 1, 'Attacker Skill', 'Dive', 0, 2),
(3, 1, 'Attacker Skill', 'Pole Dive', 2, 1),
(4, 1, 'Attacker Skill', 'Sudden Attempt', 0, 0),
(5, 1, 'Attacker Skill', 'Tap', 0, 0),
(6, 1, 'Defender Self Out', 'Out of Field', 0, 1),
(7, 1, 'Defender Self Out', 'Late Entry', 0, 0),
(8, 1, 'Defender Self Out', 'Retired', 0, 0),
(9, 1, 'Defender Self Out', 'Warning', 0, 0);*/

--NEW TABLES
CREATE  TABLE Team_Attack(
    Attack_id INT PRIMARY KEY AUTO_INCREMENT,
    match_id INT,
    team_id INT NOT NULL,
    points INT NOT NULL,
    inning INT CHECK(inning IN (1, 2, 3, 4)),
    phase VARCHAR(10) CHECK(phase IN ('Early','Mid','End','Unknown')),
	tournament_id INT,
    FOREIGN KEY (match_id) REFERENCES Match_details(match_id),
    FOREIGN KEY (team_id) REFERENCES Team(team_id),
	FOREIGN KEY (tournament_id) REFERENCES Tournament(tournament_id)
);

INSERT INTO Team_Attack (match_id,team_id,points,inning,phase,tournament_id)
VALUES
(1, 1, 1, 3, 1, 'Early', 1),
(2, 1, 2, 1, 1, 'Early', 1),
(3, 1, 1, 4, 1, 'Mid', 1),
(4, 1, 2, 3, 1, 'Mid', 1),
(5, 1, 1, 2, 2, 'Early', 1),
(6, 1, 2, 2, 2, 'Early', 1),
(7, 1, 1, 3, 2, 'Mid', 1),
(8, 1, 2, 5, 2, 'Mid', 1),
(9, 2, 3, 4, 1, 'Early', 1),
(10, 2, 4, 2, 1, 'Early', 1),
(11, 2, 3, 5, 1, 'Mid', 1),
(12, 2, 4, 3, 1, 'Mid', 1),
(13, 2, 3, 3, 1, 'End', 1),
(14, 2, 4, 4, 1, 'End', 1),
(15, 2, 3, 2, 2, 'Early', 1),
(16, 2, 4, 3, 2, 'Early', 1),
(17, 2, 3, 4, 2, 'Mid', 1),
(18, 2, 4, 5, 2, 'Mid', 1),
(19, 2, 3, 3, 2, 'End', 1),
(20, 2, 4, 2, 2, 'End', 1),
(21, 1, 1, 5, 1, 'End', 1),
(22, 1, 2, 3, 1, 'End', 1),
(23, 1, 1, 2, 2, 'End', 1),
(24, 1, 2, 6, 2, 'End', 1);



CREATE TABLE Team_Defence (
	defence_id INT PRIMARY KEY AUTO_INCREMENT,
	match_id INT NOT NULL,
	inning_no INT NOT NULL,
	team_id INT NOT NULL,
	batch_no INT NOT NULL,
	start_time FLOAT NOT NULL,
	end_time FLOAT NOT NULL,
	duration FLOAT NOT NULL,
	tournament_id INT,
	FOREIGN KEY (match_id) REFERENCES Match_details(match_id),
	FOREIGN KEY (team_id) REFERENCES Team(team_id),
	FOREIGN KEY (tournament_id) REFERENCES Tournament(tournament_id),
-- TABLE-LEVEL CHECK constraints
    CHECK (inning_no IN (1, 2, 3, 4)),
    CHECK (batch_no > 0),
    CHECK (start_time >= 0),
    CHECK (end_time > start_time),
    CHECK (duration > 0)
);

INSERT INTO Team_Defence (match_id,inning_no,team_id,batch_no,start_time,end_time,duration,tournament_id)
VALUES
(1, 1, 1, 1, 0,  3, 3, 1),
(1, 1, 1, 2, 3,  5.30,2.30, 1),
(1, 1, 1, 3, 5.30, 7,1.30, 1),
(1, 2, 1, 1, 0, 2.30,2.30, 1),
(1, 2, 1, 2, 2.30,  3.40,1.10, 1),
(1, 2, 1, 3, 3.40,  5,1.20, 1),
(1, 2, 1, 4, 5,  6.30,1.30, 1),
(1, 2, 1, 5, 6.30,  7,0.30, 1),
(1, 1, 2, 1, 0,  3.40,3.40, 1),
(1, 1, 2, 2, 3.40, 7,3.20, 1),
(1, 2, 2, 1, 0,  2.20,2.20, 1),
(1, 2, 2, 2, 2.20,4.40,2.20, 1),
(1, 2, 2, 3, 4.40, 7,2.20, 1);

/*CREATE TABLE Season (
	season_id INT PRIMARY KEY AUTO_INCREMENT,
	season_name VARCHAR(30) NOT NULL,
	tournament_id INT NOT NULL,
	start_date DATE NOT NULL,
	end_date DATE NOT NULL,
	FOREIGN KEY (tournament_id)
	REFERENCES Tournament(tournament_id),
	CHECK (start_date < end_date));

INSERT INTO Season (season_name,tournament_id,start_date,end_date)
VALUES
('Season 2020', 1, '2020-01-05', '2020-03-20'),
('Season 2021', 1, '2021-01-10', '2021-03-25'),
('Season 2022', 1, '2022-01-08', '2022-03-30'),
('Season 2023', 1, '2023-01-12', '2023-04-05'),
('Season 2024', 1, '2024-01-15', '2024-04-10');

CREATE TABLE Player_Role_History (
    player_id INT,
    season_id INT,
    role VARCHAR(20) CHECK (role IN ('Attacker','Defender','All-Rounder','Unknown')),
    PRIMARY KEY (player_id, season_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (season_id) REFERENCES Season(season_id)
);

INSERT INTO Player_Role_History (player_id,season_id,role)
VALUES
(1, 1, 'Attacker'),
(2, 1, 'Defender'),
(3, 1, 'All-Rounder'),
(4, 2, 'Attacker'),
(5, 2, 'Defender'),
(6, 2, 'All-Rounder'),
(7, 3, 'All-Rounder'),
(8, 3, 'Defender'),
(9, 3, 'Attacker'),
(10, 3, 'Attacker');*/


CREATE TABLE Player_tournament_stat (
    player_id INT NOT NULL,
    tournament_id INT NOT NULL,
    total_attack_points INT DEFAULT 0,
    total_defence_points INT DEFAULT 0,
    total_dives INT DEFAULT 0,
    matches_played INT DEFAULT 0,
    team_id INT NOT NULL,
    highest_score INT,
    pole_dives INT,
    sky_dives INT,
    assists INT,
    total_touches INT,
    avg_def_seconds INT,

    PRIMARY KEY (player_id, tournament_id),

    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (tournament_id) REFERENCES Tournament(tournament_id),
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
);


INSERT INTO player_tournament_stat 
(player_id, tournament_id, total_attack_points, total_defence_points, total_dives, matches_played, team_id, highest_attack_points, pole_dives, sky_dives, assists, total_touches, out_of_field, highest_def_time)
VALUES
(1,1,120,30,12,10,1,24,7,5,12,95,1,12),
(2,1,85,95,20,10,1,18,8,6,9,80,2,22),
(3,1,150,40,10,10,1,28,6,4,14,110,1,10),
(4,1,60,110,25,10,1,15,9,7,6,70,3,30),
(5,1,100,80,18,10,1,21,7,6,10,88,2,18),
(6,1,45,130,30,10,1,12,11,8,5,60,3,35),
(7,1,90,60,15,10,1,19,6,5,11,82,1,20),
(8,1,70,75,16,10,1,17,7,5,8,75,2,16);


CREATE TABLE Tournament(
    tournament_id INT PRIMARY KEY AUTO_INCREMENT,
    tournament_name VARCHAR(30) NOT NULL,
    tournament_type VARCHAR(30)
        CHECK (tournament_type IN ('All to all','Knockout','Group + Knockout','Unknown')),
    tournament_year INT
);

INSERT INTO Tournament (tournament_name,tournament_type,tournament_year)
VALUES
('National Kho-Kho League', 'All to all', 2020),
('Inter-University Championship', 'Knockout', 2020),
('State Level Tournament', 'Group + Knockout', 2021),
('Junior Nationals', 'All to all', 2021),
('Senior Nationals', 'Knockout', 2022),
('Inter-School League', 'Group + Knockout', 2022),
('University Premier League', 'All to all', 2023),
('Women National Championship', 'Group + Knockout', 2023),
('Kho-Kho Pro League', 'Knockout', 2024),
('National Games Kho-Kho', 'All to all', 2024);

/*CREATE TABLE Match_Awards(
    match_id INT,
    award_type VARCHAR(20) CHECK (award_type IN ('Best AllRounder','Best Attacker','Best Defender')),   
    player_id INT,
    tournament_id INT,
    PRIMARY KEY (match_id, award_type),
    FOREIGN KEY (match_id) REFERENCES Match_details(match_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (tournament_id) REFERENCES Tournament(tournament_id)
);

INSERT INTO Match_Awards (match_id,award_type,player_id,tournament_id)
VALUES
(1, 'Best AllRounder', 5, 1),
(1, 'Best Attacker', 8, 1),
(1, 'Best Defender', 3, 1),
(2, 'Best Defender', 6, 1),
(2, 'Best AllRounder', 9, 1),
(3, 'Best Attacker', 4, 2),
(4, 'Best Defender', 2, 2),
(5, 'Best Defender', 10, 3),
(5, 'Best AllRounder', 11, 3);

CREATE TABLE Player_Defence (
    player_def_id INT PRIMARY KEY AUTO_INCREMENT,
    match_id INT,
    player_id INT,
    inning_no INT,
    start_seconds INT,
    end_seconds INT,
    duration_seconds INT,
    FOREIGN KEY (match_id) REFERENCES Match_details(match_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id)
    );

INSERT INTO Player_Defence
(match_id, player_id, inning_no, start_seconds, end_seconds, duration_seconds)
VALUES
(1,1,1,30,90,60),
(1,3,1,100,130,30),
(1,3,2,50,80,30),
(1,4,1,0,70,70),
(1,4,1,150,200,50),
(1,4,2,100,130,30),
(1,5,2,200,260,60),
(1,6,1,200,280,80),
(1,6,2,50,150,100),
(1,7,1,300,360,60),
(1,7,2,150,210,60),
(1,8,2,10,50,40),
(1,9,1,50,90,40),
(1,9,2,250,290,40),
(1,10,1,180,210,30),
(1,10,2,300,360,60);


CREATE TABLE Player_Attack(
    player_attack_id INT PRIMARY KEY AUTO_INCREMENT,
    match_id INT,
    player_id INT,
    inning INT,
    phase VARCHAR(10),
    points INT,
    FOREIGN KEY (match_id) REFERENCES Match_details(match_id),
	FOREIGN KEY (player_id) REFERENCES Player(player_id)
	);

INSERT INTO Player_Attack
(match_id, player_id, inning, phase, points)
VALUES
(1,1,1,'Early',3),
(1,1,1,'Mid',2),
(1,1,2,'End',3),
(1,2,1,'Mid',4),
(1,2,2,'End',2),
(1,5,1,'Early',4),
(1,5,2,'Mid',3),
(1,5,2,'End',3),
(1,6,1,'End',3),
(1,6,2,'Mid',2),
(2,7,1,'Early',4),
(2,7,1,'Mid',3),
(2,7,2,'End',4),
(2,8,1,'Mid',5),
(2,8,2,'End',3),
(2,9,1,'Early',6),
(2,9,2,'Mid',4),
(2,9,2,'End',3),
(2,10,1,'End',2),
(2,10,2,'Mid',3),
(3,1,1,'Early',2),
(3,1,2,'End',3),
(3,2,1,'Mid',3),
(3,2,2,'End',2),
(3,3,1,'Early',4),
(3,3,2,'Mid',3),
(4,5,1,'Early',5),
(4,5,1,'Mid',3),
(4,5,2,'End',4),
(4,6,1,'Mid',4),
(4,6,2,'End',3),
(4,7,1,'Early',6),
(4,7,2,'Mid',4),
(5,5,1,'Early',4),
(5,5,1,'Mid',3),
(5,5,2,'End',5),
(5,6,1,'Mid',4),
(5,6,2,'End',3),
(5,9,1,'Early',5),
(5,9,2,'Mid',4);*/


-- Don't add values here
CREATE TABLE raw_match_file_log(
	file_id INT PRIMARY KEY AUTO_INCREMENT,
	file_name VARCHAR(200),
	file_type VARCHAR(50),
	uploaded_by VARCHAR(30),
	uploaded_at DATETIME
);

CREATE TABLE raw_match_data(
	raw_id INT PRIMARY KEY AUTO_INCREMENT,
	file_id INT,
	raw_match_id VARCHAR(50),
	raw_match_date VARCHAR(50),
	raw_home_team VARCHAR(30),
	raw_away_team VARCHAR(30),
	raw_home_team_score VARCHAR(50),
	raw_away_team_score VARCHAR(50),
	raw_result VARCHAR(50),
	raw_winner VARCHAR(30),
	raw_venue VARCHAR(100),
	FOREIGN KEY (file_id) REFERENCES raw_match_file_log(file_id)
);

CREATE TABLE raw_attack_details(
	raw_attack_id INT PRIMARY KEY AUTO_INCREMENT,
	file_id INT,
    raw_match INT,
    raw_team_name VARCHAR(50),
    raw_points INT,
    raw_inning INT ,
    raw_phase VARCHAR(10),
	FOREIGN KEY (file_id) REFERENCES raw_match_file_log(file_id),
	FOREIGN KEY (raw_match) REFERENCES raw_match_data(raw_id)
); 

CREATE TABLE raw_defence_details(
	raw_defence_id INT PRIMARY KEY AUTO_INCREMENT,
	file_id INT,
    raw_match INT,
    raw_team_name VARCHAR(50),
    raw_batch INT,
    raw_inning INT ,
	raw_start_time FLOAT,
    raw_end_time FLOAT,
	FOREIGN KEY (file_id) REFERENCES raw_match_file_log(file_id),
	FOREIGN KEY (raw_match) REFERENCES raw_match_data(raw_id)
);

CREATE TABLE raw_match_stats (
	raw_stat_id INT PRIMARY KEY AUTO_INCREMENT,
	file_id INT,
	raw_match INT,
	raw_category VARCHAR(50),
	raw_stat_type VARCHAR(50),
	raw_home_team_count INT,
	raw_away_team_count INT,
	FOREIGN KEY (file_id) REFERENCES raw_match_file_log(file_id),
	FOREIGN KEY (raw_match) REFERENCES raw_match_data(raw_id)
	);






















