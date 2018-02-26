from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from account.entity import UserEntity
from account.forms import LoginForm, login_form, RegisterForm, EditUserProfile
from account.models import CustomUser as User
from competition.repository.tournament import get_next_matches


def user_page(request, user_id):
    """
    ユーザページへ遷移
    :param request:
    :param int user_id:
    :return:
    """
    return render(request, 'web/user/user.html', context={
        'profile': UserEntity(User.objects.get(pk=user_id)),
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
                    request.session.set_expiry(86400)  # sets the exp. value of the session
                    login(request, user)  # the user is now logged in
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


@login_required
def edit_user(request, user_id):
    """
    ユーザー情報を更新する
    :param request:
    :param int user_id:
    :rtype render|redirect:
    """
    if request.method == 'POST':
        # 編集時はuser_idが設定されている
        form = EditUserProfile(request.POST, request.FILES, instance=User.objects.get(pk=user_id))
        if form.is_valid():
            form.save()
            return redirect('/user/{}/'.format(user_id))
        return render(request, 'web/user/edit_user.html', context={
                'form': form
            })
    return render(request, 'web/user/edit_user.html', context={
        'form': EditUserProfile(instance=User.objects.get(pk=user_id)),
    })
