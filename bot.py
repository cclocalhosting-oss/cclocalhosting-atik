from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import yt_dlp

TOKEN = "8766736007:AAFbawj0o4_D6NaIN7ri0UmS4tSBYzA_RXs"

async def start(update: Update, context):
    await update.message.reply_text("Send video link 🎬")

async def download(update: Update, context):
    url = update.message.text

    ydl_opts = {
        'outtmpl': 'video.mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await update.message.reply_video(video=open("video.mp4", "rb"))

    except Exception as e:
        await update.message.reply_text("Download failed ❌")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

app.run_polling()
