import asyncio
from pyrogram import Client
import database


async def main():
	api = None
	with open("config.json") as jsonfile:
		api = json.load(jsonfile)['telegram']

	app = Client("my_account", api_id=api['id'], api_hash=api['hash'])
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




