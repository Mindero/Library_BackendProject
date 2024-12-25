"""add supply_view triggers

Revision ID: c2d8484989ad
Revises: af774006a0a3
Create Date: 2024-12-26 01:18:55.736783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.project.core.config import settings

# revision identifiers, used by Alembic.
revision: str = 'c2d8484989ad'
down_revision: Union[str, None] = 'af774006a0a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(f"""
        -- Создаем функцию триггера
        CREATE OR REPLACE FUNCTION delete_from_supply_view()
        RETURNS TRIGGER AS $$
        DECLARE
           book_id INT;
           publisher_id INT;
           book_publisher_id INT;
       BEGIN
           -- 1. Найти id_book в таблице books
           SELECT id_book INTO book_id
           FROM my_app_schema.books
           WHERE name = NEW.book_name;

           IF NOT FOUND THEN
               RAISE EXCEPTION 'Book with name % not found', NEW.book_name;
           END IF;

           -- 2. Найти publisher_id в таблице publishers по имени
           SELECT id_publisher INTO publisher_id
           FROM my_app_schema.publishers
           WHERE name = NEW.publisher_name;

           IF NOT FOUND THEN
               RAISE EXCEPTION 'Publisher with name % not found', NEW.publisher_name;
           END IF;

           -- 3. Найти id_book_publisher в таблице book_publishers
           SELECT id_book_publisher INTO book_publisher_id
           FROM my_app_schema.book_publisher
           WHERE book_publisher.id_book = book_id AND book_publisher.id_publisher = publisher_id;

           IF NOT FOUND THEN
               RAISE EXCEPTION 'Book publisher relation not found for book_id % and publisher_id %',
                   book_id, publisher_id;
           END IF;

            -- 4. Удалить все записи в instances, у которых id_book_publisher и supply_date совпадают
            DELETE FROM {settings.POSTGRES_SCHEMA}.book_instance
            WHERE book_instance.id_book_publisher = book_publisher_id AND book_instance.supply_date = OLD.supply_date;

            -- Успешно завершить операцию
            RETURN OLD;
        END;
        $$ LANGUAGE plpgsql;
        """)
    op.execute(f"""
    -- Создаем триггер на представление VIEW
        CREATE TRIGGER trigger_delete_from_view
        INSTEAD OF DELETE ON {settings.POSTGRES_SCHEMA}.supply_view
        FOR EACH ROW
        EXECUTE FUNCTION delete_from_supply_view();
    """)

    op.execute(f"""
       -- Создание функции триггера
    CREATE OR REPLACE FUNCTION insert_into_supply_view()
       RETURNS TRIGGER AS $$
       DECLARE
           book_id INT;
           publisher_id INT;
           book_publisher_id INT;
       BEGIN
           -- 1. Найти id_book в таблице books
           SELECT id_book INTO book_id
           FROM my_app_schema.books
           WHERE name = NEW.book_name;

           IF NOT FOUND THEN
               RAISE EXCEPTION 'Book with name % not found', NEW.book_name;
           END IF;

           -- 2. Найти publisher_id в таблице publishers по имени
           SELECT id_publisher INTO publisher_id
           FROM my_app_schema.publishers
           WHERE name = NEW.publisher_name;

           IF NOT FOUND THEN
               RAISE EXCEPTION 'Publisher with name % not found', NEW.publisher_name;
           END IF;

           -- 3. Найти id_book_publisher в таблице book_publishers
           SELECT id_book_publisher INTO book_publisher_id
           FROM my_app_schema.book_publisher
           WHERE book_publisher.id_book = book_id AND book_publisher.id_publisher = publisher_id;

           IF NOT FOUND THEN
               RAISE EXCEPTION 'Book publisher relation not found for book_id % and publisher_id %',
                   book_id, publisher_id;
           END IF;

           -- 4. Добавить записи в instances `count` раз
            INSERT INTO my_app_schema.book_instance
            VALUES (DEFAULT, book_publisher_id, NEW.supply_date, false);

           -- Успешно завершить операцию
           RETURN NEW;
       END;
       $$ LANGUAGE plpgsql;
       """)
    op.execute(f"""
        -- Создание триггера для вставки
       CREATE TRIGGER trigger_insert_into_view
       INSTEAD OF INSERT ON {settings.POSTGRES_SCHEMA}.supply_view
       FOR EACH ROW
       EXECUTE FUNCTION insert_into_supply_view();
    """)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(f"""
        DROP TRIGGER trigger_delete_from_view;
    """)

    op.execute(f"""
    DROP FUNCTION delete_from_supply_view;
    """)

    op.execute(f"""
            DROP TRIGGER trigger_insert_into_view;
        """)

    op.execute(f"""
        DROP FUNCTION insert_into_supply_view;
        """)
    # ### end Alembic commands ###
