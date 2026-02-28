# models/mongo_models.py
from flask_pymongo import PyMongo
from datetime import datetime

# Create mongo object without importing app
mongo = PyMongo()

class ActivityLog:
    collection_name = 'activity_logs'
    
    @classmethod
    def get_collection(cls):
        return mongo.db[cls.collection_name]
    
    @classmethod
    def log_action(cls, user_id=None, action=None, details=None):
        """Log an action to MongoDB"""
        collection = cls.get_collection()
        log_entry = {
            'user_id': user_id,
            'action': action,
            'details': details,
            'timestamp': datetime.utcnow()
        }
        
        # Insert into MongoDB
        result = collection.insert_one(log_entry)
        return result
    
    @classmethod
    def get_user_activity(cls, user_id, limit=50):
        """Get activity logs for a specific user"""
        collection = cls.get_collection()
        return list(collection.find({'user_id': user_id}).sort('timestamp', -1).limit(limit))
    
    @classmethod
    def get_recent_activities(cls, limit=100, filter_query=None):
        """Get most recent activities with optional filters"""
        collection = cls.get_collection()
        query = filter_query or {}
        return list(collection.find(query).sort('timestamp', -1).limit(limit))
    
    @classmethod
    def get_stats(cls):
        """Get statistics about logs"""
        collection = cls.get_collection()
        pipeline = [
            {
                '$group': {
                    '_id': '$action',
                    'count': {'$sum': 1},
                    'last_occurrence': {'$max': '$timestamp'}
                }
            },
            {'$sort': {'count': -1}}
        ]
        
        return list(collection.aggregate(pipeline))