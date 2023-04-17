'''
TREEのデータ構造を扱うmodule
'''

from itertools import chain #リストを一次元化するときに使う

class List_Adress_Tree:
    '''
    旧来のプログラムで使っていた、リスト表記によるAdressを、人権が認められる記法で分かりやすく扱うためのクラス
    
    0付きの木であることを勝手に前提として書くからね。
    (0付きの木以外は、勝手に冒頭にzeroを付加して形式を整えるぞ)
    (今までよくこんなキモい記法で書いてきたもんだ)

    List_Adress_Tree()は、基本的には、BinaryTreeと同値な対象を表現するための一つの簡便的な表示法であり、木のそれぞれの葉のadressの集合によって木構造を暗に示す。
    ただし、中間の枝に関する情報は持っていないため、曖昧性がある。
    '''

    def __init__(self,adresses):

        self.adresses = adresses

    def max_adress(self):
        '''
        この木のrootに該当するadressの数字を求める
        '''
        return max(chain(*self.adresses))


    def left(self):
        '''
        木の左を返す
        '''
        if len(self.adresses)==0:
            return []
        
        num=self.max_adress()
        return List_Adress_Tree(adresses=[x for x in self.adresses if not num in x])


    def right(self):
        '''
        木の右を返す
        '''
        if len(self.adresses)==0:
            return []
        
        num=self.max_adress()
        return List_Adress_Tree(adresses=[[y for y in x if y!=num] for x in self.adresses if num in x])


    def adress_to_tree(self):
        '''
        0付きのadressの集合を渡された時、そのadressの集合に対応するBinaryTreeのrootを返してくれる
        ちなみに、この旧来のやり方では、左の木に関しては中間の空白が削除されてるけどなんか文句あるか
        '''
        adress = self.adresses

        if not len(adress):
            return None
        
        if len(adress) == 1:
            return BinaryNode()

        
        root = BinaryNode()

        num = max(chain(*adress))

        root.left = self.left().adress_to_tree()
        root.right = self.left().adress_to_tree()



    def adress_to_tree2(self):
        '''
        0付きのadressの集合を渡された時、そのadressの集合に対応するBinaryTreeのrootを返してくれる
        この書き方だと、BinaryNode.to_adress()正確に元の木に戻ってくると思う。
        '''

        root = BinaryNode()

        for listadress in (self.adresses):
            path = Path(listadress)
            top_num = self.max_adress()
            path.to_adress(top_num)
            root.make_path(path) 

        return root


    def make_time_list(self):
        '''
        元のモジュールへの埋め込み。
        与えられたlist のorg_treeを、2-変換代数で計算して、再び結果をlistとして出力する。
        '''

        org_binary_node = self.adress_to_tree2()


        org_binary_node.double_trans_alg()

        org_binary_node.sister[0].search_leafs()
        time_list = []
        org_binary_node.search_vals(time_list)

        return time_list
    

class Path:
    '''
    pathとは、旧来のlistタイプのadressには(0とNoneを同一視しててキモイなどの点で)人権がないので、pathという新しいツールに進化させて人権を獲得したものである。
    
    pathは、木の中での(通常はrootからの)相対的な位置関係を表す。
    
    pathは以下のような記述ルールに基づいて書かれる。
    [an…a3,a2,a1]というリストが渡された時、rootから、a1番目、a2番目,,,というnodeを辿って行ったときに辿りつけるnodeが、現在のnodeである。

    最初の桁に小構造が、最後の桁に大構造が入っている(パリ式の住所)
    '''

    def __init__(self,adress=[]):
        self.adress = adress

    def to_adress(self,top_num):
        '''
        List_Adressをpathに変換するためのツール。
        ただし、List_Adress_Treeにおいて曖昧であった、top_numという標識を補う必要がある。
        top_numとは、List_Adress_Treeの最大の数字のことである。
        '''
        new_adress = []

        for i in range(top_num):
            j = i+1
            if j in self.adress:
                new_adress.append(1)
            else:
                new_adress.append(0)

        self.adress = new_adress

    def to_bool(self):
        '''
        変換代数に用いる。
        adressの値から、縮約、非縮約を決定するbool値を返す。
        '''

        #ここには変換代数としての任意性がある
        depth = len(self.adress)

        return (depth%2)#深度の偶奇で縮約、非縮約を分ける   bool(random.getrandbits(1))

    def left(self):
        '''
        そのパスの左のパスを返す
        '''
        return Path([0]+self.adress)
    
    def right(self):
        '''
        そのパスの右のパスを返す
        '''
        return Path([1]+self.adress)



class BinaryNode:
    '''
    二分木構造。
    一般の根付き木を使いたい場合にはNodeを使用すること。
    '''
    def __init__(self):
        self.root = None
        self.left = None
        self.right = None


    def to_adress(self):
        '''
        そのNodeをrootとした時の、そのNodeの下に生えてる木全体をlist_adressの集合として返してくれる。
        戻り値top_numは、その木全体の深さを示す。
        '''

        if not(self.left) and (self.right):
            return [[0]]
        
        if not(self.left):
            left_adress = [[0]]
        else:
            left_adress, left_top_num = self.left.to_adress()

        if not(self.right):
            right_adress = [[0]]
        else:
            right_adress, right_top_num = self.right.to_adress()

        top_num = max([left_top_num,right_top_num])+1
        
        for i in right_adress:
            i.append(top_num)

        return (left_adress + right_adress) , top_num

    def make_right(self):
        '''
        右にノードを追加する
        '''
        if not(self.right):
            self.right = BinaryNode()
        
        return self.right
    
    def make_left(self):
        '''
        左にノードを追加する
        '''
        if not(self.left):
            self.left = BinaryNode()
        
        return self.left

    def make_path(self,path):
        '''
        パスというオブジェクトが渡された時、そのnodeからパスに該当する葉と、その葉への最小限の経路を木に追加する。
        最後にその追加された葉を返す
        '''

        if len(path.adress) == 0:
            return self
        
        next_node = BinaryNode()

        if path.adress[-1] == 0:
            if self.left:
                next_node = self.left
            else:
                next_node = BinaryNode()
                self.left = next_node

        elif path.adress[-1] == 1:
            if self.right:
                next_node = self.right
            else:
                next_node = BinaryNode()
                self.right = next_node

        else:
            print('エラー、二分木のパスには0か1の値を入れてください')

        next_node.root =self
        next_node.make_path(Path(path.adress[:-1]))
        return None
    

    def get_root(self):
        '''
        そのnodeの大元のrootとなるnodeを求める。
        '''
        if self.root:
            return self.root.get_root()
        else:
            return self
        

    def get_path(self):
        '''
        rootに対して適用せよ。
        rootから下の木全てについて絶対パスを求める。パスはself.pathとしてPathオブジェクトで設定される。
        '''
        #selfのpathを設定する
        if not(self.root):
            self.path = Path([])

        else:
            if self.root.right == self:
                self.path = self.root.path.right()

            elif self.root.left == self:
                self.path = self.root.path.left()

            else: print("error")

        #selfの下のpathを設定する
        if self.right:
            self.right.get_path()
        if self.left:
            self.left.get_path()

        return None
    
    def set_path(self):
        '''
        その木全体のnodeにパスを設定する
        '''
        my_root = self.get_root()
        my_root.get_path()

        return None

    def make_copy_node(self):
        '''
        rootに対して適用せよ。その木の各nodeにコピーを作る。
       
        コピーする木にはself.sisterという写像がついていて、娘のnodeの"リスト"を覚えている。
        コピーされた木のnodeには、self.motherという写像がついていて、母親のnodeを覚えている。
        '''

        copy_root = Node()

        self.sister = [copy_root]
        copy_root.mother = self
        

        if self.left:
            self.left.make_copy_node()
        if self.right:
            self.right.make_copy_node() 

        return None


    def make_copy_tree(self):
        '''
        その木全体の、根付き木としてのコピーを作る。
        '''

        org_root = self.get_root()
        org_root.make_copy_node()


        org_root.sister[0].set_copy_nexts()

        return org_root.sister[0]
    

    def double_trans_alg(self):
        '''
        2-変換代数
        この処理についてはノートの三角形図式を参照

        結果的に、sisterのtreeは破壊されてminitreeとなり、motherのtreeの葉のsister写像には求めるminitreeの葉の冪への写像が入っている。        
        '''
        self.make_copy_tree()
        self.set_path()

        org_root = self#.get_root()
        org_root.do_trans_from_bottom()

        return org_root.sister[0]

    def do_trans_from_bottom(self):
        '''
        帰りがけ順でsisterに縮約情報を送る
        '''

        if self.left:
            self.left.do_trans_from_bottom()
        if self.right:
            self.right.do_trans_from_bottom()

        if self.path.to_bool():##################################debugここをFalseにするとバグが消える、（つまりこの先の四角形図式でバグが起きてる）（ここよりもっと先まで検証が進んでいます）
            self.sister[0].do_contraction()

        return None
    
    def pull_buck(self):
        '''
        三角図式の縦方向の運動で、"葉について"、org_treeからcopy_treeへのsister写像を更新する
        '''

        if (not self.right) and (not self.left):  
            self.sister = [x.co_brother for x in self.sister]
            self.sister = chain(*self.sister)

        if self.left:
            self.left.pull_buck()
        if self.right:
            self.right.pull_buck()

            
    def search_vals(self,time_list):
        '''
        葉に含まれる値を検索する
        '''
        if (not self.right) and (not self.left):
            time_list.append(x.val for x in self.sister)

        if self.left:
            self.left.search_vals(time_list)
        if self.right:
            self.right.search_vals(time_list)

        return time_list

class Node:
    '''
    根付き木構造
    '''
    def __init__(self):
        self.root = None
        self.next = []

    def set_copy_nexts(self):
        '''
        BinaryNodeでmake_copy_treeした時に使う。
        コピーされた木に、コピー前の木と同じ連結構造を作る。
        '''
        org_root = self.mother

        if org_root.left:
            self.next.append(org_root.left.sister[0])
            org_root.left.sister[0].root = self
            org_root.left.sister[0].set_copy_nexts()

        if org_root.right:
            self.next.append(org_root.right.sister[0])
            org_root.right.sister[0].root = self
            org_root.right.sister[0].set_copy_nexts()

        return None
    
    def do_contraction(self):
        '''
        指定されたnode(self)について、その下のsub_tree間で1_変換代数を行う
        パターンB(ノート参照)の、上詰めアルゴリズムである。
        '''
        if len(self.next) == 0:
            return None
        

        '''
        if len(self.next) == 1:
            if False and self.root:#上詰め
                self.root.next[self.root.next.index(self)] = self.next#######################ここにバグがあります！

            return None
        '''

        if len(self.next) == 2:
            left_tree = self.next[0]
            right_tree = self.next[1]


            copy_left_tree = left_tree.double_trans_alg()#copy_left_treeはSubNode
            copy_right_tree = right_tree.double_trans_alg()#copy_right_treeはSubNode


            #ここで、left_treeを固定した上で、right_treeをleft_treeに引き戻す写像を構成する。
            #ここが時間構造関数の中核だぜーーー
            
            #楽しい楽しい時間構造関数の旅へ行ってらっしゃい！！！！！！！！！！！！！！！！！！！
            #print(['before_number',len(right_tree.search_leafs())])
            #print(['co_bro_number', len(copy_right_tree.search_leafs()) ])


            copy_right_tree.make_co_brother()
            copy_left_tree.make_brother(copy_right_tree)

            #right_tree.print_leafs_sisters()###################debug

            #四角形図式の射を合成して、 copy_left_treeの葉をcopy_right_treeの葉に引き戻す写像を作る。
            right_tree.pull_buck()

            self.next.remove(right_tree)
            right_tree.mother.pull_buck()#right_tree.motherはBinaryNode



    def pull_buck(self):
        '''
        copy_tree達にbrother写像が作られているとき、"葉について"、left_treeからright_treeへの引き戻しとなるco_brother写像を構成する。
        '''

        #print('pullbuck')
        if len(self.next) == 0:
            #print('leaf')
            self.co_brother = [x.mother for x in self.sister[0].co_brother]
            '''
            print('debug')
            print(self)
            print(self.sister)
            '''
            
            '''
            self.co_brother = [[y.mother for y in x.co_brother] for x in self.sister]
            self.co_brother = chain(*self.co_brother)
            '''


        for i in self.next:
            i.pull_buck()


    def get_root(self):
        '''
        そのnodeの大元のrootとなるnodeを求める。
        '''
        if self.root:
            return self.root.get_root()
        else:
            return self
        
    def get_path(self,my_root):
        '''
        rootに対して適用せよ。
        rootから下の木全てについて絶対パスを求める。パスはself.pathとしてPathオブジェクトで設定される。
        '''
        #selfのpathを設定する
        if self == my_root:
            self.path = Path([])

        else:
            conode_num = len(self.root.next)

            for i in range(conode_num):
                if self.root.next[i] == self:
                    self.path = Path( [conode_num] + self.root.path.adress )

        #selfの下のpathを設定する
        for next_node in self.next:
            next_node.get_path(my_root)

        return None
    
    def set_path(self):
        '''
        その木全体のnodeにパスを設定する
        '''
        my_root = self
        my_root.get_path(my_root)

        return None

    def make_copy_node(self):
        '''
        rootに対して適用せよ。その木の各nodeにコピーを作る。
       
        コピーする木にはself.sisterという写像がついていて、娘のnodeの"リスト"を覚えている。
        コピーされた木のnodeには、self.motherという写像がついていて、母親のnodeを覚えている。
        '''

        copy_root = SubNode()

        self.sister = [copy_root]
        copy_root.mother = self
        
        for next_node in self.next:
            next_node.make_copy_node()

        return None           

    def make_copy_tree(self):
        '''
        その木全体の、根付き木としてのコピーを作る。
        '''

        org_root = self#.get_root()
        org_root.make_copy_node()

        org_root.sister[0].set_copy_nexts()

        return org_root.sister[0]



    def double_trans_alg(self):
        #print('double_trans_alg')
        #print(['right_leaf',len(self.search_leafs())])
        '''
        2-変換代数
        この処理についてはノートの三角形図式を参照

        結果的に、sisterのtreeは破壊されてminitreeとなり、motherのtreeの葉のsister写像には求めるminitreeの葉の冪への写像が入っている。        
        '''
        self.make_copy_tree()
        self.set_path()

        #print(['new_copy',len(self.sister[0].search_leafs())])

        org_root = self#.get_root()
        org_root.do_trans_from_bottom(org_root)


        #self.print_leafs_sisters()###################debug
        return org_root.sister[0]


    def do_trans_from_bottom(self,my_root):
        '''
        帰りがけ順でsisterに縮約情報を送る
        '''
        
        for nodes in self.next:
            nodes.do_trans_from_bottom(my_root)

        if self.path.to_bool():########################################debugここをfalseにするとバグが消える！！！

            #print(['before_do_const',len(my_root.sister[0].search_leafs())])
            self.sister[0].do_contraction(my_root)
            #print(['after_do_const',len(my_root.sister[0].search_leafs())])

        return None


    def search_leafs(self):
        '''
        その木の全ての葉を検索してリストにする。また、self.valに対して整列順序を入れる。
        '''
        leafs = []

        self.append_leafs(leafs)

        #if False:
        for number in range(len(leafs)):
            leafs[number].val=number*(1/4)

        return leafs

    def append_leafs(self,leafs):

        if len(self.next) ==0:
            leafs.append(self)

        for i in self.next:
            i.append_leafs(leafs)

        return None



    def print_leafs_sisters(self):
        '''
        デバッグツール。right_treeに対して適用し、対応する木の葉にco_brotherが入っているかどうかを確認せよ。
        '''
        if len(self.next) ==0:
            print(self.sister[0].__dict__.items())
            if not 'co_brother' in  self.sister[0].__dict__.keys():
                print('NO_CO_BRO!!!!!!!!!!')
                #print(self.mother.sister[0].__dict__.items())

        for i in self.next:
            i.print_leafs_sisters()




class SubNode(Node):

    def set_copy_nexts(self):
        '''
        Nodeでmake_copy_treeした時に使う。
        コピーされた木に、コピー前の木と同じ連結構造を作る。
        '''
        org_root = self.mother

        for next_node in org_root.next:
            self.next.append(next_node.sister[0])
            next_node.sister[0].root = self
            next_node.sister[0].set_copy_nexts()

        return None
    
    def do_contraction(self,my_root):
            #print(['left_leaf',len(my_root.search_leafs())])
            '''
            指定されたnode(self)について、その下のsub_tree間で1_変換代数を行う
            パターンB(ノート参照)の、上詰めアルゴリズムである。
            '''
            

            if self==my_root:
                return None

            elif len(self.next) == 0:
                return None


            else:# len(self.next) >= 1:
                #print(len(self.root.next))

                #self.root.next += list(chain(*[x.next for x in self.next]))
                self.root.next += self.next
                self.root.next.remove(self)

                #print(len(self.root.next))
                for x in self.root.next:
                    x.root = self.root
                return None
            '''
            if len(self.next) == 1:
                if False:#上詰め
                    self.root.next[self.root.next.index(self)] = self.next################ここにバグがあります！
                return None
            '''

            '''
            if len(self.next) == 2:
                left_tree = self.next[0]
                right_tree = self.next[1]

                self.root.next = left_tree.next + right_tree.next
                print([len(self.root.next)])
                return None
            
            '''



    def make_brother(self,copy_right_tree):
        '''
        左の木から、右の木に対して、引き戻し兄弟写像を作る。
        '''

        #return None #########debug

        self.brother = copy_right_tree
        copy_right_tree.co_brother.append(self)

        pattern = 1


        if pattern ==1:
            right_next_number = len(copy_right_tree.next)
            left_next_number = len(self.next)


            if right_next_number==0:
                for i in range(left_next_number):
                    self.next[i].make_brother(copy_right_tree)
                return None

            for i in range(left_next_number):
                self.next[i].make_brother(copy_right_tree.next[i%right_next_number])
            return None


    def make_co_brother(self):
        '''
        copy_right_treeの”葉”に、make_brother関数で使うco_brother変数を準備する
        '''

        #if self.next==None:
        self.co_brother = []
        

        for x in self.next:
            x.make_co_brother()

        '''
        for y in [x.sister[0] for x in self.mother.next]:
            y.make_co_brother()
        '''

        return None
    
    def search_leafs(self):
        '''
        その木の全ての葉を検索してリストにする。
        '''
        leafs = []

        self.append_leafs(leafs)

        return leafs

    def append_leafs(self,leafs):

        if len(self.next) ==0:
            leafs.append(self)

        for i in self.next:
            i.append_leafs(leafs)

        return None
    
