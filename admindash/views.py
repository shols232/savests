from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import SendEmailForm
from django.contrib.auth.models import User
from .models import SendEmail

def send_email(request, **kwargs):
    if request.method == 'POST':
        form_data = request.POST
        email_id = form_data.get('email')
        if email_id == 'everyone':
            # get all user emails excluding current user
            user_emails = [
                user.email for user in User.objects.all() if user.email != request.user.email
                ]
        else:
            user_emails = [User.objects.get(id=email_id).email, ]
        subject = form_data.get('subject')
        message = form_data.get('message')
        from_email = request.user.email
        
        send_mail(
            subject,
            message,
            from_email,
            user_emails,
            fail_silently=False,
        )
        return redirect('/admin/auth/user')
    users = User.objects.all()
    return render(request, 'send_email.html', {'users':users})


def toggle_user_activity(request, id):
    user = User.objects.get(id=id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect('/admin/auth/user')

def toggle_admin(request, id):
    user = User.objects.get(id=id)

    # allow action only if request is from superuser
    if request.user.is_superuser:
        if user.is_superuser:
            user.is_superuser = False
        else:
            user.is_superuser = True
        user.save()
        return redirect('/admin/auth/user')
    