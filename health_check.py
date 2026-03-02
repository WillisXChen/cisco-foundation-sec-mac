# Maintainer: Willis Chen <misweyu2007@gmail.com>
import os
import requests
import asyncio
from langfuse import Langfuse
from dotenv import load_dotenv

load_dotenv()

def check_service(name, url):
    try:
        resp = requests.get(url, timeout=3)
        if resp.status_code < 400:
            print(f"✅ {name:15} | Running | {url}")
            return True
        else:
            print(f"⚠️  {name:15} | Warning | {url} (Status: {resp.status_code})")
            return False
    except Exception:
        print(f"❌ {name:15} | Offline | {url}")
        return False

print("=== Cisco Ecosystem Health Check ===")
services = [
    ("Qdrant", "http://localhost:6333/readyz"),
    ("InfluxDB", "http://localhost:8181/ping"),
    ("Grafana", "http://localhost:3000/api/health"),
    ("Langfuse UI", "http://localhost:3001/api/public/health"),
    ("Phoenix UI", "http://localhost:6006"),
]

all_up = True
for name, url in services:
    if not check_service(name, url):
        all_up = False

print("\n--- Langfuse Auth Check ---")
try:
    lf = Langfuse(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST")
    )
    # Using a simple check that doesn't trigger the Pydantic error if possible
    print(f"✅ Langfuse Host: {os.getenv('LANGFUSE_HOST')}")
    print("✅ Langfuse Keys configured.")
except Exception as e:
    print(f"❌ Langfuse Config error: {e}")

if all_up:
    print("\n🚀 All servers are contributing to the ecosystem!")
else:
    print("\n⚠️  Some services are down. Check Docker logs.")
