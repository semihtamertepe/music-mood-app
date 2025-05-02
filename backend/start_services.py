import subprocess
import time
import os
import signal
from pathlib import Path
from typing import List

def start_service(service_name: str, port: int) -> subprocess.Popen:
    service_path = Path(f"services/{service_name}")
    env_file = service_path / ".env"
    
    # Environment variables'i yükle
    env = os.environ.copy()
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env[key] = value

    # Log dosyalarını hazırla
    log_dir = service_path / "logs"
    log_dir.mkdir(exist_ok=True)
    stdout_log = log_dir / "stdout.log"
    stderr_log = log_dir / "stderr.log"

    # Servisi başlat
    cmd = [
        "uvicorn",
        "main:app",
        "--host", "0.0.0.0",
        "--port", str(port),
        "--log-level", "debug"
    ]
    
    with open(stdout_log, "w") as out, open(stderr_log, "w") as err:
        process = subprocess.Popen(
            cmd,
            cwd=str(service_path),
            env=env,
            stdout=out,
            stderr=err,
            start_new_session=True  # Yeni process grubu oluştur
        )
    
    print(f"🚀 {service_name} started (PID: {process.pid})")
    return process

def stop_services(processes: List[subprocess.Popen]):
    print("\n🛑 Stopping all services...")
    for process in processes:
        try:
            # Process grubunu sonlandır
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass
    print("✅ All services stopped")

def main():
    services = [
        ("api-gateway-service", 8000),
        ("auth-service", 8001),
        #("chat-service", 8002),
        ("translation-service", 8003),
        #("clickhouse-service", 8005),
        ("music-recommendation-service", 8006)
    ]
    
    processes = []
    
    try:
        print("🌟 Starting all services...\n")
        for service_name, port in services:
            print(f"⚡ Starting {service_name} on port {port}...")
            process = start_service(service_name, port)
            processes.append(process)
            time.sleep(1)  # Servisler arası kısa bekleme

        print("\n✅ All services running! Press CTRL+C to stop")
        print(f"📋 Running PIDs: {[p.pid for p in processes]}")
        
        # Ana prosesi aktif tut
        while True:
            time.sleep(3600)  # Uzun bekleme
            
    except KeyboardInterrupt:
        stop_services(processes)
    except Exception as e:
        print(f"❌ Critical error: {str(e)}")
        stop_services(processes)

if __name__ == "__main__":
    main()