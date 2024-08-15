from pyodmongo import AsyncDbEngine
from datetime import timezone, timedelta


tz_info = timezone(timedelta(hours=-3))
engine = AsyncDbEngine(
    mongo_uri="mongodb://localhost:27017/", db_name="todo-app", tz_info=tz_info
)
