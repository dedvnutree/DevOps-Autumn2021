from django.shortcuts import render
from shop.settings import EMAIL_HOST_USER
from . import forms
from django.core.mail import send_mail

#DataFlair #Send Email
def subscribe(request):
    sub = forms.Subscribe()
    if request.method == 'POST':
        sub = forms.Subscribe(request.POST)
        subject = 'Икея для бедных'
        message = 'мип мэп'
        recepient = str(sub['Email'].value())
        send_mail(subject,
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        return render(request, 'send_mail/success.html', {'recepient': recepient})
    return render(request, 'send_mail/index.html', {'form':sub})