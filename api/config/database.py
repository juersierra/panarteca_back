__all__: list[str] = ["db", "COLLECTIONS"]

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from .__base_config import MONGODB_URI, logger

COLLECTIONS = ["artworks", "artists", "orders", "users"]

client = MongoClient(MONGODB_URI, server_api=ServerApi("1"))

try:
    client.admin.command("ping")
    logger.info("Pinged your deployment. You successfully connected MongoDB")
except Exception as e:
    print(e)

# db: Database[Any] -> invalidType pero usado por el profe ??
db = client.panarteca


def create_collections() -> None:
    logger.warn("")
    logger.info("Initializing collections")
    for collection in COLLECTIONS:
        if collection not in db.list_collection_names():
            db.create_collection(collection)
            logger.warn(f"Collection '{collection}' created")
        else:
            logger.info(f"Collection '{collection}' already exists")
    logger.warn("")


# Create Collections (optional)
# create_collections()
