import shutil
import datetime

def backup_database():
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    shutil.copy("flight_data.db", f"backup_{now}.db")
    return True
