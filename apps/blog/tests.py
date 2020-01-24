from django.test import TestCase
from apps.blog.models import Tag, Post, Category
from rest_framework.test import APIClient


class TagTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.client.post('/blog/tags/', {'title': 'new tag 0'})
        self.client.post('/blog/tags/', {'title': 'new tag 1'})

    def test_create(self):
        response = self.client.post('/blog/tags/', {'title': 'new tag 0'})
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/blog/tags/', {'title': 'new tag 2'})
        self.assertEqual(response.status_code, 201)

    def test_delete(self):
        tag_count = Tag.objects.filter(id=1).count()
        self.assertTrue(tag_count == 1)

        response = self.client.delete('/blog/tags/1/')
        tag_count = Tag.objects.filter(id=1).count()
        self.assertTrue(tag_count == 0)
        self.assertEqual(response.status_code, 204)

    def test_update(self):
        response = self.client.get('/blog/tags/2/')
        self.assertEqual(response.data['title'], 'new tag 1')

        response = self.client.put('/blog/tags/2/', {'title': 'modifed'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'modifed')

        response = self.client.get('/blog/tags/2/')
        data = response.data
        self.assertEqual(data['title'], 'modifed')


class CategoryTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.client.post('/blog/category/', {'title': 'new category 0'})
        self.client.post('/blog/category/', {'title': 'new category 1'})

    def test_create(self):
        response = self.client.post('/blog/category/', {'title': 'new category 0'})
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/blog/category/', {'title': 'new category 2'})
        self.assertEqual(response.status_code, 201)

    def test_delete(self):
        category_count = Category.objects.filter(id=1).count()
        self.assertTrue(category_count == 1)

        response = self.client.delete('/blog/category/1/')
        category_count = Category.objects.filter(id=1).count()
        self.assertTrue(category_count == 0)
        self.assertEqual(response.status_code, 204)

    def test_update(self):
        response = self.client.get('/blog/category/2/')
        self.assertEqual(response.data['title'], 'new category 1')

        response = self.client.put('/blog/category/2/', {'title': 'modifed'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'modifed')

        response = self.client.get('/blog/category/2/')
        data = response.data
        self.assertEqual(data['title'], 'modifed')


class PostTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.client.post('/blog/category/', {'title': 'new category 0'})
        self.client.post('/blog/tags/', {'title': 'new tag 0'})
        self.client.post('/blog/tags/', {'title': 'new tag 1'})
        self.client.post('/blog/posts/',
                         {'title': 'qwerty', 'body': 'body text', 'category_id': 1, 'tags_ids': [1, 2, 3]})

    def test_create(self):
        response = self.client.post('/blog/posts/',
                                    {
                                        'title': 'qwerty 2',
                                        'body': 'body text',
                                        'category_id': 1,
                                        'tags_ids': [1, 2, 3]
                                    })
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/blog/posts/2/')
        self.assertEqual(response.data['category']['title'], 'new category 0')
        self.assertEqual(response.data['tags'][0]['title'], 'new tag 0')

    def test_part_create(self):
        response = self.client.post('/blog/posts/',
                                    {
                                        'title': 'qwerty 2',
                                        'body': 'body text',
                                        'tags_ids': [1, 2, 3333]
                                    })
        self.assertEqual(response.status_code, 201)

        response = self.client.post('/blog/posts/',
                                    {
                                        'title': 'qwerty 3',
                                        'body': 'body text',
                                    })
        self.assertEqual(response.status_code, 201)

        response = self.client.post('/blog/posts/',
                                    {
                                        'title': 'qwerty 4',
                                        'body': 'body text',
                                        'category_id': 1,
                                    })
        self.assertEqual(response.status_code, 201)

        response = self.client.post('/blog/posts/',
                                    {
                                        'category_id': 1,
                                        'tags_ids': [1, 2, 3]
                                    })
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/blog/posts/',
                                    {
                                        'title': 'qwerty 4',
                                        'body': 'body text',
                                        'category_id': 1,
                                        'tags_ids': [1, 2, 3]
                                    })
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/blog/posts/',
                                    {
                                        'title': 'qwerty 1999',
                                        'body': 'body text',
                                        'category_id': 1999,
                                        'tags_ids': [1, 2, 3]
                                    })
        self.assertEqual(response.status_code, 400)

    def test_delete(self):
        category_count = Post.objects.filter(id=1).count()
        self.assertTrue(category_count == 1)

        response = self.client.delete('/blog/posts/1/')
        category_count = Post.objects.filter(id=1).count()
        self.assertTrue(category_count == 0)
        self.assertEqual(response.status_code, 204)

    def test_update(self):
        response = self.client.get('/blog/posts/1/')
        self.assertEqual(response.data['title'], 'qwerty')

        response = self.client.patch('/blog/posts/1/', {'title': 'modifed'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'modifed')

        response = self.client.get('/blog/posts/1/')
        data = response.data
        self.assertEqual(data['title'], 'modifed')
