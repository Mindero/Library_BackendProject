DROP TABLE IF EXISTS my_app_schema.readers;

CREATE TABLE my_app_schema.readers
(
	reader_ticket SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	phone_number VARCHAR(20) UNIQUE NOT NULL CHECK (phone_number ~ '^\+?[0-9\s\-()]+$'),
	email  VARCHAR(255) UNIQUE NOT NULL CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'),
	passport VARCHAR(10) UNIQUE NOT NULL
--	created_date DATE NOT NULL
);

INSERT INTO my_app_schema.readers VALUES
--(default,Иванов Иван Иванович,+79152851491,ivanov@mail.ru,5412572382,2024-10-08),
--(default,Сидоров Сергей Сергеевич,+71241121414,sidorov@sgu.ru,9309156613,2024-10-02),
--(default,Алексеева Вера Максимовна,+73133131431,alexeeva@pochta.com,1210491998,2024-09-10),
--(default,Орлова Мария Александровна,+79999999999,orlova@gmail.com,1231231231,2023-01-25),
--(default,Мухин Михаил Ильич,+71111111111,muhin@sobaka.ru,1234567890,2024-05-23),
--(default,Евгений Петрович Петров,+71111111112,petrov@mail.ru,0987654321,2024-10-08);
(default,'Иванов Иван Иванович','+79152851491','ivanov@mail.ru','5412572382'),
(default,'Сидоров Сергей Сергеевич','+71241121414','sidorov@sgu.ru','9309156613'),
(default,'Алексеева Вера Максимовна','+73133131431','alexeeva@pochta.com','1210491998'),
(default,'Орлова Мария Александровна','+79999999999','orlova@gmail.com','1231231231'),
(default,'Мухин Михаил Ильич','+71111111111','muhin@sobaka.ru','1234567890'),
(default,'Евгений Петрович Петров','+71111111112','petrov@mail.ru','0987654321');