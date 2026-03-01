from chainlit.server import app as fastapi_app
from strawberry.fastapi import GraphQLRouter
from core.schema import schema
from core.logger import logger
from strawberry.subscriptions import GRAPHQL_TRANSPORT_WS_PROTOCOL, GRAPHQL_WS_PROTOCOL
from core.i18n import _t

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

# Fix for Chainlit shadowing our routes: ensure the rule is at the front
health_route = fastapi_app.routes.pop()
fastapi_app.routes.insert(0, health_route)

@fastapi_app.get("/api/translations")
async def get_translations(lang: str = "zh-TW"):
    keys = [
        "History", 
        "PerfMon", 
        "Type your message here...", 
        "Help", 
        "New Chat", 
        "Chat Settings",
        "LLMs can make mistakes. Please verify important info."
    ]
    return {k: _t(k, lang=lang) for k in keys}

# Make sure the translations route is also at the front
trans_route = fastapi_app.routes.pop()
fastapi_app.routes.insert(0, trans_route)

logger.info("✅ FastAPI routes and GraphQL initialized.")
