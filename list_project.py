import os

def list_relevant_files():
    with open('project_structure.txt', 'w') as f:
        f.write("=== Project Structure ===\n\n")
        
        relevant_extensions = {'.py', '.db', '.sqlite', '.sqlite3'}
        relevant_files = ['requirements.txt', 'README.md']
        
        for root, dirs, files in os.walk('.'):
            # Skip __pycache__ and virtual environment directories
            if '__pycache__' in root or 'venv' in root or '.git' in root:
                continue
                
            level = root.replace('.', '').count(os.sep)
            indent = '  ' * level
            
            for file in files:
                _, ext = os.path.splitext(file)
                if ext in relevant_extensions or file in relevant_files:
                    full_path = os.path.join(root, file)
                    f.write(f"{indent}{file}\n")
                    if file.endswith('.db'):
                        try:
                            size = os.path.getsize(full_path)
                            f.write(f"{indent}  Size: {size:,} bytes\n")
                        except:
                            f.write(f"{indent}  Could not get file size\n")
        
        f.write("\nFile created at: " + os.path.abspath('project_structure.txt'))

if __name__ == '__main__':
    list_relevant_files()
    print("Results written to project_structure.txt") 