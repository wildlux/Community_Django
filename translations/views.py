from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import UploadPOForm
from .models import Translation, LoginToken
import polib

def home(request):
    return render(request, 'home.html')

def upload_po(request):
    if not request.user.is_authenticated:
        return redirect('account_login')
    if request.method == 'POST':
        form = UploadPOForm(request.POST, request.FILES)
        if form.is_valid():
            po_file = request.FILES['po_file']
            po = polib.pofile(po_file.read().decode('utf-8'))
            for entry in po:
                msgid = entry.msgid
                msgstr = entry.msgstr
                if msgid and msgstr:  # Only if translated
                    trans, created = Translation.objects.get_or_create(
                        msgid=msgid,
                        language='it',
                        defaults={'msgstr': msgstr, 'submitted_by': request.user}
                    )
                    if not created:
                        # If exists, perhaps update if empty or something, but for now skip
                        pass
            return redirect('home')
    else:
        form = UploadPOForm()
    return render(request, 'upload_po.html', {'form': form})

def telegram_login(request, token):
    try:
        login_token = LoginToken.objects.get(token=token)
        if login_token.expires_at > timezone.now():
            user, created = User.objects.get_or_create(username=login_token.telegram_id, defaults={'email': f'{login_token.telegram_id}@telegram.com'})
            login(request, user)
            login_token.delete()  # Use once
            return redirect('home')
        else:
            login_token.delete()
    except LoginToken.DoesNotExist:
        pass
    return render(request, 'login_failed.html')
