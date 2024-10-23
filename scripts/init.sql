SET search_path TO my_app_schema;

DROP TABLE IF EXISTS penalty;
DROP TABLE IF EXISTS book_reader;
DROP TABLE IF EXISTS readers;
DROP TABLE IF EXISTS book_instance;
DROP TABLE IF EXISTS book_publisher;
DROP TABLE IF EXISTS publishers;
DROP TABLE IF EXISTS book_genres;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS authors_book;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;

CREATE TABLE authors
(
	id_author SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	country TEXT NOT NULL,
	birthday DATE
);
INSERT INTO authors VALUES
(default, 'Лев Николаевич Толстой', 'Россия', '1828-09-09'),
(default, 'Николай Васильевич Гоголь', 'Россия', '1809-04-01'),
(default, 'Александр Сергеевич Пушкин', 'Россия', '1799-06-06'),
(default, 'Эрнест Миллер Хемингуэй', 'США', '1899-07-21'),
(default, 'Марк Твен', 'США', '1835-11-30'),
(default, 'Илья Арнольдович Ильф', 'Россия', '1897-10-15'),
(default, 'Евгений Петрович Петров', 'Россия', '1902-12-13');

CREATE TABLE books
(
	id_book SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	year INT NOT NULL CHECK (year >= -1000 AND year < 2025)
);
INSERT INTO books VALUES
(1, 'Война и мир', 1867),
(2, 'Детство', 1852),
(3, 'Евгений Онегин', 1833),
(4, 'Старик и море', 1952),
(5, 'Приключения Тома Сойера', 1876),
(6, '12 стульев', 1928),
(7, 'Библия', 0);

CREATE TABLE authors_book
(
	id_authors_book SERIAL PRIMARY KEY,
	id_book INT REFERENCES books(id_book),
	id_author INT REFERENCES authors(id_author)
);
INSERT INTO authors_book VALUES
(DEFAULT, 1, 1),
(DEFAULT, 2, 1),
(DEFAULT, 3, 3),
(DEFAULT, 4, 4),
(DEFAULT, 5, 5),
(DEFAULT, 6, 6),
(DEFAULT, 6, 7);

CREATE TABLE genres
(
	id_genre SERIAL PRIMARY KEY,
	name TEXT UNIQUE NOT NULL
);
INSERT INTO genres VALUES
(DEFAULT, 'роман'),
(DEFAULT, 'детская литература'),
(DEFAULT, 'стихотворение');

CREATE TABLE book_genres
(
	id_book_genres SERIAL PRIMARY KEY,
	id_book INT REFERENCES books(id_book),
	id_genre INT REFERENCES genres(id_genre)
);
INSERT INTO book_genres VALUES
(DEFAULT, 1, 1),
(DEFAULT, 2, 1),
(DEFAULT, 3, 1),
(DEFAULT, 3, 3),
(DEFAULT, 4, 1),
(DEFAULT, 5, 1),
(DEFAULT, 5, 2),
(DEFAULT, 6, 1);

CREATE TABLE publishers
(
	id_publisher SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	inn VARCHAR(12) UNIQUE CHECK (LENGTH(inn) = 10 OR LENGTH(inn) = 12),
	country TEXT
);
INSERT INTO publishers VALUES
(DEFAULT, 'Эксмо-АСТ', '7708188426', 'Россия'),
(DEFAULT, 'ИП Просвещение', '7715995942', 'Россия'),
(DEFAULT, 'Питер', '9909041385', 'Россия'),
(DEFAULT, 'Самиздат', '0000000000', 'Россия');

CREATE TABLE book_publisher
(
	id_book_publisher SERIAL PRIMARY KEY,
	id_book INT REFERENCES books(id_book),
	id_publisher INT REFERENCES publishers(id_publisher),
	UNIQUE (id_book, id_publisher)
);
INSERT INTO book_publisher VALUES
(DEFAULT, 1, 1),
(DEFAULT, 1, 2),
(DEFAULT, 2, 1),
(DEFAULT, 3, 1),
(DEFAULT, 6, 3),
(DEFAULT, 6, DEFAULT); 

CREATE TABLE book_instance
(
	id_instance SERIAL PRIMARY KEY,
	id_book_publisher INT REFERENCES book_publisher(id_book_publisher),
	supply_date DATE NOT NULL,
	taken_now BOOLEAN NOT NULL
);
INSERT INTO book_instance VALUES
(DEFAULT, 1, '2024-10-07', true),
(DEFAULT, 2, '2024-09-15', false),
(DEFAULT, 6, '2023-01-30', false),
(DEFAULT, 4, '2024-10-01', true),
(DEFAULT, 4, '2024-10-01', true);

CREATE TABLE readers
(
	reader_ticket SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	phone_number VARCHAR(20) UNIQUE NOT NULL CHECK (phone_number ~ '^\+?[0-9\s\-()]+$'),
	email  VARCHAR(255) UNIQUE NOT NULL CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'),
	passport VARCHAR(10) UNIQUE NOT NULL,
	created_date DATE NOT NULL
);
INSERT INTO readers VALUES
(default,'Иванов Иван Иванович','+79152851491','ivanov@mail.ru','5412572382', '2024-10-08'),
(default,'Сидоров Сергей Сергеевич','+71241121414','sidorov@sgu.ru','9309156613', '2024-10-02'),
(default,'Алексеева Вера Максимовна','+73133131431','alexeeva@pochta.com','1210491998', '2024-09-10'),
(default,'Орлова Мария Александровна','+79999999999','orlova@gmail.com','1231231231', '2023-01-25'),
(default,'Мухин Михаил Ильич','+71111111111','muhin@sobaka.ru','1234567890', '2024-05-23'),
(default,'Евгений Петрович Петров','+71111111112','petrov@mail.ru','0987654321', '2024-10-08');

CREATE TABLE book_reader
(
	id_book_reader SERIAL PRIMARY KEY,
	reader_ticket INT REFERENCES readers(reader_ticket),
	id_instance INT REFERENCES book_instance(id_instance),
	borrow_date DATE,
	end_date DATE
);
INSERT INTO book_reader VALUES
(DEFAULT, 1, 3, '2024-10-08', '2024-10-16'),
(DEFAULT, 5, 4, '2024-09-30', '2024-10-06'),
(DEFAULT, 5, 2, '2024-10-15', '2024-10-16');

CREATE TABLE penalty
(
	id_book_reader INT PRIMARY KEY REFERENCES book_reader(id_book_reader),
	start_time DATE,
	payment INT
);
INSERT INTO penalty VALUES
(2, '2024-10-07', 10),
(3, '2024-10-15', 20);
