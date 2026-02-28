# test_db.py
import pymysql
from config import Config

def test_mysql_connection():
    try:
        # Test connection
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        
        with connection.cursor() as cursor:
            # Check if tables exist
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("Tables in database:")
            for table in tables:
                print(f"  - {table[0]}")
            
            # Check users
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"\nUsers count: {user_count}")
            
            if user_count > 0:
                cursor.execute("SELECT id, username, email, full_name FROM users LIMIT 5")
                users = cursor.fetchall()
                print("Sample users:")
                for user in users:
                    print(f"  ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Name: {user[3]}")
            
            # Check products
            cursor.execute("SELECT COUNT(*) FROM products")
            product_count = cursor.fetchone()[0]
            print(f"\nProducts count: {product_count}")
            
            if product_count > 0:
                cursor.execute("SELECT id, name, price FROM products LIMIT 5")
                products = cursor.fetchall()
                print("Sample products:")
                for product in products:
                    print(f"  ID: {product[0]}, Name: {product[1]}, Price: ${product[2]}")
        
        connection.close()
        print("\n✅ MySQL connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        return False

if __name__ == "__main__":
    test_mysql_connection()