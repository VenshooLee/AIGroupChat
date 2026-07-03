from datetime import datetime, timezone, timedelta
import os
import json
import uuid

# 北京时区 (UTC+8)
BEIJING_TZ = timezone(timedelta(hours=8))

def get_local_now():
    """获取北京时间"""
    return datetime.now(BEIJING_TZ)

# 使用 TinyDB 作为嵌入式数据库，无需安装 MongoDB
try:
    from tinydb import TinyDB, Query
    HAS_TINYDB = True
except ImportError:
    HAS_TINYDB = False

class Database:
    """嵌入式数据库，使用 JSON 文件存储"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def init_app(self, app):
        # 数据存储目录
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(data_dir, exist_ok=True)

        self._db_path = os.path.join(data_dir, 'groupchat.json')

        if HAS_TINYDB:
            self._db = TinyDB(self._db_path)
        else:
            # 纯 Python 实现的简单 JSON 数据库
            self._db = JsonDB(self._db_path)

    @property
    def db(self):
        return self._db

    @property
    def conversations(self):
        return self._db.table('conversations')

    @property
    def documents(self):
        return self._db.table('documents')

    @property
    def settings(self):
        return self._db.table('settings')


class JsonDbTable:
    """简单的 JSON 数据库表实现"""
    def __init__(self, db_path, table_name):
        self._db_path = db_path
        self._table_name = table_name
        self._data = self._load()

    def _load(self):
        if os.path.exists(self._db_path):
            try:
                with open(self._db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get(self._table_name, [])
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save(self):
        # 读取现有数据
        if os.path.exists(self._db_path):
            try:
                with open(self._db_path, 'r', encoding='utf-8') as f:
                    all_data = json.load(f)
            except (json.JSONDecodeError, IOError):
                all_data = {}
        else:
            all_data = {}

        all_data[self._table_name] = self._data

        with open(self._db_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2, default=str)

    def insert(self, doc):
        if '_id' not in doc:
            doc['_id'] = str(uuid.uuid4())
        self._data.append(doc)
        self._save()
        return doc

    def all(self):
        return self._data

    def find(self, cond=None):
        if cond is None:
            return self._data
        results = []
        for doc in self._data:
            match = True
            for key, value in cond.items():
                if doc.get(key) != value:
                    match = False
                    break
            if match:
                results.append(doc)
        return results

    def find_one(self, cond=None):
        for doc in self.find(cond):
            return doc
        return None

    def update(self, updates, cond=None):
        count = 0
        for doc in self._data:
            match = True
            if cond:
                for key, value in cond.items():
                    if doc.get(key) != value:
                        match = False
                        break
            if match:
                doc.update(updates)
                count += 1
        if count > 0:
            self._save()
        return count

    def remove(self, cond=None):
        if cond is None:
            count = len(self._data)
            self._data = []
        else:
            count = 0
            new_data = []
            for doc in self._data:
                match = True
                for key, value in cond.items():
                    if doc.get(key) != value:
                        match = False
                        break
                if not match:
                    new_data.append(doc)
                else:
                    count += 1
            self._data = new_data
        if count > 0:
            self._save()
        return count


class JsonDB:
    """简单的 JSON 数据库"""
    def __init__(self, db_path):
        self._db_path = db_path
        self._tables = {}

    def table(self, name):
        if name not in self._tables:
            self._tables[name] = JsonDbTable(self._db_path, name)
        return self._tables[name]


class ConversationModel:
    def __init__(self, db):
        self.collection = db.conversations

    def create(self, title="New Conversation"):
        doc = {
            "title": title,
            "created_at": get_local_now().isoformat(),
            "updated_at": get_local_now().isoformat(),
            "messages": []
        }
        result = self.collection.insert(doc)
        return result['_id']

    def get_all(self):
        docs = self.collection.all()
        # 按 updated_at 降序排序
        docs.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
        return [self._serialize(doc) for doc in docs]

    def get_by_id(self, id):
        doc = self.collection.find_one({'_id': id})
        return self._serialize(doc) if doc else None

    def add_message(self, id, model, role, content):
        message = {
            "id": f"{get_local_now().timestamp()}",
            "model": model,
            "role": role,
            "content": content,
            "timestamp": get_local_now().isoformat()
        }
        doc = self.collection.find_one({'_id': id})
        if doc:
            messages = doc.get('messages', [])
            messages.append(message)
            self.collection.update({
                "messages": messages,
                "updated_at": get_local_now().isoformat()
            }, {"_id": id})
        return message

    def delete_message(self, id, message_id):
        doc = self.collection.find_one({'_id': id})
        if doc:
            messages = [m for m in doc.get('messages', []) if m.get('id') != message_id]
            self.collection.update({"messages": messages}, {"_id": id})

    def delete(self, id):
        self.collection.remove({'_id': id})
    
    def delete_all(self):
        self.collection.remove({})

    def _serialize(self, doc):
        if not doc:
            return None
        return doc


class DocumentModel:
    def __init__(self, db):
        self.collection = db.documents

    def create(self, title="Untitled Document", content=""):
        doc = {
            "title": title,
            "content": content,
            "created_at": get_local_now().isoformat(),
            "updated_at": get_local_now().isoformat()
        }
        result = self.collection.insert(doc)
        return result['_id']

    def get_all(self):
        docs = self.collection.all()
        docs.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
        return [self._serialize(doc) for doc in docs]

    def get_by_id(self, id):
        doc = self.collection.find_one({'_id': id})
        return self._serialize(doc) if doc else None

    def update(self, id, title=None, content=None):
        update = {"updated_at": get_local_now().isoformat()}
        if title is not None:
            update["title"] = title
        if content is not None:
            update["content"] = content
        self.collection.update(update, {"_id": id})

    def delete(self, id):
        self.collection.remove({'_id': id})

    def _serialize(self, doc):
        if not doc:
            return None
        return doc


class SettingsModel:
    def __init__(self, db):
        self.collection = db.settings

    def get(self):
        doc = self.collection.find_one()
        return doc if doc else {}

    def update(self, api_keys=None, enabled_models=None, mongodb_uri=None):
        update = {}
        if api_keys is not None:
            update["api_keys"] = api_keys
        if enabled_models is not None:
            update["enabled_models"] = enabled_models
        if mongodb_uri is not None:
            update["mongodb_uri"] = mongodb_uri

        if self.collection.find_one():
            # JsonDbTable doesn't support $set, use plain update
            self.collection.update(update, {})
        else:
            update["api_keys"] = api_keys or {}
            update["enabled_models"] = enabled_models or []
            self.collection.insert(update)
