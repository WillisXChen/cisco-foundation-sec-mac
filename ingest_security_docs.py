import os
from qdrant_client import QdrantClient

def main():
    # Initialize Qdrant Client to point to our local docker service
    # The Qdrant service is exposed on localhost:6333 by docker-compose
    client = QdrantClient(url="http://localhost:6333")

    # Define the collection name
    COLLECTION_NAME = "security_playbooks"

    # Initialize fastembed in Qdrant (this will download the local embedding model)
    print("Setting up embedding model...")
    client.set_model("BAAI/bge-small-en-v1.5")

    # Sample internal security SOPs/Playbooks
    documents = [
        {
            "id": 1,
            "title": "Handling config.php.bak scans",
            "content": "If a user or IP is repeatedly scanning for config.php.bak, backup.zip, or similar backup files, it indicates a directory traversal or backup file exposure attack. Action: Immediately block the IP at the WAF level and investigate if any backup files are actually exposed on the server."
        },
        {
            "id": 2,
            "title": "Recurring Nginx 404s",
            "content": "A high volume of Nginx 404 errors for hidden files (e.g., .env, .git/config) signifies an automated vulnerability scanner. Action: Temporarily ban the IP using fail2ban and enable rate limiting for 404 responses."
        },
        {
            "id": 3,
            "title": "SSH Brute Force",
            "content": "Multiple failed SSH login attempts for users like root or admin. Action: Ensure password authentication is disabled, rely on SSH keys only, and verify fail2ban is monitoring port 22."
        },
        {
            "id": 4,
            "title": "SQL Injection Attempts",
            "content": "Logs containing keywords like UNION SELECT, OR 1=1, or unexpected quotation marks in URL parameters. Action: Validate input sanitization on the application end and update WAF rules to block common SQLi payloads."
        }
    ]

    print(f"Adding {len(documents)} documents to Qdrant collection '{COLLECTION_NAME}'...")

    docs = [doc["content"] for doc in documents]
    metadata = [{"title": doc["title"]} for doc in documents]
    ids = [doc["id"] for doc in documents]

    # Qdrant client's `add` method simplifies the process of embedding and indexing
    client.add(
        collection_name=COLLECTION_NAME,
        documents=docs,
        metadata=metadata,
        ids=ids
    )

    print("Ingestion complete! Data is ready for RAG.")

if __name__ == "__main__":
    main()
