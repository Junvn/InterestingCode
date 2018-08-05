#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:janvn
# datetime:18-8-4 上午9:27
# software:PyCharm

import json
import hashlib
from time import time
from flask import Flask,jsonify,request
from uuid import uuid4
from textwrap import dedent
from urllib.parse import urlparse
import requests

class BlockChain(object):
    '''
    负责管理链
    '''

    def __init__(self):
        '''
        初始构造函数
        :param self:
        :return:
        '''
        self.chain=[] #存储区块链
        self.current_transactions=[] #保存交易

        #创建一个创世区块
        self.new_block(previous_hash=1,proof=100)

        self.nodes = set()


    def new_block(self,proof,previous_hash=None):
        '''
        创建新的区块并且增加其到链
        :param proof:<int> The proof given by the Proof of work algorithm
        :param previous_hash:(Optional) <str> Hash of previous Block
        :return:<dict> New Block
        '''
        block = {

            'index':len(self.chain),
            'timestamp':time(),
            'transactions':self.current_transactions,
            'proof':proof,
            'previous_hash':previous_hash or self.hash(self.chain[-1])
        }

        # Reset the current list of transaction
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self,sender,recipient,amount):
        '''
        增加新的交易到交易列表中
        :param sender: <str> Address of the Sender
        :param recipient: <str> Addresss of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        '''

        self.current_transactions.append({
            'sender':sender,
            'recipient':recipient,
            'amount':amount
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        '''
        Creates a SHA-256 hash of a Block
        Hashes a Block   对一个块进行哈希
        :param block:<dict> Block
        :return:<str>
        '''

        #We must make sure that the Dictionary is Ordered,or we'll have inconsistent hashes
        block_string = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        '''
        返回链中的最后一个块
        :return:
        '''
        return self.chain[-1]


    def proof_of_work(self,last_proof):
        '''

        :param last_proof:
        :return:
        '''

        proof = 0
        while self.valid_proof(last_proof,proof) is False:
            proof += 1

        return proof


    @staticmethod
    def valid_proof(last_proof,proof):
        '''

        :param last_proof:
        :param proof:
        :return:
        '''
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def register_node(self,address):
        '''
        新增节点到节点列表中
        :param address:
        :return:
        '''

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)


    def valid_chain(self,chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print('\n------------------\n')

            if block['previous_hash'] != self.hash(last_block):
                return False

            if not self.valid_proof(last_block['proof'],block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        '''
        一致性算法
        :return:
        '''

        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)


        for node in neighbours:

            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False


# Instantiate our Node
app = Flask(__name__)

#Generate a globally unique address for this node
node_indentifier = str(uuid4()).replace('-','')

# Instantiate the Blockchain
blockchain = BlockChain()


@app.route('/mine',methods=['GET'])
def mine():
    '''
    挖矿
    :return:
    '''
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender='0',
        recipient=node_indentifier,
        amount=1,
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof,previous_hash)

    response = {
        'message':'New Block Forged',
        'index':block['index'],
        'transaction':block['transactions'],
        'proof':block['proof'],
        'previous_hash':block['previous_hash'],
    }

    return jsonify(response),200
    #return "We'll mine a new Block"

@app.route("/transactions/new",methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender','recipient','amount']
    if not all(k in values for k in required):
        return 'Missing values',400

    #create a new transaction
    index = blockchain.new_transaction(values['sender'],values['recipient'],values['amount'])

    response = {'message':f'Transaction will be added to Block {index}'}
    return jsonify(response),201


@app.route('/chain',methods=['GET'])
def full_chain():
    response = {
        'chain':blockchain.chain,
        'length':len(blockchain.chain),
    }

    return jsonify(response),200

@app.route('/nodes/register',methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return 'Error: Please supply a valid list of nodes', 400

    for node in nodes:
        blockchain.register_node(node)

    response = {

        'message':'New nodes have been added',
        'total_nodes':list(blockchain.nodes),

    }

    return jsonify(response),201

@app.route('/nodes/resolve',methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message':'Our chain was replaced',
            'new_chain':blockchain.chain
        }

    else:
        response = {
            'message':'Our chain is authoritative',
            'chain':blockchain.chain
        }

    return jsonify(response),200

if __name__ == '__main__':

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
