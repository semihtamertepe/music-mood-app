import socket

def test_mqtt_connection(host="localhost", port=1883):
    s = socket.socket()
    try:
        s.settimeout(3)  # 3 saniyede timeout olsun
        s.connect((host, port))
        print(f"✅ {host}:{port} bağlantısı başarılı!")
    except Exception as e:
        print(f"❌ {host}:{port} bağlantı başarısız: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    test_mqtt_connection()
