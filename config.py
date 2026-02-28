# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MySQL Configuration - UPDATE THESE WITH YOUR ACTUAL CREDENTIALS
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'  # CHANGE THIS TO YOUR ACTUAL MYSQL PASSWORD
    MYSQL_DB = 'ecommerce_db'
    
    # Connection URI
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # This will log SQL queries to help debug
    
    # MongoDB Configuration
    MONGO_URI = 'mongodb://localhost:27017/ecommerce_logs'