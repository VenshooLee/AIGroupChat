from datetime import datetime, timezone, timedelta
import os
import json
import uuid

# 北京时区 (UTC+8)
BEIJING_TZ = timezone(timedelta(hours=8))

def get_local_now():
    """获取北京时间"""
    return datetime.now(BEIJING_TZ)

# MongoDB support
try:
    from pymongo import MongoClient
    HAS_PYMONGO = True
except ImportError:
    HAS_PYMONGO = False

class Database:
    """MongoDB 数据库"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def init_app(self, app):
        # 从环境变量或设置获取 MongoDB URI
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
        db_name = os.environ.get('MONGO_DB', 'groupchat_db')
        
        self._client = MongoClient(mongo_uri)
        self._db = self._client[db_name]

    @property
    def conversations(self):
        return self._db.conversations

    @property
    def documents(self):
        return self._db.documents

    @property
    def settings(self):
        return self._db.settings


class ConversationModel:
    def __init__(self, db):
        self.collection = db.conversations

    def create(self, title="New Conversation"):
        doc = {
            "_id": str(uuid.uuid4()),
            "title": title,
            "created_at": get_local_now().isoformat(),
            "updated_at": get_local_now().isoformat(),
            "messages": []
        }
        result = self.collection.insert_one(doc)
        return doc["_id"]

    def get_all(self):
        docs = list(self.collection.find().sort("updated_at", -1))
        return [self._serialize(doc) for doc in docs]

    def get_by_id(self, id):
        doc = self.collection.find_one({"_id": id})
        return self._serialize(doc) if doc else None

    def add_message(self, id, model, role, content):
        message = {
            "id": f"{get_local_now().timestamp()}",
            "model": model,
            "role": role,
            "content": content,
            "timestamp": get_local_now().isoformat()
        }
        self.collection.update_one(
            {"_id": id},
            {
                "$push": {"messages": message},
                "$set": {"updated_at": get_local_now().isoformat()}
            }
        )
        return message

    def delete_message(self, id, message_id):
        self.collection.update_one(
            {"_id": id},
            {"$pull": {"messages": {"id": message_id}}}
        )

    def delete(self, id):
        self.collection.delete_one({"_id": id})
    
    def delete_all(self):
        self.collection.delete_many({})

    def _serialize(self, doc):
        if not doc:
            return None
        doc["id"] = doc.pop("_id")  # 将 _id 转换为 id
        return doc


class DocumentModel:
    def __init__(self, db):
        self.collection = db.documents

    def create(self, title="Untitled Document", content=""):
        doc = {
            "_id": str(uuid.uuid4()),
            "title": title,
            "content": content,
            "created_at": get_local_now().isoformat(),
            "updated_at": get_local_now().isoformat()
        }
        self.collection.insert_one(doc)
        return doc["_id"]

    def get_all(self):
        docs = list(self.collection.find().sort("updated_at", -1))
        return [self._serialize(doc) for doc in docs]

    def get_by_id(self, id):
        doc = self.collection.find_one({"_id": id})
        return self._serialize(doc) if doc else None

    def update(self, id, title=None, content=None):
        update = {"updated_at": get_local_now().isoformat()}
        if title is not None:
            update["title"] = title
        if content is not None:
            update["content"] = content
        self.collection.update_one({"_id": id}, {"$set": update})

    def delete(self, id):
        self.collection.delete_one({"_id": id})

    def _serialize(self, doc):
        if not doc:
            return None
        doc["id"] = doc.pop("_id")
        return doc


class SettingsModel:
    def __init__(self, db):
        self.collection = db.settings

    def get(self):
        doc = self.collection.find_one()
        return self._serialize(doc) if doc else {}

    def update(self, api_keys=None, enabled_models=None, mongodb_uri=None):
        update = {}
        if api_keys is not None:
            update["api_keys"] = api_keys
        if enabled_models is not None:
            update["enabled_models"] = enabled_models
        if mongodb_uri is not None:
            update["mongodb_uri"] = mongodb_uri

        if self.collection.find_one():
            self.collection.update_one({}, {"$set": update})
        else:
            update["api_keys"] = api_keys or {}
            update["enabled_models"] = enabled_models or []
            self.collection.insert_one(update)

    def _serialize(self, doc):
        if not doc:
            return None
        doc["id"] = doc.pop("_id")
        return doc
