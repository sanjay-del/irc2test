import os

from iconsdk.builder.transaction_builder import (
    CallTransactionBuilder,
    DeployTransactionBuilder,
)
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.icon_service import IconService
from iconsdk.libs.in_memory_zip import gen_deploy_data_content
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.wallet.wallet import KeyWallet

from tbears.libs.icon_integrate_test import IconIntegrateTestBase, SCORE_INSTALL_ADDRESS

DIR_PATH = os.path.abspath(os.path.dirname(__file__))

class TestBasicIRC2(IconIntegrateTestBase):
    TEST_HTTP_ENDPOINT_URI_V3 = "http://127.0.0.1:9000/api/v3"
    SCORE_PROJECT = os.path.abspath(os.path.join(DIR_PATH, '..'))

    def setUp(self):
        super().setUp()

        self.icon_service = None
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
        self._score_address = self._deploy_score(params=params)['scoreAddress']

    def _deploy_score(self,to: str = SCORE_INSTALL_ADDRESS, params: dict = None) -> dict :
        transaction = DeployTransactionBuilder()\
                        .from_(self._test1.get_address()) \
                        .to(to) \
                        .step_limit(100_000_000_000) \
                        .nid(3) \
                        .nonce(100) \
                        .content_type("application/zip") \
                        .content(gen_deploy_data_content(self.SCORE_PROJECT)) \
                        .params(params) \
                        .build()
        signed_transaction = SignedTransaction(transaction, self._test1)
        tx_result = self.process_transaction(signed_transaction, self.icon_service)
        self.assertTrue('status' in tx_result)
        self.assertEqual(1, tx_result['status'])
        self.assertTrue('scoreAddress' in tx_result)
        return tx_result

    def test_score_update(self):
        # update SCORE
        tx_result = self._deploy_score(to=self._score_address)

        self.assertEqual(self._score_address, tx_result['scoreAddress'])

    def test_balanceOf(self):
        params = {
            "_owner" : self._test1.get_address()
        }
        transaction = CallBuilder() \
                        .from_(self._test1.get_address())\
                        .to(self._score_address) \
                        .method('balanceOf') \
                        .params(params) \
                        .build()
        
        response = self.process_call(transaction, self.icon_service)
        self.assertEqual(hex(self.initial_supply*10**self.decimals), response)

    def test_transfer(self):
        to = self._wallet_array[0].get_address()
        value = 100
        params = {
            '_to' : to,
            '_value': value
        }
        transaction = CallTransactionBuilder()\
                    .from_(self._test1.get_address())\
                    .to(self._score_address)\
                    .step_limit(10_000_000)\
                    .nid(3)\
                    .nonce(100)\
                    .method('transfer')\
                    .params(params)\
                    .build()
        signed_transaction = SignedTransaction(transaction,self._test1)
        result = self.process_transaction(signed_transaction, self.icon_service)
        self.assertTrue('status' in result)
        self.assertEqual(1, result['status'])
        
        print(f"StepCost for transafer {result['stepUsed']}")
        params = {
            "_owner" : to 
        }
        call = CallBuilder() \
                        .from_(self._test1.get_address())\
                        .to(self._score_address) \
                        .method('balanceOf') \
                        .params(params) \
                        .build()
        print(call)
        response = self.process_call(call, self.icon_service)
        self.assertEqual(hex(value), response)