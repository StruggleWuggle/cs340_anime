/* Team: Team 175
   Team Members: August Le, Anna Ryplewski
   Project Title: Anime Recommender System
*/

-- Disable foreign key checks to drop tables and minimize import errors
SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

-- Drop tables if they exist
DROP TABLE IF EXISTS user_anime_ratings;
DROP TABLE IF EXISTS streaming_service_users;
DROP TABLE IF EXISTS streaming_anime;
DROP TABLE IF EXISTS anime;
DROP TABLE IF EXISTS app_users;
DROP TABLE IF EXISTS streaming_services;

-- Create 'streaming_services' table
CREATE TABLE streaming_services (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(255) NOT NULL
);

-- Create 'app_users' table
CREATE TABLE app_users (
    app_user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    age INT NOT NULL CHECK (age > 0),
    gender CHAR(1),
    location VARCHAR(255)
);

-- Create 'anime' table
CREATE TABLE anime (
    anime_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE DEFAULT NULL,
    service_id INT NOT NULL,
    genre VARCHAR(255) NOT NULL,
    maturity_rating VARCHAR(50) NOT NULL,
    trigger_warnings VARCHAR(255),
    num_episodes INT,
    FOREIGN KEY (service_id) REFERENCES streaming_services(service_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create 'streaming_anime' table (junction table for streaming services and anime)
CREATE TABLE streaming_anime (
    service_id INT NOT NULL,
    anime_id INT NOT NULL,
    PRIMARY KEY (service_id, anime_id),
    FOREIGN KEY (service_id) REFERENCES streaming_services(service_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (anime_id) REFERENCES anime(anime_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create 'streaming_service_users' table (junction table for users and streaming services)
CREATE TABLE streaming_service_users (
    service_id INT NOT NULL,
    app_user_id INT NOT NULL,
    PRIMARY KEY (service_id, app_user_id),
    FOREIGN KEY (service_id) REFERENCES streaming_services(service_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (app_user_id) REFERENCES app_users(app_user_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create 'user_anime_ratings' table (users rating anime)
CREATE TABLE user_anime_ratings (
    app_user_id INT NOT NULL,
    anime_id INT NOT NULL,
    preference INT NOT NULL,
    PRIMARY KEY (app_user_id, anime_id),
    FOREIGN KEY (app_user_id) REFERENCES app_users(app_user_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (anime_id) REFERENCES anime(anime_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Enable foreign key checks
SET FOREIGN_KEY_CHECKS=1;

-- Insert example data
INSERT INTO streaming_services (service_name) VALUES
    ('Crunchyroll'),
    ('Netflix'),
    ('Peacock'),
    ('Hulu'),
    ('Amazon Prime');

INSERT INTO app_users (name, password, age, gender, location) VALUES
    ('Alice', 'password123', 25, 'F', 'USA'),
    ('Bob', 'securepass', 30, 'M', 'Canada'),
    ('Charlie', 'animefan99', 22, 'N', 'UK'),
    ('Diana', 'mypassword', 28, 'F', 'Germany');

INSERT INTO anime (title, start_date, end_date, service_id, genre, maturity_rating, trigger_warnings, num_episodes) VALUES
    ('Attack on Titan', '2013-04-07', '2022-11-13', 1, 'Action', 'TV-MA', 'Violence', 87),
    ('Naruto', '2002-10-03', '2017-03-23', 2, 'Adventure', 'PG-13', 'Mild Violence', 720),
    ('One Piece', '1999-10-20', NULL, 3, 'Fantasy', 'PG-13', 'Adventure', 1000),
    ('Death Note', '2006-10-04', '2007-06-27', 4, 'Thriller', 'TV-MA', 'Psychological', 37),
    ('Demon Slayer', '2019-04-06', NULL, 5, 'Action', 'PG-13', 'Intense Action', 44);

INSERT INTO streaming_anime (service_id, anime_id) VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5);

INSERT INTO streaming_service_users (service_id, app_user_id) VALUES
    (1, 1),
    (2, 1),
    (3, 1),
    (1, 2),
    (4, 3);

INSERT INTO user_anime_ratings (app_user_id, anime_id, preference) VALUES
    (1, 1, 5),
    (1, 3, 3),
    (2, 1, 0),
    (4, 4, -3);

-- Commit the transaction to finalize inserts
COMMIT;
