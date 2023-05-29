import datetime

from django.test import TestCase,Client
from django.contrib.auth.models import User
from database.models import Category, Equipment, Student, Reservation
from main import views,models



# Create your tests here.
class ViewsTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

        # add category
        Category.objects.create(name='category1')
        Equipment.objects.create(serial_number='item1', category=Category.objects.get(name='category1'))
        Student.objects.create(id=123, full_name='student1' ,email='test@mail.com', phone_number=123456789, password='test')

        self.c = Client()
        self.c.login(username='test@mail.com', password='test')

    def test_category_view(self):
        response = self.c.get('/category/category1')
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'catalog.html')
    def test_main_view(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'base.html')


    def test_product_view(self):
        response = self.c.get('/categories')
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'products.html')

    def test_studio_view(self):
        response = self.c.get('/category/Studio')
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'studio.html')

    def test_podcast_view(self):
        response = self.c.get('/category/Podcast')
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'podcast.html')

    def test_malfunction_view(self):
        response = self.c.get('/malfunction/item1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'malfunction.html')

    def test_item_view(self):
        # add item
        response = self.c.get('/category/details/item1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'details.html')
    def test_item_detail_post(self):
        response = self.c.post('/category/details/item1', {'date_from': '2020-01-01', 'date_to': '2020-01-02'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'details.html')
        # check if reservation created
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Reservation.objects.get().date_from, datetime.date(2020, 1, 1))

    def test_reservation_form(self):
        response = self.c.get('/category/details/item1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'details.html')
        self.assertContains(response, 'form')
        self.assertContains(response, 'item')
        self.assertContains(response, 'date_from')
        self.assertContains(response, 'date_to')

    def test_history(self):
        self.c.logout()
        self.c.login(username="admin", password="admin")

        student = Student.objects.create(id=312, full_name='milky', email='milky@gmail.com', phone_number=123456789,
                               password='test')
        # student.save()

        response = self.c.post('/history/milky@gmail.com')
        self.assertEqual(response.status_code, 200)


    def test_statistics(self):
        self.c.logout()
        self.c.login(username="admin", password="admin")
        response = self.c.get('/statistics')
        self.assertEqual(response.status_code, 200)

    def test_policy(self):
        response = self.c.get('/policy')
        self.assertEqual(response.status_code, 200)