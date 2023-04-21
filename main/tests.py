from django.test import TestCase
from django.test import Client
from database.models import Category, Equipment, Student, Reservation


# Create your tests here.
class ViewsTest(TestCase):
    def setUp(self):
        self.c = Client()

        # add category
        Category.objects.create(name='category1')
        Equipment.objects.create(serial_number='item1', category=Category.objects.get(name='category1'))
        Student.objects.create(id=123, name='student1')
    def test_category_view(self):
        response = self.c.get('/category/category1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog.html')
    def test_main_view(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_product_view(self):
        response = self.c.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products.html')

    def test_studio_view(self):
        response = self.c.get('/studio')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studio.html')

    def test_podcast_view(self):
        response = self.c.get('/podcast')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'podcast.html')

    def test_malfunction_view(self):
        response = self.c.get('/malfunction')
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
        self.assertEqual(Reservation.objects.get().date_from, '2020-01-01')

    def test_reservation_form(self):
        response = self.c.get('/category/details/item1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'details.html')
        self.assertContains(response, 'form')
        self.assertContains(response, 'item_serial_number')
        self.assertContains(response, 'date_from')
        self.assertContains(response, 'date_to')
