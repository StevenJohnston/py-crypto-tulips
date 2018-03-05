"""
Block Service Module
"""
from crypto_tulips.dal.services.block_service import BlockService as BlockServiceDal
from crypto_tulips.dal.objects.block import Block

class BlockService():
    """
    Block Service
    """
    
    @staticmethod
    def add_block_to_chain(block):
        """
        Method Comment
        """
        block_service_dal = BlockServiceDal()
        block_service_dal.store_block(block)
        pass

    @staticmethod
    def verfiy_rsa(block):
        """
        Method Comment
        """
        pass

    @staticmethod
    def verify_block_author(block_author_public):
        pass

    @staticmethod
    def verify_ownership_of_funds(transactions):
        """
        todo check blockchain for each validation
        """
        pass