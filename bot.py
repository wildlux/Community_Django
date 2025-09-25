import os
import django
from datetime import datetime, timedelta
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_translations.settings')
django.setup()

from translations.models import LoginToken

TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_id = str(update.effective_user.id)
    now = datetime.now()
    active_token = LoginToken.objects.filter(telegram_id=telegram_id, expires_at__gt=now).first()
    if active_token:
        await update.message.reply_text(f'Hai già un token attivo: {active_token.token}\nValido fino a {active_token.expires_at}. Incollalo sul sito per accedere.')
    else:
        token = str(uuid.uuid4())
        expires_at = now + timedelta(hours=4)
        LoginToken.objects.create(token=token, telegram_id=telegram_id, expires_at=expires_at)
        await update.message.reply_text(f'Stringa di accesso: {token}\nValida per 4 ore. Incollala sul sito per accedere.')

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()