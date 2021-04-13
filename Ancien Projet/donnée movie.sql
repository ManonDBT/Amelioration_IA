DROP SCHEMA IF EXISTS movie;
CREATE SCHEMA movie;
USE movie;

DROP TABLE IF EXISTS classement;
CREATE TABLE classement (
`id` INT NOT NULL AUTO_INCREMENT,
    imdb float(10) NOT NULL,
    votes DECIMAL(30) NULL,
    metascore DECIMAL(10) NULL,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS style;
CREATE TABLE style (
id_genre INT NOT NULL AUTO_INCREMENT,
    genre varchar(30) NOT NULL,
    PRIMARY KEY (id_genre)
);

DROP TABLE IF EXISTS films;
CREATE TABLE films (
id_films INT NOT NULL AUTO_INCREMENT,
movie VARCHAR(500),
years VARCHAR(50),
PRIMARY KEY ( id_films )
);


DROP TABLE IF EXISTS note;
CREATE TABLE  note (
    id_films INT NOT NULL ,
    id INT NOT NULL ,
    PRIMARY KEY (id_films, id),
    FOREIGN KEY (id_films) REFERENCES films(id_films),
    FOREIGN KEY (id) REFERENCES classement(id)
);


DROP TABLE IF EXISTS id_movie;
CREATE TABLE  id_movie (
    id_films INT NOT NULL ,
    id_genre INT NOT NULL ,   
    PRIMARY KEY (id_films, id_genre),
    FOREIGN KEY (id_films) REFERENCES films(id_films),
    FOREIGN KEY (id_genre) REFERENCES style(id_genre)
);
