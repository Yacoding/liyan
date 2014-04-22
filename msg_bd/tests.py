# -*- coding: utf-8 -*-

from django.test import LiveServerTestCase
from selenium import webdriver

from models import Msg


class MsgTest2(LiveServerTestCase):
    fixtures = ['admin_user.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        Msg(content="Test content", contact_email="test@test.com").save()

    def tearDown(self):
        # add refresh() to avoid error: [Errno 10054]
        self.browser.refresh()
        self.browser.quit()

    def test_msg(self):
        self.browser.get(self.live_server_url)
        # go to the msg_bd
        self.browser.find_element_by_id("msg_bd_index").click()
        self.browser.find_element_by_id("msg_bd")

        # check if the exist data in the database show properly
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn("Test content", body.text)

        # try to post a new msg
        self.browser.find_element_by_id("new_msg").send_keys("Test msg post content")
        self.browser.find_element_by_id("email").send_keys("test_post_new@test.com")
        self.browser.find_element_by_id("post_new_msg").click()

        # check if the new msg is now in database
        self.assertQuerysetEqual(Msg.objects.filter(content="Test msg post content", user_name="Anonymous",
                                                    contact_email="test_post_new@test.com"),
                                 ['<Msg: Anonymous:Test msg post content>'])

        # try to reply a msg
        test_reply_content = "Test msg reply"
        test_reply_email = "test_reply@test.com"
        self.browser.find_elements_by_class_name("msg_reply")[1].click()
        self.browser.find_element_by_id("new_msg").send_keys(test_reply_content)
        self.browser.find_element_by_id("email").send_keys(test_reply_email)
        self.browser.find_element_by_id("reply_msg").click()
        self.browser.switch_to_alert().accept()

        # check if the replied one correctly saved
        self.assertQuerysetEqual(Msg.objects.filter(content="reply to Anonymous:" + test_reply_content,
                                                    user_name="Anonymous",
                                                    contact_email=test_reply_email),
                                 ['<Msg: Anonymous:reply to Anonymous:' + test_reply_content + '>']
                                 )

        # try to delete a msg

        # check if delete successfully