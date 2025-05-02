from internal.database.clickhouse import ClickHouseDB

db = ClickHouseDB()

async def get_or_create_room(username1: str, username2: str):
    room_id = db.get_room_id(username1, username2)
    if room_id:
        return room_id
    else:
        return db.create_room(username1, username2)

async def get_users_by_room(room_id: str):
    return db.get_users_by_room(room_id)


