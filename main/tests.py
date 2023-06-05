"""Tests for main app."""
# pylint: disable=E1101
import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User
from database.models import Category, Equipment, Student, Reservation



class ViewsTest(TestCase):
    """
    Test class for views in the main app.
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

        # add category
        Category.objects.create(name='category1')
        Equipment.objects.create(
            serial_number='item1',
            category=Category.objects.get(name='category1')
        )
        Student.objects.create(
            id=123,
            full_name='student1',
            email='test@mail.com',
            phone_number=123456789,
            password='test'
        )

        self.client = Client()
        self.client.login(username='test@mail.com', password='test')

    def test_category_view(self):
        """
        Test category view.
        """
        response = self.client.get('/category/category1')
        self.assertEqual(response.status_code, 200)

    def test_main_view(self):
        """
        Test main view.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_view(self):
        """
        Test product view.
        """
        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 200)

    def test_studio_view(self):
        """
        Test studio view.
        """
        response = self.client.get('/category/Studio')
        self.assertEqual(response.status_code, 200)

    def test_podcast_view(self):
        """
        Test podcast view.
        """
        response = self.client.get('/category/Podcast')
        self.assertEqual(response.status_code, 200)

    def test_malfunction_view(self):
        """
        Test malfunction view.
        """
        response = self.client.get('/malfunction/item1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'malfunction.html')

    def test_item_view(self):
        """
        Test item view.
        """
        response = self.client.get('/category/details/item1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'details.html')

    def test_item_detail_post(self):
        """
        Test item detail post.
        """
        response = self.client.post(
            '/category/details/item1',
            {'date_from': '2020-01-01', 'date_to': '2020-01-02', 'time_from': '12:00', 'time_to': '13:00'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'details.html')

        # check if reservation created
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Reservation.objects.get().date_from, datetime.date(2020, 1, 1))

    def test_reservation_form(self):
        """
        Test reservation form.
        """
        response = self.client.get('/category/details/item1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'details.html')
        self.assertContains(response, 'form')
        self.assertContains(response, 'item')
        self.assertContains(response, 'date_from')
        self.assertContains(response, 'date_to')

    def test_history(self):
        """
        Test history.
        """
        self.client.logout()
        self.client.login(username="admin", password="admin")

        Student.objects.create(
            id=312,
            full_name='milky',
            email='milky@gmail.com',
            phone_number=123456789,
            password='test'
        )

        response = self.client.post('/history/milky@gmail.com')
        self.assertEqual(response.status_code, 200)

    def test_statistics(self):
        """
        Test statistics.
        """
        self.client.logout()
        self.client.login(username="admin", password="admin")
        response = self.client.get('/statistics')
        self.assertEqual(response.status_code, 200)

    def test_policy(self):
        """
        Test policy.
        """
        response = self.client.get('/policy')
        self.assertEqual(response.status_code, 200)
