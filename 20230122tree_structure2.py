'''
TREEのデータ構造を扱うmodule
'''

from itertools import chain #リストを一次元化するときに使う

class BinaryNode:
    def __init__(self):
        self.root = None
        self.reft = None
        self.right = None

    def to_adress(self):
        '''
        そのNodeをrootとした時の、そのNodeの下に生えてる木全体をadressの集合として返してくれる。
        '''
        if not(self.reft) and (self.right):
            return [0]
        
        if not(self.reft):
            reft_adress = []
        else:
            reft_adress = self.left.to_adress()

        if not(self.right):
            right_adress = []
        else:
            reft_adress = self.right.to_adress()

        num = max(chain(*right_adress))+1
        
        for i in right_adress:
            i.append(num)

        return reft_adress + right_adress
    
    def to_list(self):




def adress_to_tree():
    '''
    adressの集合を渡された時、そのadressの集合に対応する木を返してくれる
    '''
    





class Node:
    def __init__(self):
        self.root = None
        self.next = []