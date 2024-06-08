"""create tables

Revision ID: db143061298e
Revises: 
Create Date: 2024-06-07 22:31:41.576160

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db143061298e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment_method',
    sa.Column('payment_method_id', sa.Integer(), nullable=False),
    sa.Column('method_name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('payment_method_id')
    )
    op.create_table('restaurant',
    sa.Column('restaurant_id', sa.Integer(), nullable=False),
    sa.Column('restaurant_name', sa.String(length=255), nullable=True),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('contact', sa.String(length=255), nullable=True),
    sa.Column('total_seats', sa.Integer(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('image', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('restaurant_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('availability',
    sa.Column('availability_id', sa.Integer(), nullable=False),
    sa.Column('available_seats', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.restaurant_id'], ),
    sa.PrimaryKeyConstraint('availability_id')
    )
    op.create_table('organizer',
    sa.Column('organizer_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('organizer_id')
    )
    op.create_table('preference',
    sa.Column('preference_id', sa.Integer(), nullable=False),
    sa.Column('genre', sa.String(length=255), nullable=True),
    sa.Column('smoking_allowed', sa.Boolean(), nullable=True),
    sa.Column('budget', sa.Float(), nullable=True),
    sa.Column('additional_info', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('preference_id')
    )
    op.create_table('restaurant_details',
    sa.Column('restaurant_details_id', sa.Integer(), nullable=False),
    sa.Column('genre', sa.String(length=255), nullable=True),
    sa.Column('smoking_allowed', sa.Boolean(), nullable=True),
    sa.Column('budget', sa.Float(), nullable=True),
    sa.Column('additional_info', sa.String(length=255), nullable=True),
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.restaurant_id'], ),
    sa.PrimaryKeyConstraint('restaurant_details_id')
    )
    op.create_table('event',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('event_name', sa.String(length=255), nullable=True),
    sa.Column('event_date', sa.DateTime(), nullable=True),
    sa.Column('total_cost', sa.Float(), nullable=True),
    sa.Column('primary_participant_count', sa.Integer(), nullable=True),
    sa.Column('secondary_participant_count', sa.Integer(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('organizer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organizer_id'], ['organizer.organizer_id'], ),
    sa.PrimaryKeyConstraint('event_id')
    )
    op.create_table('reservation',
    sa.Column('reservation_id', sa.Integer(), nullable=False),
    sa.Column('reservation_date', sa.DateTime(), nullable=True),
    sa.Column('reserved_seats', sa.Integer(), nullable=True),
    sa.Column('reservation_status', sa.Integer(), nullable=True),
    sa.Column('arrival_time', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.Column('organizer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organizer_id'], ['organizer.organizer_id'], ),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.restaurant_id'], ),
    sa.PrimaryKeyConstraint('reservation_id')
    )
    op.create_table('participant',
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.Column('is_attending', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.event_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('participant_id')
    )
    op.create_table('payment',
    sa.Column('payment_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('payment_date', sa.DateTime(), nullable=True),
    sa.Column('payment_status', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('participant_id', sa.Integer(), nullable=True),
    sa.Column('payment_method_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.participant_id'], ),
    sa.ForeignKeyConstraint(['payment_method_id'], ['payment_method.payment_method_id'], ),
    sa.PrimaryKeyConstraint('payment_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment')
    op.drop_table('participant')
    op.drop_table('reservation')
    op.drop_table('event')
    op.drop_table('restaurant_details')
    op.drop_table('preference')
    op.drop_table('organizer')
    op.drop_table('availability')
    op.drop_table('user')
    op.drop_table('restaurant')
    op.drop_table('payment_method')
    # ### end Alembic commands ###