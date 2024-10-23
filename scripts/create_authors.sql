CREATE TABLE my_app_schema.authors
(
	id_author SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	country TEXT NOT NULL,
	birthday DATE
);

INSERT INTO my_app_schema.authors VALUES
(default, 'Лев Николаевич Толстой', 'Россия', '1828-09-09'),
(default, 'Николай Васильевич Гоголь', 'Россия', '1809-04-01'),
(default, 'Александр Сергеевич Пушкин', 'Россия', '1799-06-06'),
(default, 'Эрнест Миллер Хемингуэй', 'США', '1899-07-21'),
(default, 'Марк Твен', 'США', '1835-11-30'),
(default, 'Илья Арнольдович Ильф', 'Россия', '1897-10-15'),
(default, 'Евгений Петрович Петров', 'Россия', '1902-12-13');
