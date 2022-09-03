import asyncio
from pyrogram import Client
import database


async def main():
	api_id = 13671196
	api_hash = "db08bc60a8e5e6fb2927d192df4f30c0"

	app = Client("my_account", api_id=api_id, api_hash=api_hash)
	app.start()
	entities = database.get_entities()
	for entity in entities:
		messages = database.get_chat_messages(entity)
		for message in messages:
			async with app:
				message_tm = await app.get_messages(chat_id=entity.username, message_ids=message.message_id)
			
			if (hasattr(message, 'reactions') and message.reactions):
				print(str((message_tm.reactions.reactions)))
				database.save_reactions(message, message_tm.reactions.reactions)
	app.stop()

asyncio.run(main())




