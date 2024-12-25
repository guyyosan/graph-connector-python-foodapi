import asyncio
import logging
import httpx
from datetime import datetime, timezone
from typing import Generator, List
from msgraph.generated.models.external_connectors.access_type import AccessType
from msgraph.generated.models.external_connectors.acl import Acl
from msgraph.generated.models.external_connectors.acl_type import AclType
from msgraph.generated.models.external_connectors.external_activity import (
    ExternalActivity,
)
from msgraph.generated.models.external_connectors.external_activity_type import (
    ExternalActivityType,
)
from msgraph.generated.models.external_connectors.external_item import ExternalItem
from msgraph.generated.models.external_connectors.external_item_content import (
    ExternalItemContent,
)
from msgraph.generated.models.external_connectors.external_item_content_type import (
    ExternalItemContentType,
)
from msgraph.generated.models.external_connectors.identity import Identity
from msgraph.generated.models.external_connectors.identity_type import IdentityType
from msgraph.generated.models.external_connectors.properties import Properties

from connection_configuration import external_connection, user_id
from graph_service import graph_client

logging.basicConfig()
logger = logging.getLogger(__name__)

async def _fetch_data() -> List[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://world.openfoodfacts.net/cgi/search.pl",
            params={
                "action": "process",
                "page_size": 100,
                "json": True,
            },
        )
        response.raise_for_status()
        data = response.json()
        print(data.get("products", [])) 
        return data.get("products", [])
        

async def _extract() -> List[dict]:
    return await _fetch_data()

def _transform(content: List[dict]) -> Generator[ExternalItem, None, None]:
    local_time_with_timezone = datetime.now().astimezone()
    for item in content:
        product_id = item.get("id") or item.get("_id") or item.get("code")
        if not product_id:
            continue
        
        date_str = local_time_with_timezone.isoformat()

        yield ExternalItem(
            id=str(product_id),
            properties=Properties(
                additional_data={
                    "title": item.get("product_name", ""),
                    "excerpt": item.get("generic_name", ""),
                    "imageUrl": item.get("image_url", ""),
                    "url": item.get("url", ""),
                    "date": date_str,  # Ensure the date is in ISO 8601 format with timezone
                    "tags@odata.type": "Collection(String)",
                    "tags": item.get("categories_tags", []),
                }
            ),
            content=ExternalItemContent(
                type=ExternalItemContentType.Text,
                value=item.get("ingredients_text", ""),
            ),
            acl=[
                Acl(
                    type=AclType.Everyone,
                    value="everyone",
                    access_type=AccessType.Grant,
                )
            ],
            activities=[
                ExternalActivity(
                    odata_type="#microsoft.graph.externalConnectors.externalActivity",
                    type=ExternalActivityType.Created,
                    start_date_time=local_time_with_timezone.replace(
                        tzinfo=local_time_with_timezone.tzinfo
                    ),
                    performed_by=Identity(type=IdentityType.User, id=user_id),
                )
            ],
        )

async def _load(content: Generator[ExternalItem, None, None]):
    for doc in content:
        try:
            if external_connection.id is not None:
                await graph_client.external.connections.by_external_connection_id(
                    external_connection.id
                ).items.by_external_item_id(str(doc.id)).put(doc)
                logger.info(f"Loaded document {doc.id}")
            else:
                logger.error("external_connection.id is None, cannot load document")
        except Exception as e:
            logger.error(f"Error loading document {doc.id}: {e}")

async def load_content():
    content = await _extract()
    transformed = _transform(content)
    await _load(transformed)