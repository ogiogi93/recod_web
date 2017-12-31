from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from account.forms import (
    LoginForm,
    login_form,
    RegisterForm
)


def top_page(request):
    return render(request, 'web/index.html', context={
        'login_form': login_form,
    })


def forum_page(request):
    return render(request, 'web/forum.html', context={
        'login_form': login_form,
    })


def news_list_page(request):
    return render(request, 'web/news_list.html', context={
        'login_form': login_form
    })


def video_list_page(request):
    return render(request, 'web/video_list.html', context={
        'login_form': login_form
    })


def live_page(request):
    return render(request, 'web/live.html', context={
        'login_form': login_form
    })


def competition_page(request):
    return render(request, 'web/competition.html', context={
        'login_form': login_form
    })


def team_list_page(request):
    return render(request, 'web/team_list.html', context={
        'login_form': login_form
    })


def contact_page(request):
    return render(request, 'web/contact.html', context={
        'login_form': login_form
    })


def article_page(request):
    return render(request, 'web/article.html', context={
        'login_form': login_form
    })


def register_page(request):
    register_form = RegisterForm(request.POST or None)
    return render(request, 'web/register.html', context={
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
        return render(request, 'web/login.html', context={
            'login_form': form
        })
    return render(request, 'web/login.html', context={
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
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'web/index.html', context={
            'login_form': login_form,
        })
    return render(request, 'web/register.html', context={
        'login_form': login_form,
        'register_form': register_form
    })
