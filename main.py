import asyncio
from args import args
from connection_service import create_connection
from content_service import load_content, _fetch_data

if args.subcommand == "test":
    asyncio.run(_fetch_data())
if args.subcommand == "create-connection":
    asyncio.run(create_connection())
elif args.subcommand == "load-content":
    asyncio.run(load_content())
