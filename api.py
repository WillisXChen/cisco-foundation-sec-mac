from chainlit.server import app as fastapi_app
from strawberry.fastapi import GraphQLRouter
from core.schema import schema
from core.logger import logger

# Include GraphQL Router
fastapi_app.include_router(GraphQLRouter(schema), prefix="/graphql")

@fastapi_app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Cisco Foundation Sec 8B API"}

logger.info("✅ FastAPI routes and GraphQL initialized.")
