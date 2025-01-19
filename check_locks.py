import psutil
import os

def find_process_locking_file(filepath):
    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            files = proc.info['open_files']
            if files:
                for file in files:
                    if filepath in str(file):
                        return proc.info
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None

if __name__ == '__main__':
    db_path = os.path.abspath('instance/recipes.db')
    print(f"Looking for processes locking: {db_path}")
    
    process = find_process_locking_file(db_path)
    if process:
        print(f"Found process locking the database:")
        print(f"PID: {process['pid']}")
        print(f"Name: {process['name']}")
    else:
        print("No process found locking the database") 