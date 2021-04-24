from django.core.mail import send_mail


def send_activation_email(email, activation_code, is_password):
    activation_url = f'http://localhost:8000/v1/api/account/activate/{activation_code}'
    if not is_password:
        message = f'Спасибо за регистрацию\nДля активации перейдите по этой ссылке:  {activation_url}'
    else:
        message = f'Ваш активационный код:  {activation_code}'
    send_mail(
        'Активация Socks_blog',
        message,
        'm.ysakov.jcc@gmail.com',
        [email, ],
        fail_silently=False,
    )


