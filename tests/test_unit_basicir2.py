from iconservice import Address
from iconservice.base.exception import DatabaseException
from tbears.libs.scoretest.score_test_case import ScoreTestCase
from ..basic_irc2 import BasicIRC2

class TestSimple(ScoreTestCase):
        def setUp(self):
                super().setUp()
                self.score2 = self.get_score_instance(BasicIRC2, self.test_account1,
                                                        on_install_params={'_name':'Soi','_symbol':'Si','_initialSupply':10,'_decimals':12})
                self.test_account1 = Address.from_string(f"hx{'12345'*8}")
                self.test_account2 = Address.from_string(f"hx{'12534'*8}")
                # account_info = {
                #         self.test_account1: 0x9184e72a000,
                #         self.test_account2: 0}
                # self.initialize_accounts(account_info)

        def test_for_transfer(self):

                self.score2.transfer( "_to" : self.test_account2,"_value":65)
                self.score2.Transfer.assert_called_with(_to":self.test_account2, "_value":65)

#       def test_write_on_readonly(self):
#               self.assertRaises(DatabaseException, self.score2.write_on_readonly)
        def test_balace(self):
                owner = self.test_account1
                self.score2.balanceOf(owner)

        def test_total_supply(self):
                self.score2.totalSupply(self)

        