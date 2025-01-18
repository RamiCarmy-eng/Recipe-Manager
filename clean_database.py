import sqlite3


def cleanup_database():
    db = sqlite3.connect('instance/recipes.db')
    cursor = db.cursor()

    try:
        cursor.execute('BEGIN TRANSACTION')

        # Delete all records from both tables
        cursor.execute('DELETE FROM ingredients')
        cursor.execute('DELETE FROM recipes_images')

        # Reset the auto-increment counters
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="recipes_images"')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="ingredients"')

        cursor.execute('COMMIT')
        print("Successfully cleaned up the database!")

    except Exception as e:
        cursor.execute('ROLLBACK')
        print(f"Error during cleanup: {str(e)}")

    finally:
        db.close()


if __name__ == '__main__':
    cleanup_database()
