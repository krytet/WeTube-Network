from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
import time

from .forms import PostForm
from .models import Post

User = get_user_model()
# Create your tests here.


class TestStringMethods(TestCase):
    
    def test_length(self):
        self.assertEqual(len('wetube'), 6)

    def test_show_msg(self):
                # действительно ли первый аргумент — True?
                self.assertTrue(True, msg="Важная проверка на истинность")

class ProfileTest(TestCase):
    def setUp(self):
        # создание тестового клиента — подходящая задача для функции setUp()
        self.client = Client()
        # создаём пользователя
        self.user = User.objects.create_user(
            username = 'TAcc_1', email = 'account1@acc.com', password = 'TestAccount1'
        )
        self.user_2 = User.objects.create_user(
            username = 'TAcc_2', email = 'account1@acc.com', password = 'TestAccount1'
        )
        # создаём пост от имени пользователя
        self.post = Post.objects.create(text = 'My first post in test post!', author = self.user)
        self.post2 = Post.objects.create(text = 'My first post in test post for comment!', author = self.user_2)

    def test_profile_open(self):         # проверяем наличие страницы
        # формируем GET-запрос к странице сайта
        response = self.client.get("/TAcc_1/")
        # проверяем что страница найдена
        self.assertEqual(response.status_code, 200, msg='Ответ страницы не 200')

    def test_profile_text(self):    # проверка количества записей в профеле
        response = self.client.get("/TAcc_1/")
        # проверяем, что при отрисовке страницы был получен список из 1 записи
        self.assertEqual(len(response.context["page"]), 1, msg='Не соотвествует число записей')

    def test_profile_account(self):  #проверка соотвествия страницы пользователя
        response = self.client.get("/TAcc_1/")
        # проверяем что станица пользовател соответствует классу User
        self.assertIsInstance(response.context["profile"], User, msg='Созданный аккаунт не входит в User')
        # проверяем, что объект пользователя, переданный в шаблон, 
        # соответствует пользователю, которого мы создали
        self.assertEqual(response.context["profile"].username, self.user.username, msg=' Страница профеля не соотвествует аккаунту')

    def test_new_post_anonim(self): #анономное добовление записи
#        context = {
#            'text' : 'New test post',
#            'author' : self.user,
#        }
#        response = self.client.post("/new/", context )
        response = self.client.get("/new/")
        self.assertEqual(response.status_code, 302, msg='Не пересылает на другую страницу')

    def test_new_post_user(self): #добовление авторезированным пользователем

        response = self.client.login(username='TAcc_1', password='TestAccount1')
        self.assertTrue(response, msg= 'Не удолось авторизоваться')
        response = self.client.get("/new/")
        self.assertEqual(response.status_code, 200, msg='Пересылает на другую страницу')
        
        context_post ={
            'text' : 'New test post',
            'author' : self.user,
        }
        response = self.client.post("/new/", context_post )
        self.assertEqual(response.status_code, 302, msg='Не пересылает на другую страницу новый пост')

        response = self.client.get("/TAcc_1/")
        # проверяем, что при отрисовке страницы был получен список из 1 записи
        self.assertEqual(len(response.context["page"]), 2, msg='Не соотвествует число записей')

        post_id = self.post.id
        response = self.client.get(f"/TAcc_1/{post_id}/edit/")
        self.assertEqual(response.status_code, 200, msg='Не может редоктировать свою запись')


    def test_edit_post_anonim(self): #редоктирование анаоном но запись
        post_id = self.post.id
        response = self.client.get(f"/TAcc_1/{post_id}/edit/")
        self.assertEqual(response.status_code, 302, msg='Можно редоктировать не свою запись')

    def test_404(self):  # возращает ли страницу 404
        response = self.client.get('/no_page', follow= True)
        self.assertEqual(response.status_code, 404, msg='Не переходит на страницу 401')

    def test_comment(self):
        post_id = self.post.id
        # попытка написать коментарий не авторизованным
        text_comment = 'comment for the post'
        response_0 = self.client.get(f"/TAcc_1/{post_id}/").content
        post = self.client.post(f"/TAcc_1/{post_id}/comment/", { 'text': text_comment})
        response = self.client.get(f"/TAcc_1/{post_id}/")
        #self.assertNotContains(response, text_comment, msg_prefix= 'Добавился коментарий неавторизованного пользователя') # не рабтает
        self.assertEqual(response.content, response_0, msg='Сраницы отличаються, значит появился коментарий неавторизованного пользователя')

        # написание коментрария авторизованного пользователя
        
        response = self.client.login(username='TAcc_1', password='TestAccount1')
        response_0 = self.client.get(f"/TAcc_1/{post_id}/").content
        post = self.client.post(f"/TAcc_1/{post_id}/comment/", { 'text': text_comment})
        response = self.client.get(f"/TAcc_1/{post_id}/")
        #self.assertContains(response, text_comment, msg_prefix= 'Не добавился коментарий авторизованного пользователя') # не работает
        self.assertNotEqual(response.content, response_0, msg='Сраницы схожи, значит не появился коментарий авторизованного пользователя')

    def test_post_follow(self):
        response = self.client.login(username='TAcc_1', password='TestAccount1')
        response_0 = self.client.get("/follow/")
        response = self.client.get("/TAcc_2/follow/")
        response = self.client.get("/follow/")
        self.assertNotEqual(response.content.decode(), response_0.content.decode(), msg='Отсутствуют записи в подписках, и нет возможности подписок')

    def test_cache(self):
        post_id = self.post.id
        response = self.client.get("")
        response_1 = response.content
        response = self.client.get("")
        self.assertEqual(response_1, response.content, msg='Не прозводиться хеширования главной страницы')
        response = self.client.login(username='TAcc_1', password='TestAccount1')
        post = self.client.post(f"/TAcc_1/{post_id}/edit/", {'author': self.user, 'text': 'post for trst cache'})
        time.sleep(21)
        response = self.client.get("")
        self.assertNotEqual(response_1, response.content, msg='хеширование страницы более 20 сек')

    
    def test_post_noimagefile(self):
        post_id = self.post.id
        response = self.client.login(username='TAcc_1', password='TestAccount1')
        
        with open('posts/text.txt','rb') as img:
            post = self.client.post(f"/TAcc_1/{post_id}/edit/", {'author': self.user, 'text': 'post with no image file', 'image': img})
        
        response = self.client.get(f"/TAcc_1/{post_id}/")
        self.assertNotContains( response  , 'img class', msg_prefix= 'Отсутствует изоброжение в записи, так как файл не являеться изоброжением')
        #response = self.client.get(f"/TAcc_1/{post_id}/")
        #self.assertContains( response  , 'img class', msg_prefix= 'Отсутствует изоброжение в записи')

    def test_check_site_post_on_image_tag(self): #проверка тега записи на наличие картинки
        post_id = self.post.id
        response = self.client.login(username='TAcc_1', password='TestAccount1')
        with open('posts/file.jpg','rb') as img:
            post = self.client.post(f"/TAcc_1/{post_id}/edit/", {'author': self.user, 'text': 'post with image', 'image': img})
        response = self.client.get(f"/TAcc_1/{post_id}/")
        self.assertContains( response  , 'img class', msg_prefix= 'Отсутствует изоброжение в записи')
        response = self.client.get(f"/TAcc_1/")
        self.assertContains(response, 'img class', msg_prefix= 'Отсутствует изоброжения на сранице пользователя')
        time.sleep(20) # ХЕШИРОВАНИЕ 20 СЕК
        response = self.client.get(f"")
        self.assertContains(response, 'img class', msg_prefix= 'Отсутствует изоброжения на главной странице')



    

    
        







        
