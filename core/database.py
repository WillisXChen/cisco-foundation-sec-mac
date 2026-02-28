import os
import json
import asyncio
from qdrant_client import QdrantClient
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
import requests

class VectorDBManager:
    """Manages Qdrant vector database connection and ingestion."""
    def __init__(self, url: str = "http://localhost:6333"):
        self.url = url
        self.client = QdrantClient(url=self.url)
        self.collection_name = "security_playbooks"

    def setup_model(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.client.set_model(model_name)

    def is_collection_exists(self) -> bool:
        collections = self.client.get_collections()
        return any(c.name == self.collection_name for c in collections.collections)

    def ingest_playbooks(self, playbooks_path: str):
        """Loads and ingests playbooks from JSON file."""
        if not os.path.exists(playbooks_path):
            return False
            
        with open(playbooks_path, "r", encoding="utf-8") as f:
            docs_data = json.load(f)
            docs = [d["content"] for d in docs_data]
            metadatas = [{"title": d["title"]} for d in docs_data]
            ids = [d["id"] for d in docs_data]
            
            self.client.add(
                collection_name=self.collection_name,
                documents=docs,
                metadata=metadatas,
                ids=ids
            )
        return True

    def query_context(self, query_text: str, limit: int = 1) -> str:
        """Queries the vector database for relevant context based on user input."""
        try:
            search_result = self.client.query(
                collection_name=self.collection_name,
                query_text=query_text,
                limit=limit
            )
            if search_result:
                best_match = search_result[0]
                return f"[Internal System Context]\n{best_match.document}\n\n"
        except Exception as e:
            print(f"[RAG Error] {e}")
        return ""

class MetricsDBManager:
    """Manages InfluxDB metrics connection and ingestion."""
    def __init__(self, url: str, token: str, org: str, bucket: str):
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_hardware_stats(self, stats: dict):
        """Writes hardware statistics point to InfluxDB."""
        try:
            p = Point("hardware_monitor") \
                .tag("host", "mac_server") \
                .tag("chip", stats.get("chip_label", "Unknown")) \
                .field("e_cpu_pct", float(stats.get("e_cpu_pct", 0))) \
                .field("p_cpu_pct", float(stats.get("p_cpu_pct", 0))) \
                .field("gpu_pct", float(stats.get("gpu_pct", 0))) \
                .field("ram_pct", float(stats.get("ram_pct", 0))) \
                .field("ram_used_gb", float(stats.get("ram_used_gb", 0))) \
                .field("cpu_power_w", float(stats.get("cpu_power_w", 0))) \
                .field("gpu_power_w", float(stats.get("gpu_power_w", 0))) \
                .field("total_power_w", float(stats.get("total_power_w", 0)))
            self.write_api.write(bucket=self.bucket, org=self.org, record=p)
        except Exception as e:
            print(f"InfluxDB Write Error: {e}")

    def query_hardware_history_df(self) -> pd.DataFrame:
        """Queries the last 15 minutes of hardware data."""
        headers = {"Authorization": f"Token {self.token}"}
        params = {
            "db": self.bucket,
            "q": "SELECT * FROM hardware_monitor WHERE time >= now() - 15m"
        }
        res = requests.get(f"{self.url}/query", headers=headers, params=params)
        res.raise_for_status()
        
        res_json = res.json()
        results = res_json.get("results", [])
        if not results or "series" not in results[0]:
            return pd.DataFrame()

        series = results[0]["series"][0]
        columns = series["columns"]
        values = series["values"]
        df = pd.DataFrame(values, columns=columns)
        
        if 'time' in df.columns:
            df['_time'] = pd.to_datetime(df['time'])
            
        return df
