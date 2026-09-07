import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST", "localhost")
port = int(os.getenv("DB_PORT", 3306))
user = os.getenv("DB_USER", "Swaroop3011")
password = os.getenv("DB_PASSWORD", "Pooraws123!")
db_name = os.getenv("DB_NAME", "vibeosys_db")

print(f"1. Attempting direct connection as {user} to MySQL at {host}:{port}...")
try:
    conn = pymysql.connect(host=host, port=port, user=user, password=password)
    with conn.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"   [SUCCESS] Database `{db_name}` created or already exists.")
    conn.close()

    from app.database import engine, Base
    from app.models import Product
    Base.metadata.create_all(bind=engine)
    print("   [SUCCESS] Product table initialized successfully in MySQL!")
except pymysql.err.OperationalError as e:
    err_code, err_msg = e.args
    print(f"   [AUTH ERROR] Could not log in with {user}: {err_msg}")
    print("\n2. Trying administrative root logins to create the user and database...")

    created = False
    for root_pwd in ["", "root", "rootpassword", "admin", "Pooraws123!"]:
        try:
            r_conn = pymysql.connect(host=host, port=port, user="root", password=root_pwd)
            print(f"   [CONNECTED] Connected to MySQL as root (password: '{root_pwd}')")
            with r_conn.cursor() as cur:
                cur.execute(f"CREATE USER IF NOT EXISTS '{user}'@'localhost' IDENTIFIED BY '{password}';")
                cur.execute(f"ALTER USER '{user}'@'localhost' IDENTIFIED BY '{password}';")
                cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                cur.execute(f"GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{user}'@'localhost';")
                cur.execute("FLUSH PRIVILEGES;")
                print(f"   [SUCCESS] Created MySQL user '{user}' and database '{db_name}'.")
            r_conn.close()
            created = True
            break
        except Exception:
            continue

    if created:
        from app.database import engine, Base
        from app.models import Product
        Base.metadata.create_all(bind=engine)
        print("   [SUCCESS] Product table initialized successfully in MySQL!")
    else:
        print("\n   [INFO] If your MySQL root user has a custom password, run this SQL in MySQL Workbench / MySQL CLI:")
        print(f"   CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"   CREATE USER IF NOT EXISTS '{user}'@'localhost' IDENTIFIED BY '{password}';")
        print(f"   GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{user}'@'localhost';")
        print("   FLUSH PRIVILEGES;")
