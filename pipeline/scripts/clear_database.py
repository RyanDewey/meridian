from utils.run_sql import run_sql_file
import os

# Script clears the database data
def clear_database():
    DIR = "../database"
    file = "clearData.sql"
    full = os.path.join(DIR, file)
    run_sql_file(full)
    print("Data cleared")

if __name__ == "__main__":
    clear_database()