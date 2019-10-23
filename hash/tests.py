import hashlib
from time import sleep

from django.test import TestCase
from django.core.exceptions import ValidationError

from .forms import HashForm
from .models import Hash

from selenium import webdriver


class FunctionalTestCase(TestCase):
    def setUp(self):
        self.homepage = 'http://127.0.0.1:8000/'
        self.browser = webdriver.Firefox()
        self.browser.get(self.homepage)
        self.hello_sha256 = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'

    def test_html_homepage_rendered(self):
        self.assertIn('html homepage rendered', self.browser.page_source)
        self.assertIn('Enter Hash here:', self.browser.page_source)

    def test_hash_hello(self):
        text = self.browser.find_element_by_id('id_text')
        text.send_keys('hello')
        self.browser.find_element_by_name('submit').click()
        self.assertIn(self.hello_sha256, self.browser.page_source)

    def test_ajax_quickhash(self):
        self.browser.get(self.homepage)
        text = self.browser.find_element_by_id('id_text')
        text.send_keys('hello')
        sleep(0.5)
        self.assertIn(self.hello_sha256, self.browser.page_source)




    def tearDown(self):
        self.browser.quit()


class UnitTestCase(TestCase):
    
    def setUp(self):
        self.test_text = 'hello'
        self.test_text_hash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'

    def test_homepage_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'hash/home.html')

    def test_hash_form(self):
        form = HashForm(data={'test': 'hello'})
        self.assertTrue(form.is_valid)

    def test_hash_functions(self):
        self.assertEqual(
            self.test_text_hash,
            hashlib.sha256(b'hello').hexdigest()
        )

    def create_a_db_hash_record_n_return_it(self):
        new_hash = Hash()
        new_hash.text = self.test_text
        new_hash.sha256 = self.test_text_hash
        new_hash.save()
        return new_hash

    def test_hash_object(self):
        hash = self.create_a_db_hash_record_n_return_it()
        db_retrieved = Hash.objects.get(sha256=self.test_text_hash)
        self.assertEqual(db_retrieved.text, self.test_text)
        self.assertEqual(db_retrieved.sha256, self.test_text_hash)

    def test_hash_url(self):
        hash = self.create_a_db_hash_record_n_return_it()
        url = f'/sha256/{self.test_text_hash}'
        response = self.client.get(url)
        self.assertContains(response, self.test_text)

    def test_hash_model_validation(self):
        def make_invalid_hash_model_instance():
            row = Hash()
            row.text = self.test_text
            row.sha256 = self.test_text_hash + 'some_text!'
        self.assertRaises(ValidationError, make_invalid_hash_model_instance())

    def tearDown(self):
        pass

