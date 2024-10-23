CREATE TABLE my_app_schema.books
(
	id_book SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	year INT NOT NULL CHECK (year >= -1000 AND year < 2025)
);

INSERT INTO my_app_schema.books VALUES
(1, 'Война и мир', 1867),
(2, 'Детство', 1852),
(3, 'Евгений Онегин', 1833),
(4, 'Старик и море', 1952),
(5, 'Приключения Тома Сойера', 1876),
(6, '12 стульев', 1928),
(7, 'Библия', 0);