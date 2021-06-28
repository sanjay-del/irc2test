from iconservice import Address
from iconservice.base.exception import DatabaseException
from tbears.libs.scoretest.score_test_case import ScoreTestCase
from ..basic_irc2 import BasicIRC2

class TestSimple(ScoreTestCase):
        def setUp(self):
                super().setUp()
                self.name = 'Neps'
                self.symbol='nps'
                self.initial_supply = 10
                self.decimals = 10
                params =  {
                "_name": self.name,
                "_symbol": self.symbol,
                "_initialSupply": self.initial_supply,
                "_decimals": self.decimals
                }
                self.score = self.get_score_instance(BasicIRC2, self.test_account1,
                                                        on_install_params=params)
                self.test_account3 = Address.from_string(f"hx{'12345'*8}")
                self.test_account4 = Address.from_string(f"hx{'12534'*8}")
                # account_info = {
                #          self.test_account3: 10*10,
                #          self.test_account4: 10**12}
                # self.initialize_accounts(account_info)

        
        
        # def test_for_transfer(self):
        #         self.score.transfer('_to':self.test_account4, 'value':100)
        #         self.score.Transfer.assert_called_with(params)

# #       def test_write_on_readonly(self):
# #               self.assertRaises(DatabaseException, self.score.write_on_readonly)
        # def test_balace_initially(self):
        #         balance = 10*10**10
        #         owner = self.test_account1
        #         res = self.score.balanceOf(owner)
        #         self.assertEqual(res,balance)

        def test_total_supply(self):
                # balance = self.initial_supply * 10 ** self.decimals
                # value = self.score.totalSupply()
                self.assertEqual(self.initial_supply * 10 ** self.decimals, self.score.totalSupply())
        
        def test_symbol(self):
                # print(self.test_account3)
                # balance_3 = self.get_balance(self.test_account3)
                # print(balance_3)
                self.assertEqual(self.symbol, self.score.symbol())

        # def test_transfer(self):
        #         to = self.test_account3
        #         value = 100
        #         params = {
        #         '_to': to, 
        #         '_value': value
        #         }
        #         self.score.transfer('_to': to, 
        #         '_value': value)
