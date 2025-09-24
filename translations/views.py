from django.shortcuts import render, redirect
from .forms import UploadPOForm
from .models import Translation
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
