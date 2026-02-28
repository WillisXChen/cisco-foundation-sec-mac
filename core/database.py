import os
import json
import asyncio
from qdrant_client import QdrantClient
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
import requests
from core.config import QDRANT_COLLECTION
from core.logger import logger

class VectorDBManager:
    """Manages Qdrant vector database connection and ingestion."""
    def __init__(self, url: str = "http://localhost:6333"):
        self.url = url
        self.client = QdrantClient(url=self.url)
        self.collection_name = QDRANT_COLLECTION

    def setup_model(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        logger.info(f"Setting up embedding model: {model_name}")
        self.client.set_model(model_name)

    def is_collection_exists(self) -> bool:
        try:
            collections = self.client.get_collections()
            return any(c.name == self.collection_name for c in collections.collections)
        except Exception as e:
            logger.error(f"Error checking Qdrant collection: {e}")
            return False

    def ingest_playbooks(self, playbooks_path: str):
        """Loads and ingests playbooks from JSON file."""
        if not os.path.exists(playbooks_path):
            logger.warning(f"Playbooks file not found: {playbooks_path}")
            return False
            
        try:
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
            logger.info(f"Successfully ingested {len(docs)} playbooks into {self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"Ingestion error: {e}")
            return False

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
                logger.info("Found relevant context in VectorDB.")
                return f"[Internal System Context]\n{best_match.document}\n\n"
        except Exception as e:
            logger.error(f"[RAG Error] {e}")
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
            logger.error(f"InfluxDB Write Error: {e}")

    def query_hardware_history_df(self) -> pd.DataFrame:
        """Queries the last 15 minutes of hardware data."""
        headers = {"Authorization": f"Token {self.token}"}
        params = {
            "db": self.bucket,
            "q": "SELECT * FROM hardware_monitor WHERE time >= now() - 15m"
        }
        try:
            res = requests.get(f"{self.url}/query", headers=headers, params=params, timeout=5)
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
        except Exception as e:
            logger.error(f"InfluxDB Query Error: {e}")
            return pd.DataFrame()
