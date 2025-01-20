"""Update recipe structure

Revision ID: update_recipe_structure
Revises: 310d384eaf6b
Create Date: 2024-01-25
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Update recipes table
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        # Add new columns
        batch_op.add_column(sa.Column('title', sa.String(100), server_default=''))
        batch_op.add_column(sa.Column('cook_time', sa.Integer(), server_default='0'))
        batch_op.add_column(sa.Column('difficulty', sa.String(20), server_default='medium'))
        batch_op.add_column(sa.Column('category_id', sa.Integer()))
        
        # Copy data from old columns to new ones
        op.execute('UPDATE recipes SET title = name')
        
        # Drop old columns
        batch_op.drop_column('name')
        batch_op.drop_column('is_reported')
        batch_op.drop_column('is_approved')
        batch_op.drop_column('is_hidden')
        batch_op.drop_column('is_featured')
        batch_op.drop_column('rejection_reason')
        batch_op.drop_column('subcategory')
        
        # Add foreign key constraints
        batch_op.create_foreign_key(
            'fk_recipes_category',
            'categories',
            ['category_id'],
            ['id'],
            ondelete='SET NULL'
        )
        batch_op.create_foreign_key(
            'fk_recipes_user',
            'users',
            ['user_id'],
            ['id'],
            ondelete='CASCADE'
        )

def downgrade():
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        # Remove foreign keys
        batch_op.drop_constraint('fk_recipes_category', type_='foreignkey')
        batch_op.drop_constraint('fk_recipes_user', type_='foreignkey')
        
        # Add back old columns
        batch_op.add_column(sa.Column('name', sa.TEXT()))
        batch_op.add_column(sa.Column('is_reported', sa.BOOLEAN()))
        batch_op.add_column(sa.Column('is_approved', sa.BOOLEAN()))
        batch_op.add_column(sa.Column('is_hidden', sa.BOOLEAN()))
        batch_op.add_column(sa.Column('is_featured', sa.BOOLEAN()))
        batch_op.add_column(sa.Column('rejection_reason', sa.TEXT()))
        batch_op.add_column(sa.Column('subcategory', sa.VARCHAR(100)))
        
        # Copy data back
        op.execute('UPDATE recipes SET name = title')
        
        # Drop new columns
        batch_op.drop_column('category_id')
        batch_op.drop_column('difficulty')
        batch_op.drop_column('cook_time')
        batch_op.drop_column('title') 