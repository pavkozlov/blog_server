from django.test import TestCase
from rest_framework.test import APIClient


def register_and_login(client, email, password):
    client.post('/auth/registration/', {'email': email, 'password': password})
    token_response = client.post('/auth/login/', {'email': email, 'password': password})
    return token_response.data


class BlogBaseTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        # Регистрация
        token = register_and_login(self.client, 'admin@admin.ru', 'admin')

        # Авторизация
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        # Создать 5 тегов
        for tag_num in range(1, 6):
            self.client.post('/blog/tags/', {'title': f'new tag {tag_num}'})

        # Создать 3 категории
        for cat_num in range(1, 4):
            self.client.post('/blog/category/', {'title': f'new category {cat_num}'})

        # Создать 4 поста
        self.client.post('/blog/posts/', {'body': 'SIMPLE POST'})
        self.client.post('/blog/posts/', {'body': 'POST WITH CATEGORY', 'category_id': 1})
        self.client.post('/blog/posts/', {'body': 'POST WITH TAGS', 'tags_ids': [1, 2, 3]})
        self.client.post(
            '/blog/posts/',
            {'body': 'POST WITH CATEGORY AND TAGS', 'category_id': 2, 'tags_ids': [1, 4, 5]}
        )

    def test_setUp(self, tags_count=5, categories_count=3, posts_count=4):
        # Проверяем что всё создалось, создалось от имени нашего юзера
        tags = self.client.get('/blog/tags/').data
        categories = self.client.get('/blog/category/').data
        posts = self.client.get('/blog/posts/').data
        self.assertEqual(tags['count'], tags_count)
        self.assertEqual(categories['count'], categories_count)
        self.assertEqual(posts['count'], posts_count)
        for post in posts['results']:
            self.assertEqual(post['author']['id'], 1)
            self.assertEqual(post['author']['email'], 'admin@admin.ru')

    def test_created_posts(self):
        # Проверяем что посты создались правильно
        p1 = self.client.get('/blog/posts/1/')
        p2 = self.client.get('/blog/posts/2/')
        p3 = self.client.get('/blog/posts/3/')
        p4 = self.client.get('/blog/posts/4/')

        self.assertEquals(p1.status_code, p2.status_code, 200)
        self.assertEquals(p3.status_code, p4.status_code, 200)

        self.assertEqual(p1.data['category'], None)
        self.assertEqual(p1.data['tags'], [])

        self.assertEqual(p2.data['category']['id'], 1)

        self.assertEqual(len(p3.data['tags']), 3)
        self.assertEqual([tag['id'] for tag in p3.data['tags']], [1, 2, 3])

        self.assertEqual(p4.data['category']['title'], 'new category 2')
        self.assertEqual(p4.data['tags'][1]['title'], 'new tag 4')

    def test_created_tag(self):
        # Проверяем что теги создались правильно
        t1 = self.client.get('/blog/tags/1/')
        t2 = self.client.get('/blog/tags/2/')

        self.assertEquals(t1.status_code, t2.status_code, 200)
        self.assertEqual(t1.data['count'], 2)
        self.assertEqual(t1.data['title'], 'new tag 1')
        self.assertEqual(t2.data['count'], 1)

    def test_created_category(self):
        # Проверяем что категории создались правильно
        c1 = self.client.get('/blog/category/1/')
        c4 = self.client.get('/blog/category/3/')

        self.assertEquals(c1.status_code, c4.status_code, 200)
        self.assertEqual(c1.data['count'], 1)
        self.assertEqual(c1.data['title'], 'new category 1')
        self.assertEqual(c4.data['count'], 0)

    def test_destroy(self):
        # Проверяем удаление
        p = self.client.delete('/blog/posts/1/')
        t = self.client.delete('/blog/tags/1/')
        c = self.client.delete('/blog/category/1/')

        self.assertEquals(p.status_code, c.status_code, t.status_code)
        self.assertEqual(p.status_code, 204)

        self.test_setUp(4, 2, 3)

    def test_patch(self):
        # Проверяем патч
        modifed = 'modifed'

        p = self.client.patch('/blog/posts/2/', {'body': modifed})
        t = self.client.patch('/blog/tags/2/', {'title': modifed})
        c = self.client.patch('/blog/category/2/', {'title': modifed})

        self.assertEquals(p.status_code, c.status_code, t.status_code)
        self.assertEqual(p.status_code, 200)

        c2 = self.client.get('/blog/category/2/').data
        t2 = self.client.get('/blog/tags/2/').data
        p2 = self.client.get('/blog/posts/2/').data

        self.assertEquals(c2['title'], t2['title'], p2['body'])
        self.assertEqual(c2['title'], modifed)
