from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
import openai
from openai import AsyncOpenAI
import sys


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

class Reference:
    '''
    A class to store previously response from openai API
    '''
    def __init__(self) -> None:
        self.conversation = []


reference = Reference()
model_name = "gpt-4.1-mini"


# initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot)


def clear_past():
    """
    A function to clear the previous conversation and comntext
    """
    reference.conversation = []


@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context
    """
    clear_past()
    await message.reply("You have cleared the past conversation and context.")


@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives messages with '/start' or '/help' command
    """
    await message.reply("Hi\nI am Tele Bot!\nCreated by Marcel. How can I assist you?")


@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu
    """
    help_command = """
    Hi there, I am a Telegram bot created by Marcel! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversations and context
    /help - t get this help menu.
    I hope this helps.  :)
    """
    await message.reply(help_command)


@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    
    user_message = {"role": "user", "content": message.text}
    reference.conversation.append(user_message)
    response = await openai_client.chat.completions.create(
        model = model_name,
        messages = reference.conversation
    )

    assistant_message = response.choices[0].message
    reference.conversation.append({"role": assistant_message.role, "content": assistant_message.content})
    
    await message.reply(assistant_message.content)



# start the bot
if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)