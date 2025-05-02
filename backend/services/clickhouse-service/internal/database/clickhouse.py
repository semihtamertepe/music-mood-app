from clickhouse_driver import Client
import os

class ClickHouseDB:
    def __init__(self):
        self.client = Client(
            host=os.getenv('CLICKHOUSE_HOST', 'localhost'),
            port=int(os.getenv('CLICKHOUSE_PORT', 9000)),
            user=os.getenv('CLICKHOUSE_USER', 'default'),
            password=os.getenv('CLICKHOUSE_PASSWORD', '')
        )

    def create_database_and_tables(self):
        self.client.execute('CREATE DATABASE IF NOT EXISTS chat_service')

        self.client.execute('''
        CREATE TABLE IF NOT EXISTS chat_service.chat_messages
        (
            room_id String,
            sender String,
            receiver String,
            message String,
            timestamp String,
        )
        ENGINE = Kafka
        SETTINGS
            kafka_broker_list = 'kafka:9092',
            kafka_topic_list = 'chat-messages',
            kafka_group_name = 'chat-service',
            kafka_format = 'JSONEachRow',
            kafka_num_consumers = 1
        ''')

        self.client.execute('''
        CREATE TABLE IF NOT EXISTS chat_service.chat_messages_table
        (
            room_id String,
            sender String,
            receiver String,
            message String,
            timestamp String
        )
        ENGINE = MergeTree()
        ORDER BY (room_id, timestamp)
        ''')

        self.client.execute('''
        CREATE MATERIALIZED VIEW IF NOT EXISTS chat_service.chat_messages_mv
        TO chat_service.chat_messages_table
        AS
        SELECT *
        FROM chat_service.chat_messages
        ''')

        self.client.execute('''
        CREATE TABLE IF NOT EXISTS chat_service.rooms
        (
            room_id String,
            username1 String,
            username2 String
        )
        ENGINE = MergeTree()
        ORDER BY room_id
        ''')

    def get_room_id(self, username1, username2):
        usernames = sorted([username1, username2])
        query = """
        SELECT room_id FROM chat_service.rooms
        WHERE username1 = %(username1)s AND username2 = %(username2)s
        LIMIT 1
        """
        result = self.client.execute(query, {'username1': usernames[0], 'username2': usernames[1]})
        if result:
            return result[0][0]
        return None

    def create_room(self, username1, username2):
        usernames = sorted([username1, username2])
        room_id = f"{usernames[0]}_{usernames[1]}"
        self.client.execute("""
        INSERT INTO chat_service.rooms (room_id, username1, username2)
        VALUES (%(room_id)s, %(username1)s, %(username2)s)
        """, {'room_id': room_id, 'username1': usernames[0], 'username2': usernames[1]})
        return room_id
    
    def get_users_by_room(self, room_id):
        """
        Retrieve the two usernames associated with a room ID.
        
        Args:
            room_id (str): The room ID to look up.
            
        Returns:
            tuple: (username1, username2) if the room exists, None otherwise.
        """
        query = """
        SELECT username1, username2 FROM chat_service.rooms
        WHERE room_id = %(room_id)s
        LIMIT 1
        """
        result = self.client.execute(query, {'room_id': room_id})
        return result[0] if result else None
