"""Update recipe relationships

Revision ID: new_migration
Revises: previous_migration
Create Date: 2024-01-25
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Add cascade deletes
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.drop_constraint('fk_recipes_user', type_='foreignkey')
        batch_op.drop_constraint('fk_recipes_category', type_='foreignkey')
        batch_op.create_foreign_key('fk_recipes_user', 'users', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key('fk_recipes_category', 'categories', ['category_id'], ['id'], ondelete='SET NULL')

    with op.batch_alter_table('ingredients', schema=None) as batch_op:
        batch_op.drop_constraint('fk_ingredients_recipe', type_='foreignkey')
        batch_op.create_foreign_key('fk_ingredients_recipe', 'recipes', ['recipe_id'], ['id'], ondelete='CASCADE')

def downgrade():
    with op.batch_alter_table('ingredients', schema=None) as batch_op:
        batch_op.drop_constraint('fk_ingredients_recipe', type_='foreignkey')
        batch_op.create_foreign_key('fk_ingredients_recipe', 'recipes', ['recipe_id'], ['id'])

    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.drop_constraint('fk_recipes_category', type_='foreignkey')
        batch_op.drop_constraint('fk_recipes_user', type_='foreignkey')
        batch_op.create_foreign_key('fk_recipes_category', 'categories', ['category_id'], ['id'])
        batch_op.create_foreign_key('fk_recipes_user', 'users', ['user_id'], ['id']) 