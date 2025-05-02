from internal.database.clickhouse import ClickHouseDB

db = ClickHouseDB()

async def get_messages_by_room(room_id: str, limit: int = 50, offset: int = 0):
    query = f"""
    SELECT sender, receiver, message, timestamp
    FROM chat_service.chat_messages_table
    WHERE room_id = %(room_id)s
    ORDER BY timestamp ASC
    LIMIT {limit} OFFSET {offset}
    """
    results = db.client.execute(query, {'room_id': room_id})
    
    messages = []
    for sender, receiver, message, timestamp in results:
        messages.append({
            "sender": sender,
            "receiver": receiver,
            "message": message,
            "timestamp": timestamp  # zaten string
        })
    
    return messages
