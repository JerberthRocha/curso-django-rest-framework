import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorBaseTest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorBaseTest):
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('email@email.com')

        callback(form)
        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Ex.: Michael')
            first_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Write your first name', form.text)
        
        self.form_field_test_with_callback(callback )

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Ex.: Scofield')
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Write your last name', form.text)
        
        self.form_field_test_with_callback(callback )

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form, 'Your username')
            username_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('This field must not be empty', form.text)
        
        self.form_field_test_with_callback(callback )
    
    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, 'Your e-mail')
            email_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('The e-mail must be valid.', form.text)
        
        self.form_field_test_with_callback(callback )
    
    def test_passwords_do_not_match(self):
        def callback(form):
            password1 = self.get_by_placeholder(form, 'Your password')
            confirm_password = self.get_by_placeholder(form, 'Repeat your password')
            password1.send_keys('P@ssw0rd')
            confirm_password.send_keys('P@ssw0rd_diff')

            form = self.get_form()

            self.assertIn('Password must have at least one uppercase letter,'
                          'one lowercase letter and one number. The length ' 
                          'should beat least 8 characters', 
                          form.text
            )
        
        self.form_field_test_with_callback(callback )
    
    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.get_by_placeholder(form, 'Ex.: Michael').send_keys('Teste First Name')
        self.get_by_placeholder(form, 'Ex.: Scofield').send_keys('Teste Last Name')
        self.get_by_placeholder(form, 'Your username').send_keys('testeusername')
        self.get_by_placeholder(form, 'Your e-mail').send_keys('teste@email.com')
        self.get_by_placeholder(form, 'Your password').send_keys('t3st3P@ssw0rd')
        self.get_by_placeholder(form, 'Repeat your password').send_keys('t3st3P@ssw0rd')

        form.submit()

        self.assertIn(
            'Your user is created. Please, log in.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )


