from iconservice import Address
from iconservice.base.exception import DatabaseException, IconScoreException 
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

        def test_transfer(self):
                owner = self.test_account1
                to = self.test_account3
                value = 100
                #check balance
                inibalance_owner = self.score.balanceOf(owner)
                inibalance_receiver = self.score.balanceOf(to)
                print(f' Ini {inibalance_owner} // {inibalance_receiver}')
                # print(resu)
                self.set_msg(owner,value)
                self.score.transfer(to, value)
                #check the result
                fibalance_owner = self.score.balanceOf(owner)
                fibalance_receiver = self.score.balanceOf(to)
                print(f'Fin {fibalance_owner} // {fibalance_receiver}')
                self.assertEqual(fibalance_owner, inibalance_owner-value)
                self.assertEqual(fibalance_receiver, value)
        
        def test_negative_transfer(self):
                owner = self.test_account1
                to = self.test_account3
                value = -1
                self.set_msg(owner)
                with self.assertRaises(IconScoreException) as cm:
                        self.score.transfer(to, value) 
                self.assertEqual(cm.exception.message, 'Transferring value cannot be less than zero' )
        
        def test_out_of_balance(self):
                owner = self.test_account3
                to = self.test_account4
                value = 100
                self.set_msg(owner)
                with self.assertRaises(IconScoreException) as cm:
                        self.score.transfer(to, value) 
                self.assertEqual(cm.exception.message, 'Out of balance' )