from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST

from account.forms import LoginForm, login_form, RegisterForm
from account.models import CustomUser as User
from competition.repository.tournament import get_next_matches
from recod_web.settings import AWS_S3_CUSTOM_DOMAIN


class UserEntity:
    def __init__(self, user):
        self._user = user

    def id(self):
        return self._user.id

    def username(self):
        return self._user.username

    def nickname(self):
        return self._user.nickname

    def description(self):
        return self._user.description

    def image(self):
        return 'https://' + AWS_S3_CUSTOM_DOMAIN + '/media/' + str(self._user.image)


def user_page(request, user_id):
    """
    ユーザページへ遷移
    :param request:
    :param int user_id:
    :return:
    """
    # User IDが指定されていなかった場合は404
    if not user_id:
        return render(request, 'web/404.html', context={
            'login_form': login_form,
        })
    return render(request, 'web/user/user.html', context={
        'user': UserEntity(User.objects.get(pk=user_id)),
        'login_form': login_form,
        'next_matches': get_next_matches()
    })


def register_page(request):
    register_form = RegisterForm(request.POST or None)
    return render(request, 'web/user/register.html', context={
        'login_form': login_form,
        'register_form': register_form
    })


def login_page(request):
    """
    ログイン処理を行う, ログイン成功後はトップページへ遷移する
    :param request:
    :return:
    """
    if request.POST:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
        return render(request, 'web/user/login.html', context={
            'login_form': form
        })
    return render(request, 'web/user/login.html', context={

        'login_form': login_form
    })


def logout_page(request):
    """
    ログアウト処理を行う、ログアウト後はトップページへ遷移する　
    :param request:
    :return:
    """
    logout(request)
    return redirect('/')


@require_POST
def register(request):
    """
    ユーザー登録処理を行う, 登録後はログインした状態でトップページへ移動する
    :param request:
    :return:
    """
    register_form = RegisterForm(request.POST)
    if register_form.is_valid():
        user = register_form.save()
        # 初回はユーザーネームをそのままニックネームとしても登録する
        user.nickname = user.username
        user.save()
        login(request, user)
        return redirect('/')
    return render(request, 'web/user/register.html', context={
        'login_form': login_form,
        'register_form': register_form
    })
