import os
from dotenv import load_dotenv
load_dotenv()

import openai

API_HASH = TG_BOT = os.getenv('TG_BOT_TOKEN')
openai.api_key = os.environ.get('OPENAI_API_KEY')

#Import Telegram Bot Features
from telegram import InputMediaAudio, InputMediaVideo, Update, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Define a function that sends a message to ChatGPT and gets a response
def ask_chatgpt(message_history):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        n=1,
        messages=message_history)
    wegot_content = response.choices[0]['message']
    return wegot_content


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    activeuser = update.effective_user
    print(activeuser)
    print(update.message['text']+" - Bot is already running!")
    await update.message.reply_html(
        rf"Dear {activeuser.mention_html()}, Bot is active, Send Messages continuously to chat.", reply_markup=ReplyKeyboardRemove(selective=True))



async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    activeuser = update.effective_user
    print(activeuser)
    FLAG = 1
    print(update.message['text']+" - Resetting The System...")
    message_history = [
                {"role": "system", "content": "You are a helpful assistant with exciting, interesting things to say."}]
    await update.message.reply_html(
        rf"Dear {activeuser.mention_html()}, Chat is Reset, You can continue asking new things.", reply_markup=ReplyKeyboardRemove(selective=True))

message_history = [
                {"role": "system", "content": "You are a helpful assistant with exciting, interesting things to say."}]

async def chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    endlist=['stop', 'halt', 'quit', 'exit', 'end', 'cancel', 'close', 'finish', 'bye', 'goodbye', 'farewell', 'done']
    msg = update.message.text
    if msg.lower() in endlist:
        await stop(update,context)
    else:      
        try:
            prompt = {"role": "user", "content": msg}
            message_history.append(prompt)
            response = ask_chatgpt(message_history)
            print(response['content'])
            await context.bot.send_message(chat_id=update.message.chat.id, text="{}".format(response['content']),parse_mode='MARKDOWN')
            message_history.append(response)
        except Exception as e:
            # monitor exception using Rollbar
            print("Error asking ChatGPT", e)

#All Commands and Listeners
def main() -> None:
    
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TG_BOT).read_timeout(10).write_timeout(50).get_updates_read_timeout(42).connect_timeout(30).build()
    print("Bot Initiated!")
    
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    #For other links
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt))

    
    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()