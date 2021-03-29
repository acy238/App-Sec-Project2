from django.test import TestCase, Client
from LegacySite.models import Product, User
import unittest
from . import models, views
import codecs, json
from django.core.management import call_command


# Create your tests here.
class TestResponses(TestCase):
    #setUp
    def setUp(self):
        self.client = Client()
        #Adding product number 1 to our database
        prod = Product(product_name="NYU Apparel Card", product_image_path="/images/product_1.jpg", recommended_price=95, description="Use this card to buy NYU Clothing!")
        prod.save()
        #Adding user to our database
        res = self.client.post("/register", {"uname":"john", "pword":"john", "pword2":"john"})
        self.assertEqual(res.status_code, 302)
        u = User.objects.get(username="john")
        self.assertTrue(u.username=="john")
        #Adding admin to our database
        resAd = self.client.post("/register", {"uname":"admin", "pword":"admin", "pword2":"admin"})
        self.assertEqual(resAd.status_code, 302)
        uAd = User.objects.get(username="admin")
        self.assertTrue(uAd.username=="admin")
        
    #Testing for XSS, attack number 1
    def test_a1(self):
        res = self.client.get("/gift", {"director": "<script>alert("Hello")</script>"})
        self.assertEqual(res.status_code, 200)
        result = str(res.content, 'utf-8').find("<script>alert("Hello")</script>")
        self.assertEqual(result, -1)
        
    #Testing for unintended buy, attack number 2
    def test_a2(self):
        res = self.client.post('/gift/1', {"director": "%3Cscript%3Evar%20xhr%20=%20new%20XMLHttpRequest();%20xhr.open(%22POST%22,%20%22/gift/1%22,%20true);var%20data%20=%20new%20FormData();%20data.append(%27username%27,%27john%27);%20data.append(%27amount%27,333);%20data.append(%27product%27,%20%271%27);%20xhr.send(data);%3C/script%3E"})
        self.assertEqual(res.status_code, 302)
        
    #Testing for SQL injection in uploaded giftcard to retrieve admin user's salted password, related to both attack number 3 and number 4
    def test_a3(self):
        self.client.post("/login/", {"uname":"john", "pword":"john"})
        data = {}
        with open("salt.gftcrd", "rb") as giftcardfile:
            data["card_data"] = giftcardfile.read()
        res = self.client.post("/use.html", data)
        result = str(res.content, 'utf-8').find("000000000000000000000000000078d2$18821d89de11ab18488fdc0a01f1ddf4d290e198b0f80cd4974fc031dc2615a3")
        self.assertEqual(result, -1)
