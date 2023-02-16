
import pytest
from django.contrib.auth.models import User

from GamersCave.models import *
from GamersCave.forms import *

from django.test import Client,TestCase

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user():
    user = User.objects.create(username='test', email='test@test.com')
    return user

@pytest.fixture
def threeart():
    user = User.objects.create(username='test', email='test@test.com')

    article1 = Article.objects.create(title='bajojajo1', text='bajojajobajojajobajojajo', by_user=user)
    article2 = Article.objects.create(title='bajojajo2', text='bajojajobajojajobajojajo', by_user=user)
    article3 = Article.objects.create(title='bajojajo3', text='bajojajobajojajobajojajo', by_user=user)
    return [article1,article2,article3]

@pytest.fixture
def three_users():
    user1 = User.objects.create(username='test1', email='test1@test.com')
    user2 = User.objects.create(username='test2', email='test2@test.com')
    user3 = User.objects.create(username='test3', email='test3@test.com')
    return [user1,user2,user3]


@pytest.fixture
def studio():
    return Studio.objects.create(name='Blizzard', is_active=True)

@pytest.fixture
def game():
    std=Studio.objects.create(name='test')
    return Game.objects.create(
        name='Gothic3',year=2006,description='xyz',studio=std
    )
@pytest.fixture
def threegames():
    std = Studio.objects.create(name='test')
    game1=Game.objects.create(name='test1',year=2000,description='xyz',studio=std)
    game2=Game.objects.create(name='test2',year=2000,description='xyz',studio=std)
    game3=Game.objects.create(name='test3',year=2000,description='xyz',studio=std)
    return [game1,game2,game3]


@pytest.fixture
def forumpost():
    user = User.objects.create(username='test3', email='test@test.com')
    post1=Forum_post.objects.create(user=user,title='latarka mi nie dziala', text='pomocy plis')
    post2=Forum_post.objects.create(user=user,title='pralka mi nie dziala', text='pomocy plis')
    post3=Forum_post.objects.create(user=user,title='zmywarka mi nie dziala', text='pomocy plis')
    return [post1,post2,post3]

@pytest.fixture
def post():
    user = User.objects.create(username='test4', email='test@test.com')
    post = Forum_post.objects.create(user=user, title='latarka mi nie dziala', text='pomocy plis')
    return post




@pytest.mark.django_db
def test_basic(client):
    response = client.get('')
    assert response.status_code == 200

@pytest.mark.django_db
def test_register_user_view(client):
    # Testing GET
    get_response=client.get('/add_user/')
    assert get_response.status_code==200

    # Testing POST
    count_before_create=User.objects.count()
    data={
        'username':'test',
        'password':'test',
        'password2':'test',
        'first_name':'testt',
        'last_name':'testy',
        'email':'test@test.pl',
    }
    post_response = client.post('/add_user/',data)
    count_after_create=User.objects.count()

    assert post_response.status_code==200
    assert count_after_create==count_before_create+1


@pytest.mark.django_db
def test_login_user_view(client):
    # Testing GET
    get_response=client.get('/login/')
    assert get_response.status_code==200

    # Testing POST

    data = {
                'username':'Heniek123',
                'password':'haslo1',
                }

    User.objects.create_user(**data)


    post_response = client.post('/login/',**data)

    assert post_response.status_code==200
    assert post_response.status_code!=500

@pytest.mark.django_db
def test_logout_user_view(client):
    # Testing GET
    get_response=client.get('/logout/')
    assert get_response.status_code==200




@pytest.mark.django_db
def test_user_view(client, user):
    # Testing GET
    response = client.get(f'/user/{user.id}/')
    assert response.status_code == 200

    assert user.username == 'test'
    assert user.email == 'test@test.com'

    #Testing non existing user
    response=client.get('/user/12521/')
    assert response.status_code==404\

@pytest.mark.django_db
def test_add_studio_view(client):
    # Testing GET
    response = client.get(f'/add_studio/')
    assert response.status_code == 200

    count_before_create=Studio.objects.count()
    data = {
        'name': 'test',
        'is_active': True,
    }



    post_response = client.post('/add_studio/', data)

    count_after_create=Studio.objects.count()

    assert count_after_create == count_before_create+1
    assert post_response.status_code == 302
    assert post_response.status_code != 500

@pytest.mark.django_db
def test_studio_view(client,studio):
    response=client.get(f'/studio/{studio.id}/')
    assert response.status_code==200

    assert studio.name =='Blizzard'
    assert studio.is_active==True

    response=client.get('/studio/215125/')
    assert response.status_code==404

@pytest.mark.django_db
def test_all_studios_view(client,three_users):
    response=client.get('/all_studios/')
    assert response.status_code==200

    users=User.objects.all()
    i = 1
    for u in users:

        assert u.username ==f"test{i}"
        assert u.email ==f"test{i}@test.com"
        i+=1

@pytest.mark.django_db
def test_add_game_view(client):
    #testing GET
    response = client.get('/add_game/')
    assert response.status_code==200

    # Testing POST
    studio = Studio.objects.create(name='teststudio', is_active = True)
    count_before = Game.objects.count()
    post_response = client.post('/add_game/', data={
        'name': 'test',
        'year': 2022,
        'description': 'test game.',
        'studio': studio.id,
    })
    count_after=Game.objects.count()

    assert post_response.status_code == 302
    assert count_after==count_before+1



@pytest.mark.django_db
def test_game_view(client,game,user):

    client.force_login(user)
    response = client.get(f'/game/{game.id}/')
    assert response.status_code == 200

    assert game.name=='Gothic3'
    assert game.year==2006
    assert game.description == 'xyz'

    response = client.get('/game/1225215125/')
    assert response.status_code==404

    # Testing POST
    # count_before = GameRating.objects.count()

    post_response = client.post(f'/game/{game.id}/', data={
        'user':user.id,
        'game':game.id,
        'rate':5,
        'reviev':'abcd'
    })
    # count_after = GameRating.objects.count()

    assert post_response.status_code == 200
    # assert count_after == count_before + 1

@pytest.mark.django_db
def test_all_studios_view(client,threegames):
    response=client.get('/all_games/')
    assert response.status_code==200

    games=Game.objects.all()
    i = 1
    for g in games:

        assert g.name ==f"test{i}"
        assert g.year ==2000
        assert g.description =='xyz'
        i+=1

@pytest.mark.django_db
def test_add_article_view(client,user):

    #TESTING GET
    response=client.get('/add_article/')
    assert response.status_code==200

    # TESTING POST
    client.force_login(user)
    count_before=Article.objects.count()
    data ={
        'title':'xyz',
        'text':'xyzxyzxyzxyzxyz',
        'user':user.id
    }
    post_response=client.post('/add_article/',data=data)
    count_after=Article.objects.count()

    assert post_response.status_code==302
    assert count_after==count_before+1


@pytest.mark.django_db
def test_all_articles_view(client,threeart):
    response=client.get('/all_articles/')
    assert response.status_code==200

    art=Article.objects.all()
    i = 1
    for a in art:

        assert a.title ==f"bajojajo{i}"
        assert a.text =='bajojajobajojajobajojajo'
        i+=1

@pytest.mark.django_db
def test_forum_view(client,forumpost,user):
    client.force_login(user)
    response=client.get('/gamecave/forum/')
    assert response.status_code==200

    posts=Forum_post.objects.all()
    assert posts[0].text=='pomocy plis'
    assert posts[1].text=='pomocy plis'
    assert posts[2].text=='pomocy plis'
    assert posts[0].title=='latarka mi nie dziala'
    assert posts[1].title=='pralka mi nie dziala'
    assert posts[2].title=='zmywarka mi nie dziala'
    assert posts[0].user.username == 'test3'

@pytest.mark.django_db
def test_forum_post_add_view(client,user):

    #TESTING GET
    client.force_login(user)
    response=client.get('/gamecave/forum/addpost/')
    assert response.status_code==200

    #TESTING POST
    count_before=Forum_post.objects.count()
    data={
        'user':user.id,
        'title':'Kran mi przecieka',
        'text':'Matko bosko kran mi przecieka,pomozcie ludzie',
    }
    post_response=client.post('/gamecave/forum/addpost/',data=data)

    count_after=Forum_post.objects.count()

    assert post_response.status_code == 302
    assert count_after == count_before + 1

@pytest.mark.django_db
def test_forum_post_view(client,post,user):
    #TESTING GET
    client.force_login(user)
    response=client.get(f'/gamecave/forum/{post.id}/')
    assert response.status_code == 200
    p = Forum_post.objects.all()
    assert p[0].title =='latarka mi nie dziala'
    assert p[0].text=='pomocy plis'
    assert p[0].user.username=='test4'

    #TESTING POST
    count_before=Post_answer.objects.count()
    data={
        'user':user.id,
        'text':'testanswer',
        'post':p[0].id
    }

    post_response=client.post(f'/gamecave/forum/{post.id}/',data=data)

    count_after=Post_answer.objects.count()

    assert post_response.status_code == 200
    assert count_after == count_before + 1









































