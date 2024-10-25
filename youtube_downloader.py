import yt_dlp
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
)

# أدخل رمز الوصول (Token) الخاص بك هنا
TELEGRAM_TOKEN = '7706214778:AAEAI-NSprJNmmTs0zls55SpgUD8xi2AJfM'

# إعدادات yt-dlp لتنزيل الفيديو
ydl_opts = {
    'format': 'best',
    'outtmpl': '%(title)s.%(ext)s',  # حفظ الفيديو بنفس اسمه الأصلي
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """رسالة ترحيب عند بدء استخدام البوت."""
    await update.message.reply_text(
        "👋 أهلاً بك في *YouTube Video Downloader Bot*!\n"
        "📥 أرسل لي رابط فيديو من YouTube، وسأقوم بتحميله لك بأعلى جودة.",
        parse_mode='Markdown'
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تحميل الفيديو وإرساله عبر Telegram."""
    url = update.message.text.strip()
    
    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("⚠️ يرجى إرسال رابط صالح من YouTube.")
        return

    await update.message.reply_text("⏳ جاري تحميل الفيديو، يرجى الانتظار...")

    try:
        # تنزيل الفيديو باستخدام yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = ydl.prepare_filename(info)

        # إرسال الفيديو إلى المستخدم
        with open(video_title, 'rb') as video:
            await update.message.reply_video(video)

        await update.message.reply_text("✅ تم إرسال الفيديو بنجاح!")

    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ أثناء التنزيل: {e}")

def main():
    """تشغيل البوت."""
    # إنشاء تطبيق Telegram باستخدام ApplicationBuilder
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # التعامل مع الأوامر والرسائل
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    # بدء البوت
    print("🤖 البوت يعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()
