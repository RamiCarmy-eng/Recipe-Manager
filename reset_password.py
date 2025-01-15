import json
import bcrypt
import os

def reset_manager_password():
    print("=== Password Reset Tool ===")
    
    # 1. Load current users
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
            print("Current users:", list(users.keys()))
    except Exception as e:
        print(f"Error loading users: {e}")
        return
    
    # 2. Create new password hash
    password = "password123"
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    # 3. Update manager user
    users['manager'] = {
        "password": hashed.decode('utf-8'),
        "role": "manager"
    }
    
    # 4. Save updated users
    try:
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)
        print("\nManager password updated successfully!")
    except Exception as e:
        print(f"Error saving users: {e}")
        return
    
    # 5. Verify the update
    try:
        with open('users.json', 'r') as f:
            saved_users = json.load(f)
            stored_hash = saved_users['manager']['password']
            
            # Test verification
            is_valid = bcrypt.checkpw(
                password.encode('utf-8'),
                stored_hash.encode('utf-8')
            )
            
            print("\nVerification test:")
            print(f"File path: {os.path.abspath('users.json')}")
            print(f"Password verification: {'SUCCESS' if is_valid else 'FAILED'}")
            print("\nYou can now log in with:")
            print("Username: manager")
            print("Password: password123")
    except Exception as e:
        print(f"Error verifying password: {e}")

if __name__ == "__main__":
    reset_manager_password()