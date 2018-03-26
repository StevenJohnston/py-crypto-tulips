"""
Block Service Module
"""
from crypto_tulips.dal.services.redis_service import RedisService
from crypto_tulips.dal.services.block_service import BlockService as BlockServiceDal
from crypto_tulips.services.transaction_service import TransactionService
from crypto_tulips.services.contract_transaction_service import ContractTransactionService
from crypto_tulips.services.pos_transaction_service import PosTransactionService
from crypto_tulips.dal.objects.block import Block

import redis

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
        return block_service_dal.store_block(block)

    @staticmethod
    def get_max_height():
        """
        Method Comment
        """
        block_service_dal = BlockServiceDal()
        return block_service_dal.get_max_block_height()

    @staticmethod
    def verfiy_block(block):
        signature_valid = block.valid_signature()
        hash_valid = block.valid_hash()
        transactions_valid = BlockService.verify_transactions(block)
        return signature_valid and hash_valid and transactions_valid

    @staticmethod
    def remove_stale_blocks():
        """
        Removes stale, unused blocks.
        Blocks are removed if starting from the newest block, they do not appear when following the chain of previous blocks.
        ie.

        []<-[]<-[]<-[]<-[]<-[]<-[]<-[]<-[]<-[]
                    ^---[]<-[]<-[]<-[]<-[]

        In the above scenario, the bottom chain would be removed, moving all of those transactions back to the mempool.
        """
        block_dal = BlockServiceDal()
        current_height = block_dal.get_max_block_height()
        highest_blocks = block_dal.find_by_height(current_height)

        # if there is only 1 block at the greatest height, we can prune old blocks
        if len(highest_blocks) == 1:
            # get all block hashes
            all_block_hashes = block_dal.get_all_block_hashes()
            correct_block_hashes = set()
            block = highest_blocks[0]
            # add current highest block to the set of correct blocks
            correct_block_hashes.add(block._hash)
            # TODO while there is still a previous block
            while block.prev_block != 'GENESIS_BLOCK':
                block = block_dal.find_by_hash(block.prev_block)
                # add to list of correct blocks
                correct_block_hashes.add(block._hash)

            print("correct_block_hashes len: " + str(len(correct_block_hashes)))
            print("\t" + str(correct_block_hashes))
            # get the difference between the two sets of blocks
            to_remove = set(all_block_hashes) - correct_block_hashes
            print("to_remove: " + str(to_remove))
            # remove each of the blocks
            for block_hash in to_remove:
                print("Removing block: " + block_hash)
                BlockService._remove_block_by_hash(block_hash)

    @staticmethod
    def _remove_block_by_hash(block_hash):
        """
        Remove a block and restore it's transactions to the mempool.

        Parameters:
        block_hash  -- hash of block to remove
        """
        rs = RedisService()
        block_dal = BlockServiceDal()
        block = block_dal.find_by_hash(block_hash)

        # put all transaction types back into the mempool
        for transaction in block.transactions:
            TransactionService.add_to_mem_pool(transaction)
        for contract_transaction in block.contract_transactions:
            ContractTransactionService.add_to_mem_pool(contract_transaction)
        for pos_transaction in block.pos_transactions:
            PosTransactionService.add_to_mem_pool(pos_transaction)

        r = redis.StrictRedis()
        # remove from the sorted set of blocks
        r.zrem('blocks', block_hash)
        # remove from the set of blocks at it's height
        r.srem('block:' + str(block.height), block_hash)

        # delete the actual block
        rs.delete_by_key('block:' + block_hash)

    @staticmethod
    def get_last_block_hash():
        """
        Gets the highest block's hash.

        Returns:
        string  -- hash of the highest block
        """
        block_dal = BlockServiceDal()
        max_height = block_dal.get_max_block_height()
        latest_blocks = block_dal.find_by_height(max_height)
        if len(latest_blocks) != 0:
            return latest_blocks[0]._hash
        else:
            # TODO
            return 'GENESIS_BLOCK'

    @staticmethod
    def verify_transactions(new_block):
        block_service_dal = BlockServiceDal()
        transactions_before_block = block_service_dal.get_all_transaction_up_to_block(new_block.prev_block)

        duplicate_transaction = False
        signatures_valid = True
        hashes_valid = True
        # balance for each from_addr in new block
        balances = {}
        for block_transaction in new_block.transactions:
            # update address current balance
            balances[block_transaction.from_addr] = block_transaction.amount + balances.get(block_transaction.from_addr, 0)
            # check that the transaction isnt used in earlier block
            if block_transaction._hash not in transactions_before_block:
                duplicate_transaction = True
                # TODO add logger
            # signature validation
            if new_block.prev_block and not block_transaction.valid_signature():
                signatures_valid = False
            if not block_transaction.valid_hash():
                hashes_valid = False

        # update balances using all transaction from the past
        for key, transaction in transactions_before_block:
            if transaction.from_addr in balances:
                balances[transaction.from_addr] -= transaction.amount
            if transaction.to_addr in balances:
                balances[transaction.to_addr] += transaction.amount
        # not genesis block
        all_balance_positive = True
        if new_block.prev_block:
            # make sure each balance > 0
            for key, balance in balances:
                if balance < 0:
                    all_balance_positive = False
                    # TODO add logger
                    break
        return duplicate_transaction and all_balance_positive


    @staticmethod
    def get_transaction_balances():
        block_service_dal = BlockServiceDal()
        last_block_hash = BlockService.get_last_block_hash()
        transactions_before_block = block_service_dal.get_all_transaction_up_to_block(last_block_hash)

        balances = {}
        # update balances using all transaction from the past
        for key, transaction in transactions_before_block:
            balances[transaction.from_addr] = balances.get(transaction.from_addr, 0) - transaction.amount
            balances[transaction.to_addr] = balances.get(transaction.to_addr, 0) + transaction.amount
        return balances

    @staticmethod
    def get_all_balances(objects = None):
        if objects == None:
            block_dal = BlockServiceDal()
            last_block_hash = BlockService.get_last_block_hash()
            block = block_dal.find_by_hash(last_block_hash)
            objects = block_dal.get_all_objects_up_to_block(block)

        balances = {}

        print('------------TRANSACTION PAYOUT------------')
        # Transactions
        transaction_dict = objects.get('transactions', {})
        for transaction_hash in transaction_dict:
            transaction = transaction_dict.get(transaction_hash)
            balances[transaction.from_addr] = balances.get(transaction.from_addr, 0) - transaction.amount
            balances[transaction.to_addr] = balances.get(transaction.to_addr, 0) + transaction.amount


        print('------------POS TRANSACTION PAYOUT------------')
        # Proof of Stake Transactions
        pos_transaction_dict = objects.get('pos_transactions', {})
        for pos_transaction_hash in pos_transaction_dict:
            pos_transaction = pos_transaction_dict.get(pos_transaction_hash)
            balances[pos_transaction.from_addr] = balances.get(pos_transaction.from_addr, 0) - pos_transaction.amount


        print('------------SIGNED CONTRACT PAYOUT------------')

        # Signed Contracts
        signed_contract_dict = objects.get('signed_contracts', {})
        for signed_contract_hash in signed_contract_dict:
            signed_contract = signed_contract_dict[signed_contract_hash]
            balances[signed_contract.from_addr] = balances.get(signed_contract.from_addr, 0) - signed_contract.amount
            print('sc|| from:\t' + signed_contract.from_addr + ": balance:" + str(balances[signed_contract.from_addr]))
            balances[signed_contract._hash] = (balances.get(signed_contract._hash, (0, 0))[0] + signed_contract.amount, 0)
            print('sc|| parent:\t' + signed_contract._hash + ": balance:" + str(balances[signed_contract._hash]))



        print('------------CONTRACT TRANSACTION PAYOUT------------')
        # Contract Transactions
        contract_transaction_dict = objects.get('contract_transactions', {})

        temp_contracts = {}

        for key, contract_transaction in contract_transaction_dict.items():
            temp_contracts[contract_transaction.signed_contract_addr] = temp_contracts.get(contract_transaction.signed_contract_addr, list())
            temp_contracts[contract_transaction.signed_contract_addr].append(contract_transaction)

        unspent_cts = {}
        for signed_contract_addr in temp_contracts.keys():
            # sort by signed_contract_addr first, then to_symbol, then from_symbol, then price
            contract_transactions = sorted(temp_contracts[signed_contract_addr], key=lambda ct: (ct.signed_contract_addr, ct.timestamp))
            print('owner:' + signed_contract_addr + "  len=" + str(len(contract_transactions)))
            for contract_transaction in contract_transactions:
                if contract_transaction.from_symbol == 'TPS':
                    # remove from balance
                    print('\tFROM TPS| amount: ' + str(contract_transaction.amount) + ' @ ' + str(contract_transaction.price) + ' ct hash:' + contract_transaction._hash)

                    balances[contract_transaction.signed_contract_addr] = (balances.get(contract_transaction.signed_contract_addr, (0, 0))[0] - contract_transaction.amount, balances.get(contract_transaction.signed_contract_addr)[1] + contract_transaction.amount)

                    print('\t\t' + contract_transaction.signed_contract_addr + ": balance:" + str(balances[contract_transaction.signed_contract_addr]))

                    unspent_cts[signed_contract_addr] = unspent_cts.get(signed_contract_addr, list())
                    unspent_cts[signed_contract_addr].append(contract_transaction)
                elif contract_transaction.to_symbol == 'TPS':
                    print('\tTO TPS| amount: ' + str(contract_transaction.amount) + ' @ ' + str(contract_transaction.price) + ' ct hash:' + contract_transaction._hash)

                    # sort by price first
                    unspent_cts[signed_contract_addr].sort(key=lambda ct: ct.price)
                    amount_remaining = contract_transaction.amount
                    # iterate through copy of unspent_cts, removing as they are used up
                    for unspent_ct in unspent_cts[signed_contract_addr]:
                        # if took place before current contract transaction
                        if amount_remaining == 0:
                            break
                        if unspent_ct.timestamp <= contract_transaction.timestamp and unspent_ct.amount != 0:
                            if amount_remaining - unspent_ct.amount == 0:
                                print('\t\t->B:S')
                                # sell contract is used up, buy contract is used up
                                amount_remaining -= unspent_ct.amount
                                profit = contract_transaction.price / unspent_ct.price * unspent_ct.amount
                                print('\t\t' + str(contract_transaction.price) + "/" + str(unspent_ct.price) + "*" + str(unspent_ct.amount) + "=" + str(profit))
                                balances[contract_transaction.signed_contract_addr] = (balances[contract_transaction.signed_contract_addr][0] + profit, balances[contract_transaction.signed_contract_addr][1] - unspent_ct.amount)
                                print('\t\t' + contract_transaction.signed_contract_addr + ' amount: ' + str(balances.get(contract_transaction.signed_contract_addr)) + ' (added: ' + str(profit) + ")")
                                unspent_ct.amount = 0
                                break
                            elif amount_remaining - unspent_ct.amount > 0:
                                print('\t\t->B')
                                # sell contract is not used up, buy contract is used up
                                profit = contract_transaction.price / unspent_ct.price * unspent_ct.amount
                                print('\t\t' + str(contract_transaction.price) + "/" + str(unspent_ct.price) + "*" + str(unspent_ct.amount) + "=" + str(profit))
                                balances[contract_transaction.signed_contract_addr] = (balances[contract_transaction.signed_contract_addr][0] + profit, balances[contract_transaction.signed_contract_addr][1] - unspent_ct.amount)
                                print('\t\t' + contract_transaction.signed_contract_addr + ' amount: ' + str(balances.get(contract_transaction.signed_contract_addr)) + ' (added: ' + str(profit) + ")")
                                amount_remaining -= unspent_ct.amount
                                unspent_ct.amount = 0
                                continue
                            elif amount_remaining - unspent_ct.amount < 0:
                                print('\t\t->S')
                                # sell contract is used up, buy contract is not
                                profit = contract_transaction.price / unspent_ct.price * amount_remaining
                                print('\t\t' + str(contract_transaction.price) + "/" + str(unspent_ct.price) + "*" + str(amount_remaining) + "=" + str(profit))
                                balances[contract_transaction.signed_contract_addr] += (balances[contract_transaction.signed_contract_addr][0] + profit, balances[contract_transaction.signed_contract_addr][1] - amount_remaining)
                                print('\t\t' + contract_transaction.signed_contract_addr + ' amount: ' + str(balances.get(contract_transaction.signed_contract_addr)) + ' (added: ' + str(profit) + ")")
                                unspent_ct.amount -= amount_remaining
                                amount_remaining = 0
                                break

        # Terminated Contracts

        print('------------TERMINATED CONTRACT PAYOUT------------')
        term_contract_dict = objects.get('terminated_contracts', {})

        for signed_contract_addr in term_contract_dict.keys():
            print(signed_contract_addr + "||unspent cts len: " + str(len(unspent_cts.get(signed_contract_addr, []))))
            terminated_contract = term_contract_dict.get(signed_contract_addr)

            for unspent_ct in unspent_cts.get(signed_contract_addr, []):
                print('\thash:' + unspent_ct._hash + ' -> amount:' + str(unspent_ct.amount))
                if unspent_ct.timestamp <= terminated_contract.timestamp and unspent_ct.amount != 0:
                    profit = terminated_contract.price / unspent_ct.price * unspent_ct.amount
                    print('\t\t' + str(terminated_contract.price) + "/" + str(unspent_ct.price) + "*" + str(unspent_ct.amount) + "=" + str(profit))

                    balances[signed_contract_addr] = (balances[signed_contract_addr][0] + profit, balances[signed_contract_addr][1] - unspent_ct.amount)
                    unspent_ct.amount = 0
                    print('\t\t' + signed_contract_addr + ' amount: ' + str(balances.get(signed_contract_addr)) + ' (added: ' + str(profit) + ")")
            signed_contract = signed_contract_dict.get(signed_contract_addr, None)
            if signed_contract != None:
                base_amount = signed_contract.amount
                final_amount = balances[signed_contract_addr][0]
                profit = final_amount - base_amount
                print('----TOTAL PROFIT:' + str(profit))
                from_addr_profit = 0
                contract_owner_profit = 0
                if profit > 0:
                    # if profit was made, split profit among both accounts
                    # contract owner gets the profit at the specified rate
                    contract_owner_profit = profit * signed_contract.rate
                    # account that signed gets remaining profit
                    from_addr_profit = profit - contract_owner_profit
                else:
                    # if no profit was made, from_addr gets all of the money remaining
                    contract_owner_profit = 0
                    from_addr_profit = final_amount

                balances[signed_contract.parent_owner] = balances.get(signed_contract.parent_owner, 0) + contract_owner_profit
                print('-----' + signed_contract.parent_owner + ' amount: ' + str(balances.get(signed_contract.parent_owner)) + ' (added: ' + str(contract_owner_profit) + ")")
                balances[signed_contract.from_addr] = balances.get(signed_contract.from_addr, 0) + from_addr_profit
                print('-----' + signed_contract.from_addr + ' amount: ' + str(balances.get(signed_contract.from_addr)) + ' (added: ' + str(from_addr_profit) + ")")
                balances[signed_contract._hash] = 0


        # Contracts
        contract_dict = objects.get('contracts', {})

        # Owners
        print('------------MINER PAYOUT------------')
        owners = objects.get('owners', [])
        for owner in owners:
            balances[owner] = balances.get(owner, 0) + 10
            print('owner: ' + owner + ' amount: ' + str(balances[owner]) + ' (added: 10)')

        return balances
