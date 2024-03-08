from pyrogram import Client
from pyrogram.types import Message, InputMediaPhoto, InputMediaDocument, InputMediaVideo
from decouple import config

api_id = config("API_ID")
api_hash = config('API_HASH')
chat_ids = config('CHAT_IDS', cast=lambda v: [int(i) for i in v.split(',')])
destination_chat_id = config('DESTINATION_CHAT_ID', cast=int)
forbidden_words = config('FORBIDDEN_WORDS').split(', ')

app = Client("my_account", api_id=api_id, api_hash=api_hash)

@app.on_message()
def handle_message(client, message: Message):
    if message.chat.id in chat_ids:
        if any(word in message.text.lower() for word in forbidden_words):
            print("Found forbidden word in the message:", message.text)
            return 
        if message.text:
            print("Received message in the supergroup:", message.text)
            app.send_message(destination_chat_id, message.text)
        elif message.media:
            file_id = None
            media_type = None
            caption = message.caption 
            if message.photo:
                file_id = message.photo.file_id
                media_type = InputMediaPhoto(file_id, caption=caption) if caption else InputMediaPhoto(file_id)
            elif message.document:
                file_id = message.document.file_id
                media_type = InputMediaDocument(file_id, caption=caption) if caption else InputMediaDocument(file_id)
            elif message.video:
                file_id = message.video.file_id
                media_type = InputMediaVideo(file_id, caption=caption) if caption else InputMediaVideo(file_id)
            print("Caption:", caption)
            print("File ID:", file_id)
            app.send_media_group(destination_chat_id, media=[media_type])

app.run()