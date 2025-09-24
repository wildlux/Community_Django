import os
import django
from datetime import datetime, timedelta
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_translations.settings')
django.setup()

from translations.models import LoginToken

TOKEN = '8210640700:AAEHDeluJEJhL2FGaiy-8FGIGbFnXV3zmDw'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_id = str(update.effective_user.id)
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(hours=4)
    LoginToken.objects.create(token=token, telegram_id=telegram_id, expires_at=expires_at)
    link = f'http://localhost:8000/login/{token}'
    await update.message.reply_text(f'Clicca qui per accedere: {link}\nIl link scade tra 4 ore.')

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()