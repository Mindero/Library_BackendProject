"""add foreign keys

Revision ID: 15f8b2c5d867
Revises: 291f6fe7f3f4
Create Date: 2024-11-18 09:05:04.081036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15f8b2c5d867'
down_revision: Union[str, None] = '291f6fe7f3f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'authors_book', 'books', ['id_book'], ['id_book'], source_schema='my_app_schema', referent_schema='my_app_schema', onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'authors_book', 'authors', ['id_author'], ['id_author'], source_schema='my_app_schema', referent_schema='my_app_schema', onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'book_genres', 'genres', ['id_genre'], ['id_genre'], source_schema='my_app_schema', referent_schema='my_app_schema', onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'book_genres', 'books', ['id_book'], ['id_book'], source_schema='my_app_schema', referent_schema='my_app_schema', onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'book_instance', 'book_publisher', ['id_book_publisher'], ['id_book_publisher'], source_schema='my_app_schema', referent_schema='my_app_schema', onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'book_publisher', 'books', ['id_book'], ['id_book'], source_schema='my_app_schema', referent_schema='my_app_schema', onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'book_publisher', 'publishers', ['id_publisher'], ['id_publisher'], source_schema='my_app_schema', referent_schema='my_app_schema', onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'book_reader', 'book_instance', ['id_instance'], ['id_instance'], source_schema='my_app_schema', referent_schema='my_app_schema', onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'book_reader', 'readers', ['reader_ticket'], ['reader_ticket'], source_schema='my_app_schema', referent_schema='my_app_schema', onupdate='CASCADE', ondelete='CASCADE')
    op.add_column('penalty', sa.Column('id_book_reader', sa.Integer(), nullable=False), schema='my_app_schema')
    op.create_foreign_key(None, 'penalty', 'book_reader', ['id_book_reader'], ['id_book_reader'], source_schema='my_app_schema', referent_schema='my_app_schema', onupdate='CASCADE', ondelete='CASCADE')
    op.drop_column('penalty', 'id_authors_book', schema='my_app_schema')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('penalty', sa.Column('id_authors_book', sa.INTEGER(), autoincrement=True, nullable=False), schema='my_app_schema')
    op.drop_constraint(None, 'penalty', schema='my_app_schema', type_='foreignkey')
    op.drop_column('penalty', 'id_book_reader', schema='my_app_schema')
    op.drop_constraint(None, 'book_reader', schema='my_app_schema', type_='foreignkey')
    op.drop_constraint(None, 'book_reader', schema='my_app_schema', type_='foreignkey')
    op.drop_constraint(None, 'book_publisher', schema='my_app_schema', type_='foreignkey')
    op.drop_constraint(None, 'book_publisher', schema='my_app_schema', type_='foreignkey')
    op.drop_constraint(None, 'book_instance', schema='my_app_schema', type_='foreignkey')
    op.drop_constraint(None, 'book_genres', schema='my_app_schema', type_='foreignkey')
    op.drop_constraint(None, 'book_genres', schema='my_app_schema', type_='foreignkey')
    op.drop_constraint(None, 'authors_book', schema='my_app_schema', type_='foreignkey')
    op.drop_constraint(None, 'authors_book', schema='my_app_schema', type_='foreignkey')
    # ### end Alembic commands ###
