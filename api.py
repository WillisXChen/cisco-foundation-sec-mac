from chainlit.server import app as fastapi_app
from strawberry.fastapi import GraphQLRouter
from core.schema import schema
from core.logger import logger
from strawberry.subscriptions import GRAPHQL_TRANSPORT_WS_PROTOCOL, GRAPHQL_WS_PROTOCOL

# Include GraphQL Router with subscription protocols enabled
graphql_app = GraphQLRouter(
    schema,
    subscription_protocols=[
        GRAPHQL_TRANSPORT_WS_PROTOCOL,
        GRAPHQL_WS_PROTOCOL,
    ]
)
fastapi_app.include_router(graphql_app, prefix="/graphql")

@fastapi_app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Cisco Foundation Sec 8B API"}

logger.info("✅ FastAPI routes and GraphQL initialized.")
