import os

print("\nCurrent working directory:", os.getcwd())
print("\nLooking for recipes.db...")

# Look in current directory and subdirectories
for root, dirs, files in os.walk('.'):
    if 'recipes.db' in files:
        print(f"Found recipes.db in: {root}")
        full_path = os.path.join(root, 'recipes.db')
        print(f"Full path: {full_path}")
        print(f"File size: {os.path.getsize(full_path)} bytes") 