# In Python console or script
from werkzeug.security import generate_password_hash, check_password_hash

# Generate a new password hash
password = 'admin123'
hashed = generate_password_hash(password)
print(f"Hashed password: {hashed}")

# Verify it works
print(check_password_hash(hashed, 'admin123'))  # Should print True