# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from accounts.models import User
from liyan.settings import NEED_CONFIRM_EMAIL


class AccountsTest(TestCase):
    username = "test_user"
    email = "test@test.com"
    password = "111111"

    def test_valid_register(self):
        response = self.client.post(reverse('accounts:register'),
                                    {'username': self.username, 'email': self.email, 'password': self.password})
        # 测试是否重定向
        self.assertEqual(response.status_code, 302)
        # 测试数据库是否写入正确数据
        user = User.objects.filter(username=self.username, email=self.email)
        self.assertQuerysetEqual(user, ['<User: ' + self.username + "-" + self.email + '>'])
        # 测试重定向路径是否正确
        self.assertRedirects(response, reverse("accounts:login"))

    def test_valid_login(self):
        self.test_valid_register()
        User.objects.update(is_active=True)
        response = self.client.post(reverse('accounts:login'), {'email': self.email, 'password': self.password})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:index"))

    def test_valid_logout(self):
        self.test_valid_login()
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:index"))

    def test_go_to_index(self):
        self.test_valid_login()
        response = self.client.post(reverse("accounts:index"))
        self.assertEqual(response.status_code, 200)

    def test_valid_check_detail(self):
        self.test_valid_login()
        response = self.client.post(reverse("accounts:check_detail"),
                                    {'username': self.username + '1', 'email': self.email})
        user = User.objects.filter(username=self.username + '1', email=self.email)
        self.assertQuerysetEqual(user, ['<User: ' + self.username + "1-" + self.email + '>'])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:index'))

    def test_valid_reset_password(self):
        new_password = "222222"
        self.test_valid_login()
        response = self.client.post(reverse("accounts:reset_password"),
                                    {"old_password": self.password, "new_password": new_password})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:index'))
        response = self.client.post(reverse('accounts:login'), {'email': self.email, 'password': new_password})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:index"))

    def test_active_after_register(self):
        self.test_valid_register()
        if NEED_CONFIRM_EMAIL:
            response = self.client.post(reverse('accounts:login'), {'email': self.email, 'password': self.password})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, '账户尚未激活，请激活后登陆')
            User.objects.filter(email=self.email).update(is_active=True)
        response = self.client.post(reverse('accounts:login'), {'email': self.email, 'password': self.password})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:index"))