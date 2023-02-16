from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from GamersCave.models import *
from GamersCave.forms import *


# Create your views here.
def homepage(request):
    return render(request, 'home.html')


class RegisterUserView(View):
    def get(self, request):
        form = UserCreateForm()
        return render(request, 'register_user.html', context={'form': form})

    def post(self, request):
        form = UserCreateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            User.objects.create(username=data.get('username'), password=data.get('password'),
                                first_name=data.get('first_name'), last_name=data.get('last_name'),
                                email=data.get('email'))

            msg='uzytkownik zarejestrowany pomyslnie!'
            return render(request, 'home.html', {'msg': msg})
        else:
            return render(request, 'register_user.html', context={'form': form})


class LoginUserView(View):
    def get(self, request):
        form = LoginUserForm()
        return render(request, 'login2.html', context={'form': form})

    def post(self, request):
        form = LoginUserForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            username = data.get('username')
            password = data.get('password')

            user = User.objects.get(username=username, password=password)
            login(request, user)
            msg = f"zalogowano użytkownika {user}"
            return render(request, 'home.html', {'msg': msg})
        else:
            msg='bledne dane'
            return render(request, 'login2.html', context={'form': form,'msg':msg})


class LogoutView(View):
    def get(self, request):
        logout(request)
        msg = "wylogowano użytkownika"
        return render(request, 'home.html', {'msg': msg})


class UserView(View):
    def get(self, request, user_id):
        # user = User.objects.get(pk=user_id)
        user = get_object_or_404(User,pk=user_id)
        reviews=GameRating.objects.filter(user=User.objects.get(id=user_id))
        return render(request, 'user.html', {'user': user, 'reviews':reviews})


class AddStudioView(View):

    def get(self, request):
        form = AddStudioForm()
        return render(request, 'add_studio.html', context={'form': form})

    def post(self, request):
        form = AddStudioForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Studio.objects.create(name=data.get('name'), is_active=data.get('is_active'))
            return redirect('/all_studios/')
        else:

            return render(request, 'add_studio.html', context={'form': form})


class StudioView(View):
    def get(self, request, studio_id):
        studio = get_object_or_404(Studio,id=studio_id)
        return render(request, 'studio.html', {'studio': studio})


class AllStudioView(View):
    def get(self, request):
        studio = Studio.objects.all()

        return render(request, 'allstudios.html', {'studio': studio})


class AddGameView(View):

    def get(self, request):
        form = AddGameForm()
        return render(request, 'add_game.html', context={'form': form})

    def post(self, request):
        form = AddGameForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            studio_id = data.get('studio')
            Game.objects.create(name=data.get('name'), year=data.get('year'), description=data.get('description'),
                                studio=Studio.objects.get(id=studio_id))

            return redirect('/all_games/')
        else:
            form = AddGameForm()
            return render(request, 'add_game.html', context={'form': form})


class GameView(View):
    def get(self, request, game_id):
        # game = Game.objects.get(id=game_id)
        game = get_object_or_404(Game,id=game_id)
        gamerating = GameRating.objects.filter(game=game_id)
        if request.user.is_authenticated:
            review = GameRating.objects.filter(game=game_id, user=request.user.id)
            if review:
                log_msg = "You reviewed this game!"
                return render(request, 'game.html',
                              context={'game': game, 'log_msg': log_msg, 'gamerating': gamerating})
            else:
                form = GameRatingForm()
                return render(request, 'game.html', context={'game': game, 'form': form, 'gamerating': gamerating})
        else:
            log_msg = "Please log in to make review"
            return render(request, 'game.html', context={'game': game, 'log_msg': log_msg, 'gamerating': gamerating})

    def post(self, request, game_id):
        form = GameRatingForm(request.POST)
        gamerating = GameRating.objects.filter(game=game_id)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.get(id=request.user.id)
            game = Game.objects.get(id=game_id)
            rate = data.get('rate')
            reviev = data.get('reviews')

            GameRating.objects.create(user=user, game=game, rate=rate, reviev=reviev)
            log_msg = "Review added!"
            return render(request, 'game.html', context={'game': game, 'log_msg': log_msg, 'gamerating': gamerating})

        else:
            return HttpResponse("blad")


class AllGameView(View):
    def get(self, request):
        game = Game.objects.all()
        return render(request, 'allgames.html', {'game': game})


class AddArticleView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = AddArticleForm()
            return render(request, 'newarticle.html', {'form': form})
        else:
            return HttpResponse("Tylko zalogowani uzytkownicy moga pisac artykuly!")

    def post(self, request):
        form = AddArticleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            title = data.get('title')
            text = data.get('text')
            user = request.user

            Article.objects.create(title=title, text=text, by_user=user)


            return redirect('/all_articles/')
        else:
            msg='Nie udalo sie dodac artykulu'
            return render(request,'newarticle.html',{'form':form,'msg':msg})


class AllArticleView(View):
    def get(self, request):
        article = Article.objects.all()
        return render(request, 'allarticles.html', {'article': article})


class ForumView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        posts = Forum_post.objects.all()
        answers = Post_answer.objects.all()
        return render(request, 'forum.html', {'posts': posts, 'answers': answers})


class ForumPostAddView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = Forum_postForm()
        return render(request, 'createpost.html', {'form': form})

    def post(self, request):
        form = Forum_postForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            user = request.user
            title = data.get('title')
            text = data.get('text')
            Forum_post.objects.create(user=user, title=title, text=text)
            return redirect('/gamecave/forum/')
        else:
            form=Forum_postForm()
            msg='Nie udalo sie dodac posta'
            return render(request, 'createpost.html', {'form': form,'msg':msg})


class ForumPostView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, forum_post_id):
        # post = Forum_post.objects.get(id=forum_post_id)
        post=get_object_or_404(Forum_post,id=forum_post_id)
        form = Post_answerForm()
        answers = Post_answer.objects.filter(post=post)
        return render(request, 'forumpost.html', context={'post': post, 'form': form, 'answers': answers})

    def post(self, request, forum_post_id):
        form = Post_answerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            user = request.user
            text = data.get('text')
            post = Forum_post.objects.get(id=forum_post_id)
            answers = Post_answer.objects.filter(post=post)
            Post_answer.objects.create(user=user, text=text, post=post)

            return render(request, 'forumpost.html', context={'post': post, 'form': form, 'answers': answers})
