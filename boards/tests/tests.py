from django.urls import reverse,resolve
from django.test import TestCase
from  boards.models import *
from  boards.views import *
from django.contrib.auth.models import User


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, home)

class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEqual(view.func, board_topics)

from django.urls import reverse
from django.test import TestCase
from django.urls import resolve
from boards.views import new_topic
from boards.models import Board

class NewTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Test Board', description='Test Board description')
        self.url = reverse('new_topic', kwargs={'pk': self.board.pk})
        self.response = self.client.get(self.url)

    def test_new_topic_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/{}/new/'.format(self.board.pk))
        self.assertEqual(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{}"'.format(board_topics_url))

    def test_new_topic_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'new_topic.html')

    def test_new_topic_view_contains_board_instance_in_context(self):
        self.assertEqual(self.response.context['board'], self.board)

