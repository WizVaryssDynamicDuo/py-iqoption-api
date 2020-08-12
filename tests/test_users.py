import unittest
from pyiqoptionapi import IQOption
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
# 579121
email = "cayem28791@mail2paste.com"
password = "testerforapi2020"


class TestUsers(unittest.TestCase):

    def test_users(self):
        iq_api = IQOption(email, password)
        iq_api.connect()
        iq_api.change_balance("PRACTICE")
        self.assertEqual(iq_api.check_connect(), True)
        users = iq_api.get_leader_board('Worldwide', 1, 1, 0)
        iq_api.get_users_availability(30)
        self.assertTrue(type(iq_api.request_leaderboard_userinfo_deals_client(users['result']['positional']['1']['user_id'], users['result']['positional']['1']['flag'])) is dict)
        self.assertTrue(type(iq_api.get_user_profile_client(users['result']['positional']['1']['user_id'])) is dict)
