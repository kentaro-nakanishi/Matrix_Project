'''
TREEのデータ構造を扱うmodule
'''

from itertools import chain #リストを一次元化するときに使う。
import tree_config #自作モジュール。


class List_Adress_Tree:
    '''
    旧来のプログラムで使っていた、リスト表記によるAdressを、人権が認められる記法で分かりやすく扱うためのクラス

    List_Adress_Tree()は、基本的には、BinaryTreeと同値な対象を表現するための一つの簡便的な表示法であり、木のそれぞれの葉のadressの集合によって木構造を暗に示す。
    ただし、中間の枝に関する情報は持っていないため、曖昧性がある。
    '''

    def __init__(self,adresses,tree_name):

        self.adresses = adresses
        self.tree_name = tree_name

    def max_adress(self):
        '''
        この木のrootに該当するadressの数字を求める
        '''
        return max(chain(*self.adresses))


    def adress_to_tree2(self):
        '''
        0付きのadressの集合を渡された時、そのadressの集合に対応するBinaryTreeのrootを返してくれる。
        '''

        root = BinaryNode(tree_name=self.tree_name)

        for listadress in (self.adresses):

            path = Path(listadress,tree_name=self.tree_name)
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

        org_binary_node.sister[0].set_val()


        time_list = []
        org_binary_node.search_vals(time_list)

        time_list = tree_config.output_range_config(time_list,tree_name=self.tree_name)

        return time_list


class Path:
    '''
    pathとは、旧来のlistタイプのadressには(0とNoneを同一視しててキモイなどの点で)人権がないので、pathという新しいツールに進化させて人権を獲得したものである。

    pathは、木の中での(通常はrootからの)相対的な位置関係を表す。

    pathは以下のような記述ルールに基づいて書かれる。
    [a1,a2,a3…an]というリストが渡された時、rootから、a1番目、a2番目,,,というnodeを辿って行ったときに辿りつけるnodeが、現在のnodeである。
    '''

    def __init__(self,adress=[],tree_name=''):
        self.adress = adress
        self.tree_name=tree_name

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



    def to_bool(self, bool_pattern=0, dim_pattern={}):
        '''
        変換代数に用いる。
        adressの値から、縮約、非縮約を決定するbool値を返す。
        '''

        D, U, R =  self.adress_to_DUR()

        return tree_config.to_bool_config(tree_name=self.tree_name,bool_pattern=bool_pattern, D=D,U=U,R=R)




    def adress_to_DUR(self,  len_U = 3, len_R = 3):
        '''
        adressからd,u,rの数字の3つ組を計算して返す
        '''
        D = len(self.adress)

        U_Tree = (self.adress + [0]*len_U)[:len_U]
        R_Tree = (self.adress[::-1] + [0]*len_R)[:len_R]


        U,R = 0,0

        for i in range(len_U):
            U += (2**i) * U_Tree[i]
        for i in range(len_R):
            R += (2**i) * R_Tree[i]


        return D, U, R



    def left(self):
        '''
        そのパスの左のパスを返す
        '''
        return Path(self.adress+[0],tree_name=self.tree_name)

    def right(self):
        '''
        そのパスの右のパスを返す
        '''
        return Path(self.adress+[1],tree_name=self.tree_name)


class BinaryNode:
    '''
    二分木構造。
    一般の根付き木を使いたい場合にはNodeを使用すること。
    '''
    def __init__(self,tree_name):
        self.root = None
        self.left = None
        self.right = None
        self.tree_name=tree_name


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
            self.right = BinaryNode(tree_name=self.tree_name)

        return self.right

    def make_left(self):
        '''
        左にノードを追加する
        '''
        if not(self.left):
            self.left = BinaryNode(tree_name=self.tree_name)

        return self.left

    def make_path(self,path):
        '''
        パスというオブジェクトが渡された時、そのnodeからパスに該当する葉と、その葉への最小限の経路を木に追加する。
        最後にその追加された葉を返す
        '''

        if len(path.adress) == 0:
            return self

        '''
        next_node = BinaryNode(tree_name=self.tree_name)#これは削除してもよい？
        '''

        if path.adress[0] == 0:
            if self.left:
                next_node = self.left
            else:
                next_node = BinaryNode(tree_name=self.tree_name)
                self.left = next_node

        elif path.adress[0] == 1:
            if self.right:
                next_node = self.right
            else:
                next_node = BinaryNode(tree_name=self.tree_name)
                self.right = next_node

        else:
            print('エラー、二分木のパスには0か1の値を入れてください')

        next_node.root =self
        next_node.make_path(Path(path.adress[1:],tree_name=self.tree_name))
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
            self.path = Path([],tree_name=self.tree_name)

        else:
            if self.root.right == self:
                self.path = self.root.path.right()

            elif self.root.left == self:
                self.path = self.root.path.left()

            else: print("get_path_error")

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

        copy_root = Node(tree_name=self.tree_name)

        self.sister = [copy_root]
        '''
        copy_root.co_sister = [self]
        '''

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

        org_root = self
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

        if self.path.to_bool(bool_pattern=0):

            self.sister[0].do_contraction(dim_pattern=self.path.to_bool(bool_pattern=4))

        return None


    def pull_buck(self):
        '''
        三角図式の縦方向の運動で、"葉について"、Binary_Node_treeからNode_treeへのsister写像を更新する
        '''

        if (not self.right) and (not self.left):

            for x in self.sister:


                if not 'co_brother' in vars(x).keys():##debug
                    print('no_cobro_error')
                    print(self)

                    print(x)
                    print(vars(x))
                    print(x.path.adress)

                    print('informations___end')


            self.sister = [x.co_brother for x in self.sister]
            self.sister = list(chain(*self.sister))


        if self.left:
            self.left.pull_buck()
        if self.right:
            self.right.pull_buck()

    def search_vals(self,time_list):
        '''
        葉に含まれる値を検索する
        '''
        if (not self.right) and (not self.left):

            for i in self.sister:
                if not 'val' in vars(i).keys():
                    pass

                    '''
                    print('no_vals_error')
                    print(i)
                    print(vars(i))

                    print('root_node_information')
                    print(i.root)
                    print(vars(i.root))

                    print('root_root_node_information')
                    print(i.root.root)
                    print(vars(i.root.root))

                    print('root_root_root_node_information')
                    print(i.root.root.root)
                    print(vars(i.root.root.root))

                    print('root_root_root_root_node_information')
                    print(i.root.root.root.root)
                    print(vars(i.root.root.root.root))

                    print('root_root_root_root_root_node_information')
                    print(i.root.root.root.root.root)
                    print(vars(i.root.root.root.root.root))

                    print('root_root_root_root_root_root_node_information')
                    print(i.root.root.root.root.root.root)
                    print(vars(i.root.root.root.root.root.root))

                    print('ultimet_root_information')
                    x=i
                    depth=0
                    while x.root:
                        x=x.root
                        depth+=1

                    print(depth)
                    print(x)
                    print(vars(x))

                    print('error_information_end')
                    '''

            time_list.append([x.val for x in self.sister])



        if self.left:
            self.left.search_vals(time_list)
        if self.right:
            self.right.search_vals(time_list)

        return time_list


    def append_leafs(self,list):
        '''
        デバッグツールに用いる。
        '''
        if (not self.right) and (not self.left):
            list.append(self)

        if self.left:
            self.left.append_leafs(list)
        if self.right:
            self.right.append_leafs(list)

class Node:
    '''
    根付き木構造
    '''
    def __init__(self,tree_name):
        self.root = None
        self.next = []
        self.tree_name = tree_name

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



    def do_contraction(self,  dim_pattern={}):
        '''
        指定されたnode(self)について、その下のsub_tree間で1_変換代数を行う
        '''

        if len(self.next) >2:
            print('too_many_next_error')

        if len(self.next) == 0:
            return None


        if len(self.next) == 2:
            left_tree = self.next[0]
            right_tree = self.next[1]


            copy_left_tree = left_tree.double_trans_alg(bool_pattern=1,  dim_pattern=dim_pattern)#copy_left_treeはSubNode
            copy_right_tree = right_tree.double_trans_alg(bool_pattern=2,  dim_pattern=dim_pattern)#copy_right_treeはSubNode


            #ここで、left_treeを固定した上で、right_treeをleft_treeに引き戻す写像を構成する。


            copy_right_tree.make_co_brother()
            copy_left_tree.make_brother(copy_right_tree,tree_name=self.tree_name,dim_pattern=dim_pattern)



            #四角形図式の射を合成して、 copy_left_treeの葉をcopy_right_treeの葉に引き戻す写像を作る。
            right_tree.pull_buck()
            right_tree.mother.pull_buck()#right_tree.motherはBinaryNode


            #########################debug#########################

            right_tree_has_bug, bug_node_list = right_tree.debug()

            '''
            if right_tree_has_bug:
                print('right_tree_has_bug')
                print(bug_node_list)
            '''

            ########################################################

            self.next.remove(right_tree)





    def debug(self):
        '''
        Binary_nodeの葉が誤ってright_treeに飛ばされてないか確認する。
        '''

        right_tree_has_bug = False
        bug_node_list = set()

        binary_root = self.mother
        while binary_root.root:
            binary_root=binary_root.root



        binary_node_leafs = []
        binary_root.append_leafs(binary_node_leafs)


        for leaf in binary_node_leafs:
            for sister in leaf.sister:

                sister_org=sister

                if sister==self:
                    #print('right_exisitance_error')
                    right_tree_has_bug = True
                    bug_node_list.add(sister_org)

                while sister.root:
                    sister=sister.root

                    if sister==self:
                        #print('right_exisitance_error')
                        right_tree_has_bug = True
                        bug_node_list.add(sister_org)


        return right_tree_has_bug, bug_node_list


    def pull_buck(self):
        '''
        SubNode_tree達にco_brother写像が作られているとき、"葉について"、left_Node_treeからright_Node_treeへの引き戻しとなるco_brother写像を構成する。
        '''

        if len(self.next) == 0:
            self.co_brother = [x.mother for x in self.sister[0].co_brother]


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
            self.path = Path([],tree_name=self.tree_name)

        else:
            conode_num = len(self.root.next)

            for i in range(conode_num):
                if self.root.next[i] == self:

                    if 'path' in vars(self.root).keys():
                        self.path = Path(self.root.path.adress + [conode_num],tree_name=self.tree_name)
                    else:
                        print('not_has_path_error')
                        print(self)
                        print(vars(self))

                        if self.root:
                            print('self.root')
                            print(self.root)
                            print(vars(self.root))

                            if self.root.root:
                                print('self.root.root')
                                print(self.root.root)
                                print(vars(self.root.root))

                                if self.root.root.root:
                                    print('self.root.root.root')
                                    print(self.root.root.root)
                                    print(vars(self.root.root.root))

                        print('error_imformation_end')

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

        copy_root = SubNode(tree_name=self.tree_name)

        self.sister = [copy_root]
        copy_root.mother = self

        for next_node in self.next:
            next_node.make_copy_node()

        return None

    def make_copy_tree(self):
        '''
        その木全体の、根付き木としてのコピーを作る。
        '''

        org_root = self
        org_root.make_copy_node()

        org_root.sister[0].set_copy_nexts()

        return org_root.sister[0]



    def double_trans_alg(self,bool_pattern,dim_pattern):

        '''
        2-変換代数
        この処理についてはノートの三角形図式を参照

        結果的に、sisterのtreeは破壊されてminitreeとなり、motherのtreeの葉のsister写像には求めるminitreeの葉の冪への写像が入っている。
        '''

        #selfはNode

        copy_tree = self.make_copy_tree()
        self.set_path()################(縮約をしている部分木で、新たにpathが作り直されていることに注意)

        org_root = self
        org_root.do_trans_from_bottom(org_root,bool_pattern,dim_pattern)

        return org_root.sister[0]


    def do_trans_from_bottom(self,my_root,bool_pattern,dim_pattern):
        '''
        帰りがけ順でsisterに縮約情報を送る
        '''


        for nodes in self.next:
            nodes.do_trans_from_bottom(my_root,bool_pattern,dim_pattern)


        if self.path.to_bool(bool_pattern,dim_pattern):
            self.sister[0].do_contraction(my_root)


        return None


    def set_val(self):
        '''
        その木の全ての葉を検索してリストにする。また、self.valに対して整列順序を入れる。
        '''
        leafs = []

        self.append_leafs(leafs)

        for number in range(len(leafs)):
            leafs[number].val=number

        return leafs



    def search_leafs(self):
        '''
        その木の全ての葉を検索してリストにする。また、self.valに対して整列順序を入れる。
        '''
        leafs = []
        self.append_leafs(leafs)

        return leafs


    def append_leafs(self,leafs):

        if len(self.next) ==0:
            leafs.append(self)

        for i in self.next:
            i.append_leafs(leafs)

        self.state='vals_checked'

        return None




    def copy_cycle_trans_node_tree(self):
        '''
        make_co_brother関数にて、Node_treeに追加するcycle_trans木をコピーする時に使う。
        '''

        new_node = Node(tree_name=self.tree_name)
        new_node.type = 'cycle_trans'#debug



        if len(self.next) ==0:
            new_node.mother = self.mother



        for nexts in self.next:
            new_node.next.append( nexts.copy_cycle_trans_node_tree() )

        for nexts in new_node.next:
            nexts.root = new_node



        if len(self.next) ==0:
            for right_subnodes in self.sister:

                flowing_subnode = SubNode(tree_name=self.tree_name)
                flowing_subnode.mother = new_node
                right_subnodes.co_brother.append(flowing_subnode)


        return new_node



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

            '''
            指定されたnode(self)について、その下のsub_tree間で1_変換代数を行う
            パターンB(ノート参照)の、上詰めアルゴリズムである。
            '''

            if self.mother==my_root:
                return None

            elif len(self.next) == 0:
                return None


            else:
                sprit_number = self.root.next.index(self)
                self.root.next = self.root.next[:sprit_number] + self.next + self.root.next[sprit_number+1:]

                for x in self.next:
                    x.root = self.root
                return None


    def make_brother(self,copy_right_tree, adress=[],tree_name='error_tree_name',   dim_pattern={}):
        '''
        左の木から、右の木に対して、引き戻し兄弟写像を作る。
        '''

        path = Path(adress=adress,tree_name=tree_name)



        '''
        循環-変換代数
        '''
        separate_number=0

        if tree_config.cycle_trans_config(tree_name=self.tree_name):#self.mother.root:#root上では循環-変換代数が実装できない(→A方式ならできるはず)

            #separate

            separate_number = int(len(copy_right_tree.next)/2)
            copy_right_tree_R = copy_right_tree.next[separate_number:]


            #Node_treeにcycle_trans木を追加

            joint_node = self.mother#.root   #rootを付けるとA方式、root無しだとB方式。


            for sister_append_tree in copy_right_tree_R:

                append_tree = sister_append_tree.mother
                new_node = append_tree.copy_cycle_trans_node_tree()
                joint_node.next.append(new_node)
                new_node.root=joint_node

                new_node.type='cycle_trans_root'#debug





        '''
        matching_pattern検索
        '''

        right_next_number = len(copy_right_tree.next) - separate_number
        left_next_number = len(self.next)



        matching_pattern = path.to_bool(bool_pattern=3  , dim_pattern=dim_pattern)





        '''
        終末条件
        '''


        if right_next_number == 0 and left_next_number == 0:
            copy_right_tree.co_brother.append(self)

            return None



        R_end_pattern =2
        L_end_pattern =2




        if right_next_number == 0:

            if R_end_pattern ==0:#写像を消滅させる
                return None

            if R_end_pattern ==1:#写像を一点に飛ばす
                self.next[0].make_brother(copy_right_tree ,adress=path.adress+[0], tree_name=tree_name, dim_pattern=dim_pattern)
                return None

            if R_end_pattern ==2:#写像を全域に飛ばす
                for i in range(left_next_number):
                    self.next[i].make_brother(copy_right_tree ,adress=path.adress+[i], tree_name=tree_name, dim_pattern=dim_pattern)
                return None



        if left_next_number == 0:

            if L_end_pattern ==0:#写像を消滅させる
                return None

            if L_end_pattern ==1:#写像を一点から飛ばす
                self.make_brother(copy_right_tree.next[0] ,adress=path.adress, tree_name=tree_name, dim_pattern=dim_pattern)
                return None


            if L_end_pattern ==2:#写像を全域から飛ばす
                for i in range(right_next_number):
                    self.make_brother(copy_right_tree.next[i] ,adress=path.adress, tree_name=tree_name, dim_pattern=dim_pattern)
                return None



        '''
        matching規則
        '''

        if matching_pattern ==0:
            '''
            fullのrepete
            (局所性、Rt全体単一性)
            '''

            X = left_next_number
            p_const = left_next_number
            q_const = left_next_number


        elif matching_pattern ==1:
            '''
            一回のみのrepete
            (局所性、Lt全体単一性)
            '''

            X = right_next_number
            p_const = right_next_number
            q_const = right_next_number



        elif matching_pattern ==2:
            '''
            stretch写像
            (Rt一様性、Lt全体単一性)
            '''

            X = left_next_number
            p_const = left_next_number
            q_const = right_next_number



        elif matching_pattern ==3:
            '''
            stretch写像の最初のみの型
            (Lt一様性、Rt全体単一性)
            '''

            X = right_next_number
            p_const = left_next_number
            q_const = right_next_number




        for i in range(X):
            self.next[  int(i*p_const/X) % left_next_number ].make_brother(copy_right_tree.next[  int(i*q_const/X) % right_next_number  ]  ,adress=path.adress+[ int(i*p_const/X) % left_next_number ], tree_name=tree_name, dim_pattern=dim_pattern)

        return None






    def make_co_brother(self):
        '''
        copy_right_treeの”葉”に、make_brother関数で使うco_brother変数を準備する
        '''

        if self.next==[]:
            self.co_brother = []


        for x in self.next:
            x.make_co_brother()

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