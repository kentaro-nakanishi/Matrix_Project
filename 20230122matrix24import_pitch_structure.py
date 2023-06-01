import copy#リストに要素を代入するときに使う。
import datetime#保存するファイル名前を決めるのに時に使う。
import pretty_midi#soundmidiでmidiを書き出す時に使う。
from fractions import Fraction #pitch関数の周波数計算に使う。
import math #周波数の計算に使う。
import time#計算時間の測定に使う

import time_structure as ts #高度な変換代数の計算に使う自作モジュール。
import pitch_structure as ps


####################################################
####################################################
#      MATRIX_PROJEKT                              #
####################################################
####################################################







####################################################
#      二分木の生成　                                #
####################################################

#木の成長関数
def glowing_function(repeat=18,choice=2,up=3,down=5,R_true_tree=[],ref=3):

    #tree(集合が1桁,2桁,3桁…の木)
    tree = []

    #単位集合
    first_note = [0]#数列は0はじまり→indexとして利用できる


    #集合は木の元(これは集合が1桁の木)
    tree.append(first_note)


    #repeat回木を成長させる
    for i in range(repeat):

        org_tree = tree
        new_tree = []

        #選択関数の桁数
        digit = i+1
        
        #生成前の木のそれぞれの元について
        for note in org_tree:
            
            #複製を追加する       
            new_tree.append(copy.copy(note))

        #生成前の木のそれぞれの元について
        for note in org_tree:

            #選択関数がTrueを取るならば
            if choice_function(digit,note,choice,up,down,R_true_tree,ref):

                #その音に指標を加え(結合関数)
                note.append(digit)
                
                #木に加える       
                new_tree.append(copy.copy(note))

        #関数の再帰化
        tree = copy.copy(new_tree)

    return tree


#選択関数(選択関数には様々な種類がある)
def choice_function(digit,note,choice,up,down,R_true_tree=[],ref=3):

    if choice ==0:
        return True
    
    if choice ==1:
        #選択数列(色彩的な数列)
        choice_list = make_choice(up,down)

        #選択数列から桁数分だけ取り出す +1(全体選択作用)
        slice_of_choice = choice_list[:digit +1]

        #判別式の値(false=1はじまり)
        d = 1 +slice_of_choice[digit]#最後の桁を全体作用として利用する。→左全体選択作用,右全体選択作用が作れる

        for i in note:
            d += choice_list[(digit-1) - i]#i=0(つまり最も細かい枝)のとき 全体作用を除いたスライスの最後の桁を採用する。

        #判別式(判別式が奇数ならfalse,偶数ならtrueを返す)
        return d%2
    
    if choice ==2:#変換代数と対応する縮約(計算量削減のため直接書いてる)

        #ref = 3#何桁前まで参照するか

        #色彩的な無限計算はここでは行わない（縮約木を固定している）

        #定数、縮約木
        #R_full_tree = glowing_function(repeat=3,choice=0)###これを毎回計算すんのがオーダー悪化させてる
        #R_full_tree = [[i for i in j if i>0] for j in R_full_tree]
        #R_true_tree = R_full_tree[1:]

        #反転disitの最後のref桁について
        rev_adress = note[::-1]
        rev_adress = [(digit-x) for x in rev_adress]#(1はじまり)

        ref_adress = [i for i in rev_adress if i<=ref]

        return ref_adress in R_true_tree





#選択数列を生成する
def make_choice(up=3,down=5):
    

    #2進数にして出力
    output = []

    for i in range(200):
        up *= 2
        if up>down:
            output.append(1)
            up -=down

        else:
            output.append(0)

    return output



####################################################
#      変換代数　　　                                #
####################################################



def left(tree):#treeの左を返す(但し上詰め代数)


    #追加的例外処理
    if len(tree) == 0:
        return []
    if len(tree) == 1:
        return tree #一葉は左に詰めて返す（これ大丈夫か...?）

    flat_tree = []

    for i in tree:
        flat_tree += i

    minimum = max(flat_tree)

    return_tree = []

    for i in tree:
        if not (minimum in i):
            return_tree.append(i)

    return return_tree

def right(tree):#treeの右を返す(但し上詰め代数)

    #追加的例外処理
    if len(tree) == 0:
        return []
    if len(tree) == 1:
        return [] #一葉は左に詰めて返す（これ大丈夫か...?）

    flat_tree = []
    
    for i in tree:
        flat_tree += i

    minimum = max(flat_tree)

    return_tree = []


    #ここで、leftと違って、topを削除しなければならない点に注意
    for i in tree:
        if minimum in i:
            x = [j for j in i if (j !=minimum) ]
            return_tree.append(x)

    return return_tree




#treeA >＝ treeB かどうか、言い換えれば、(treeB → treeA)という射が存在するかどうか、別の言い方では、treeBからtreeAへの順序を保つ単射が存在するかどうか。 
def hom(treeA,treeB):

    #treeAの方が小さかったらどのみち対応なんて作れるわけがない
    if len(treeB) > len(treeA):

        boolian = False



    #treeBが"葉"になったら、treeAが無でなければ対応が作れる(しかし、無であることは最初のケースで除外されている)
    #また、treeBが∅なら、自明な対応が作れる

    elif len(treeB) == 1 or len(treeB) == 0:
    
        boolian = True


    #右で同型が取れて、左でも同型が取れたら、全体で同型が取れる。
    elif hom(  left(treeA) , left(treeB)   )   and   hom(  right(treeA) , right(treeB)   ):

        boolian = True


    #どっちでも同型が取れなかったとしても、treeAの右だけで、もしくは左だけで同型が取れたら御の字。
    elif hom(  left(treeA) , treeB  )  or  hom(  right(treeA) , treeB   ):

        boolian = True


    else:#その内どれでも同型が取れなかったらfalse

        boolian = False

    return boolian



#treeA/treeBという商を取る     　代数的にはこれは、treeAの（AonB→0）による同値類を取っている。
def divide(treeA,treeB):

    B_class = [ [treeA,0] ] #木、識別子（0→False 1→True）



    while True:

        #全ての要素が所定の大きさより小さくなったら処理を終了する。
        brk = 1
        for pair in B_class:
            brk *= pair[1]

        if brk:
            break
        
        #分割作業

        new_B_class = []

        for pair in B_class:
            
            if pair[1] == 1:
                new_B_class.append(pair)

            else:

                if  hom(treeB, pair[0]):#treeBよりも小さいならば
                    new_B_class.append([ pair[0] , 1 ])#True化して受け渡す
                    

                else:#大きいならば
                    #分割して渡す

                    leften =  left(pair[0]) 
                    righten =  right(pair[0])

                    new_B_class.append([ leften , 0 ])
                    new_B_class.append([ righten , 0 ])


        #世代の更新
        B_class = new_B_class
            

    #B_classを整える
    B_class = [pair[0] for pair in B_class]


    return B_class

#treeB\treeAという商を取る     　(上から割っている)
def co_divide(treeA,treeB):

    if len (treeB) <= 1:#葉よりも小さければ分割終了。
        return [ [treeA] ]
    
    else:#葉よりも大きければ分割する。
        
        return   [ co_divide(left(treeA), left(treeB))   +   co_divide(right(treeA), right(treeB)) ] 



#treeAの（treeB→1）という小木AonBを取る
def quot(treeA,treeB):

    B_class = divide(treeA,treeB)


    output = []

    num = 0
    for i in B_class[1:]:

        output.append(treeA[num])
        num += len(i)

    return output

#treeAの（treeB→1）による同値類を作る
def eqiv(treeA,treeB):

    B_class = divide(treeA,treeB)

    output = []

    num = 0
    for i in B_class:

        for j in range(len(i)):
            output.append(treeA[num])

        num += len(i)

    return output





#quotとdivideを変動桁にて接合する
def mult(AonB,B_class):

    output = []


    num = 0#AonBとの対応を作る検索子


    for i in B_class:#"それぞれの楽節において"（つまり、楽節の外の構造を、可能な限り保存する。固定桁システムではなく、変動桁システムである）



        #楽節の大きさを求める

        #（∅に対する例外処理）
        if len(i) == 0:
            max_num =0

        elif len(i[-1]) == 0:
            max_num =0

        else:
            max_num = i[-1][-1]



        for j in i:#B_classのそれぞれの元について

            x = j + AonB[num][max_num:]

            output.append(x)

        num += 1#検索子を走らせる

    return output

#eqivとdivideを変動桁にて接合する

def joint(AonB,B_class):

    output = []


    num = 0#AonBとの対応を作る検索子


    for i in B_class:#"それぞれの楽節において"（つまり、楽節の外の構造を、可能な限り保存する。固定桁システムではなく、変動桁システムである）



        #楽節の大きさを求める

        #（∅に対する例外処理）
        if len(i) == 0:
            max_num =0

        elif len(i[-1]) == 0:
            max_num =0

        else:
            max_num = i[-1][-1]



        for j in i:#B_classのそれぞれの元について

            x = j + AonB[num][max_num:]

            output.append(x)

        num += len(i)#検索子を走らせる

    return output


#treeの下詰めを返す

def down(tree):
    

    if len(tree) == 0:
        return []

    if len(tree) == 1:
        return [[0]]

    L = down( left(tree) )
    R = down( right(tree) )

    #Rには識別子を足す

    flat_R = []
    for i in R:
        flat_R += i

    new_X = max(flat_R) + 1
    R = [ (x+[new_X])  for x in R ]

    return (L + R)






#######################
#変換代数P1
#######################
def transP1(tree,trans_rule=4,R_full_tree=[[],[1]],R_true_tree=[[1]], ref=3):
    """
    全木[list]を受け取って、小木[list]と、全木から小木への写像[list]を返す。
    """

    mapping = []#全木から小木への写像

    for note in tree:#各noteについて、(この時間構造関数は"驚くべきことに"正則である。)
        
        new_note = []

        for branch in note[::-1]:#分岐枝を上から降ろしていく

            if Trans_choice([i for i in note if i<branch] , branch, trans_rule, R_full_tree, R_true_tree, ref) == False:#選択関数が真なら縮約
                new_note.append(branch)

        mapping.append(new_note)

    #mappingから重複する要素を潰して像となるmini_treeを作る

    mini_tree = []
    for i in mapping:
        if not(i in mini_tree):
            mini_tree.append(i)


    return mini_tree, mapping



#時間構造関数の2番から移植した選択関数
def Trans_choice(up_tree,  now_branch, choice, R_full_tree, R_true_tree, ref=3):
    '''
    (上アドレス、現在の分岐)、それから選択ルールの3つ組を受け取って、縮約するかのbool値を返す
    '''


    if choice==0:#上フラクタル
        close = ( len(up_tree) %5 == 3  )
        return  close
    
    if choice==1:#下フラクタル
        close = ( now_branch-1 in up_tree)
        return close

    if choice==2:
        close = ( len(up_tree) <= 1  )

    if choice==3:#9の木が全部右にいっちゃう
        close = ( 9 in up_tree  )    

    if choice==4:#逆木による分割A


        #####共通定数の設定

        #bool値を持つ逆木(R_full_tree ⊃(→ 折り畳み)　R_true_tree)
        #R_full_tree = [[] , [1]]
        #R_true_tree = [ [1] ]#(1はじまり)


        ###各枝について、逆木の原理を拡大する
        
        #step1枝のアドレスを逆木に反転する
        rev_adress = up_tree[::-1]
        rev_adress = [(now_branch-x) for x in rev_adress]#(1はじまり)

        #step2全逆木から逆アドレスを検索する（これ、固定桁数にした方が早くないか。。。？）
        
        if rev_adress == []:
            search_branch = 0
        else:
            search_branch = max(rev_adress)

        roop = True
        while roop and search_branch>0:

            if not( [x for x in rev_adress if x<search_branch] in [[x for x in leaf if x<search_branch] for leaf in R_full_tree] ):
                search_branch -= 1
            else:   
                roop = False
                
        close = [x for x in rev_adress if x<(search_branch)] in R_true_tree#検索した枝がR_true_treeに含まれれば縮約.


    if choice==5:#計算量の少ないeasy_trans

        #ref=5#検索を何階上まで遡るか

        #step1枝のアドレスを逆木に反転する
        rev_adress = up_tree[::-1]
        rev_adress = [(now_branch-x) for x in rev_adress]#(1はじまり)

        rev_adress =[x for x in rev_adress if (x<=ref)]#(検索)

        close = rev_adress in R_true_tree

    return close
    

    #選択関数が真なら非縮約



"""
#(↓小木を受け取って、小木から値への写像[list]を返す)
"""


####################
#変換代数P2(引き戻し)
####################
def transP2(mapping1,mapping2):
    """
    全木から小木への写像[list]と、小木から値への写像[list]を受け取って、全木から値への写像[list]を返す
    """

    #小木を構成する
    mini_tree = []
    for i in mapping1:
        if not(i in mini_tree):
            mini_tree.append(i)

    return [mapping2[mini_tree.index(i)] for i in mapping1]

def transP3(mapping1,mapping2,mini_tree,org_tree):
    """
    全木から小木への写像[list]と、小木から値への写像[list]と、小木[list]と、全木[list]を受け取って、全木から値の集合への写像[list]を返す
    """

    #A.全木から小木の冪への写像を作る

    org_to_lit =[]

    #全木のそれぞれの元について
    num = len(org_tree)
    for index in range(num):

        #step1可変元と不可変元の集合に分離する
        changable = []
        
        for i in org_tree[index]:
            if not(i in mapping1[index]):
                changable.append(i)


        
        #step3可変元から冪集合の木を生成する(これは二分木の生成に相当する)
        power = [[]]
    
        for i in changable[:-1]:#################################################################
            power_append = [x+[i] for x in power]
            power += power_append


        #step4可変限と不可変元を融合したadressの集合(=(逆)木)を作る
        power_tree = [sorted(mapping1[index] + i) for i in power]

        ############################################(２-変換代数)
        #power_tree=left(power_tree)
        ############################################
        

        org_to_lit.append(copy.copy(power_tree))

    
    #step5冪集合と小木の共通部分を求める
    for index in range(num):
     org_to_lit[index] = [i for i in org_to_lit[index] if i in mini_tree]

    #B.　A.から「全木から値の集合への写像[list]」を作成する（Bは外部化する？）
    org_to_val = []

    for adr_sets in org_to_lit:
        val_sets = [mapping2[mini_tree.index(i)] for i in adr_sets]
        org_to_val.append(copy.copy(val_sets))


    return org_to_val

def transP3_unite(time_list,pitch_list,voice_list):#擦り合わせ、冪集合化されたtime_listの逆像木を単一の元に戻す

    new_time_list =[]
    new_pitch_list =[]
    new_voice_list =[]

    for index in range(len(time_list)):
        
        for time in time_list[index]:

            new_time_list.append(time)
            new_pitch_list.append(pitch_list[index])
            new_voice_list.append(voice_list[index])

    return new_time_list,new_pitch_list,new_voice_list



def transP3_unite2(time_list,pitch_list,voice_list):
    '''
    変換代数後の結合層  time_structureとpitch_structureの直積を取る
    '''

    new_time_list =[]
    new_pitch_list =[]
    new_voice_list =[]

    for index in range(len(time_list)):


        for time in time_list[index]:
            for pitch in pitch_list[index]:

                new_time_list.append(time)
                new_pitch_list.append(pitch)
                new_voice_list.append(voice_list[index])


    return new_time_list,new_pitch_list,new_voice_list



#################################################
#   TERMINAL                                    #
#################################################

#二分木を楽譜に変換する関数
def realisation(tree):

    #変換代数P1
    ########################################

    ref = 5

    R_full_tree = glowing_function(repeat=ref,choice=0)
    R_full_tree = [[i for i in j if i>0] for j in R_full_tree]
    
    #R_true_tree0 = R_full_tree[30:]

    R_true_tree1 = R_full_tree[:16]
    R_true_tree2 = []#R_full_tree[:8]
    R_true_tree3 = R_full_tree[:4]

    #tree,no_use = transP1(tree=tree,R_full_tree=R_full_tree,R_true_tree=R_true_tree0)
    tree = down(tree)

    '''
    time_mini_tree,time_mapping1 = transP1(tree=tree,R_full_tree=R_full_tree,R_true_tree=R_true_tree1,ref=ref)
    pitch_mini_tree,pitch_mapping1 = transP1(tree=tree,R_full_tree=R_full_tree,R_true_tree=R_true_tree2,ref=ref)
    '''

    voice_mini_tree,voice_mapping1 = transP1(tree=tree,R_full_tree=R_full_tree,R_true_tree=R_true_tree3,ref=ref)

    '''
    time_mini_tree = down(time_mini_tree)
    pitch_mini_tree = down(pitch_mini_tree)
    '''

    voice_mini_tree = down(voice_mini_tree)

    ########################################

    '''
    #→→ここにtime_structureを記述する。
    time_mapping2 = time_structure(time_mini_tree)
    '''

    '''
    ###pitch_structureで用いる音階を設定する
    topolo_list = make_topolo()


    #→→ここにpitch_structureを記述する。
    pitch_mapping2 = pitch_structure(tree=pitch_mini_tree,topolo_list=topolo_list)#topolo_listで音階を受け渡す
    
    #pitch_structureの後付けオクターブ巡回子。
    if True:
        pitch_mapping2 = pitch_limit(pitch_mapping2)
    '''


    #→→ここにvoice_structureを記述する。
    voice_mapping2 = voice_structure(voice_mini_tree)


    print('p2_start')
    C1=time.time()


     #変換代数P2(引き戻し)
    ########################################

    #time_list = transP2(time_mapping1,time_mapping2)
    #pitch_list = transP2(pitch_mapping1,pitch_mapping2)
    voice_list = transP2(voice_mapping1,voice_mapping2)
    
    '''
    time_list = transP3(time_mapping1,time_mapping2,time_mini_tree,tree)
    '''

    '''
    →→→→→→→→→→→→→→→→→→→→→→→
    treeモジュールによる2-変換代数をここに埋め込む
    ←←←←←←←←←←←←←←←←←←←←←←←
    '''


    time_object = ts.List_Adress_Tree(adresses=tree)
    time_list = time_object.make_time_list()

    pitch_object = ps.List_Adress_Tree(adresses=tree)
    pitch_list = pitch_object.make_time_list()


    #pitch_list = transP3(pitch_mapping1,pitch_mapping2,pitch_mini_tree,tree)
    #voice_list = transP3(voice_mapping1,voice_mapping2,voice_mini_tree,tree)

    #擦り合わせ
    '''
    time_list,pitch_list,voice_list = transP3_unite(time_list,pitch_list,voice_list)
    '''

    time_list,pitch_list,voice_list = transP3_unite2(time_list,pitch_list,voice_list)
    ########################################

    print('p2_end')
    C2=copy.copy(C1)
    C1=time.time()
    print(C1-C2)

    #midi化する
    midinize(pitch_list,time_list,voice_list)

    return None



####################################################
#      時間構造関数                                #
####################################################


#時間構造関数ー時間構造関数は他の音に依存するためtreeで受け取る。
def time_structure(tree,n=8):

    choice = 2
 
    if choice == 0:#固定n桁時間システム

        #下n桁を潰す(下n桁は同時発音性に用いるため)
        omit = []

        for note in tree:
            for j in range(n):
                if j in note:
                    note.remove(j)

            omit.append(copy.copy(note))

        #それぞれの音の発音タイミングを算出する
        time_list = []
        time = 0
        length = 1/4 #一拍の長さ

        #前の音と真の桁が異なる時のみ時間を加算する
        prev_note = []

        for note in omit:
            if note != prev_note:
                time += length

            prev_note = note

            time_list.append(copy.copy(time))
    
    if choice == 1:#時間構造関数の変動n桁タイムシステム


        length = 1/4 #定数、一拍の長さ
        larges = 4 #定数、最大の声部数

        old_total = [tree]
        new_total = []#total>puchi>note>1,2,3…


        while True:

            #最大のpuchiの大きさを計る
            p = []
            for puchi in old_total:
                p.append(len(puchi))

            if max(p) <= larges:#もしも最大のpuchiが所定の大きさより小さければ処理を終了する
                break

            #大きいpuchiを分割する作業
            for puchi in old_total:
                if len(puchi) <= larges:#所定の大きさより小さければ
                    new_total.append(puchi)#そのまま受け渡す

                else:#所定の大きさより大きければ
                    
                    #分割する

                    #分割する枝数の同定
                    #puchiの最後のnoteから枝数を逆順で取り出す
                    for N in puchi[-1][::-1]:
                        #puchiの最初のnoteと比べ、枝が分岐する点を同定する
                        if N not in puchi[0]:

                            #branchに分岐点を保存
                            branch = N
                            break

                    #puchiを分割
                    puchi1 = []
                    puchi2 = []
                    
                    for note in puchi:
                        if branch in note:
                            puchi2.append(note)
                        else:
                            puchi1.append(note)

                    #分割したpuchiを受け渡す
                    new_total.append(puchi1)
                    new_total.append(puchi2)


            old_total = new_total
            new_total = []
            #----->>>puchiの分割終わり、次のpuchiへ行く

        #puchiの分割が終了

        #出力するtime-listを作成する
        time_list = [] #変数、出力するリスト
        time = 0

        for puchi in old_total:#new_totalのそれぞれの元に対して
            for i in range(len(puchi)):#puchiに入っているnoteの数だけtを加える
                time_list.append(copy.copy(time))

            time += length #時間を進める

    if choice == 2:#変換代数によるフラクタル構造
        length = 1/4 #定数、一拍の長さ



        #変換代数...treeから写像を構成する
        
        m_choice=3#変換代数を選択する
        mapping = []

        if m_choice==0:
            for note in tree:#各noteについて、(この時間構造関数は"驚くべきことに"正則である。)
                
                new_note = []

                for branch in note[::-1]:#分岐枝を上から降ろしていく

                    if T_choice(note[:branch] , branch) == False:#選択関数が真なら縮約
                        new_note.append(branch)

                mapping.append(new_note)

            ########(メモ)↑このmappingとtreeを照らし合わせればtreeからmini_treeへの写像が構成できる


        if m_choice==1:
            for note in tree:#各noteについて、

                omit = []#定数
                new_note = [x for x in note if not (x in omit)]#定数の枝を潰す


                mapping.append(new_note)

        if m_choice==2:#木で割る(なぜかエラー)

            divide_tree = [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
            mapping =divide(tree,divide_tree)

        if m_choice==3:#素通り
            mapping = tree

        ####################################(↑変換代数P1)

        #整列して順序を与える

        diction = {}#key→num,val→note

        for note in mapping:  #mappingの像を取る
            num = 0
            for i in note:
                num += 2**i

            diction[num] = note#標数によって整列


        
        sorted_diction = sorted(diction.items())#key→num,key→note


        mapping2 = {} #葉から順序への写像

        time = 0
        for pair in sorted_diction: #それぞれの葉に整列順序を入れる
            
            leaf = pair[1]

            #leafをtupleに変換する
            leaf = tuple(leaf)

            mapping2[leaf] = copy.copy(time)
            time += length


        ####################################(↑時間構造関数)

        ##最後に、写像を合成してorg_treeからtimeへの写像を構成する。

        time_list = []

        for i in mapping:#org_treeからmini_treeへの写像


            key = tuple(i)
            time_list.append(mapping2[key])#mini_treeからorg_treeへの写像

        ####################################(↑変換代数P2(引き戻し))

    

    #以上,時間構造関数            
    return time_list



#時間構造関数の2番で使う選択関数→(これは二分木の生成で使えないか?)
def T_choice(up_tree,  now_branch):

    choice = 1

    if choice==0:#上フラクタル
        close = ( len(up_tree) %5 == 3  )
        return  close
    
    if choice==1:#下フラクタル
        close = ( now_branch-1 in up_tree)
        return close

    if choice==2:
        close = ( len(up_tree) <= 1  )

    if choice==3:#9の木が全部右にいっちゃう
        close = ( 9 in up_tree  )    

        return close
    


#選択関数が真なら非縮約



####################################################
#      ピッチ構造関数　                              #
####################################################

#ピッチ構造関数ー一つのノートに対してその線形和をピッチとする。（ただし、同値類で潰されている。）←選択関数との関係は？
def pitch_structure(tree,n=8,topolo_list=None):

    Pchoice = 3 #どのピッチ構造関数を使う？

    pitch_list = []


    #####1.最も簡単なΣ2^n型の正則ピッチ構造関数#####
    if Pchoice == 1:
        #tree内の各音に対してpitchを算出する
        for note in tree:

            pitch = 10

            #暫定的にΣ2^nとする。
            for i in range(n+1):
                if i in note:
                    pitch += 2^(n-i)

            pitch_list.append(copy.copy(pitch))

    #####2.一階のΣ型の正則ピッチ構造関数#####
    if Pchoice == 2:

        freq_list = []#ここに周波数を貯めていく

    
        for note in tree:

            #住所2^nをtopoloの住所に振り分ける
            topolo_adress = ad2topolo(note,topolo_list)

            pitch = 1

            for i in range(len(topolo_adress)):
                pitch*=topolo_list[i][topolo_adress[i]%len(topolo_list[i])] * (2**(topolo_adress[i]//len(topolo_list[i])))#i番目の位相の、topolo_adress[i]個目の音程を付加する#%~各位相を巡回群にする#*以降はオクターブ成分なので、同値類を潰す時は削除できる

            freq_list.append(copy.copy(pitch))

        
        #周波数をmidi_notenumberに変換する
        cons_pitch = 2#定数、全体の主音となる基準ピッチ
        pitch_list = []

        for i in freq_list:#それぞれの周波数に対して

            notenumber = cons_pitch + int(math.log2(i)*12 +1/2)##←floatに変換する必要ある?
            pitch_list.append(copy.copy(notenumber))##形式はnotenumberが時間順に並んだ単純リスト



        #####3.n階の埋め込み型ピッチ構造関数#####
    if Pchoice == 3:

        freq_list = []#ここに周波数を貯めていく

    
        for note in tree:#それぞれの音について、

            #住所2^nをtopoloの住所に振り分ける
            topolo_adress = ad2topolo(note,topolo_list)

            position = 0 #ここに、各位相での展開型を貯める

            for i in range(len(topolo_list)):#粗い位相から順番に、
                
                position += topolo_adress[i]#転移させる

                #巡回成分と純粋転移成分に分ける
                circle = position//len(topolo_list[i])#巡回成分

                T_position = position%len(topolo_list[i])#純粋転移成分


                #次の位相が存在するならば
                if i != max(range(len(topolo_list))):
                    #次の位相のpositionに引き継ぐ

                    #巡回成分で次の位相のpositionを定める
                    position = circle*len(topolo_list[i+1])

                    #純粋転移成分はまず周波数に移して、
                    T_freq = topolo_list[i][T_position]

                    #次のtopolo_listから周波数を検索して
                    search = 0#変数、検索子

                    while topolo_list[i+1][search] != T_freq:#T_freqが見つかるまでの間
                        search += 1#検索子を走らせる

                    position += search#positionに検索子を足すと次の位相のpositionが完成する
                    
                    ####処理終了、次の周へ

            ####疑問（topololistって上限と下限どっちを含む？）←下限!
            
            #positionをpitchに変換する
            pitch = T_freq * 2**circle #純粋位相成分×巡回成分（ここでは上限がないので２を法とする）

            freq_list.append(copy.copy(pitch))
            ##ここまでで一つの音の処理が終わり


        #周波数をmidi_notenumberに変換する
        cons_pitch = 42-60#定数、全体の主音となる基準ピッチ
        pitch_list = []

        for i in freq_list:#それぞれの周波数に対して

            notenumber = cons_pitch + int(math.log2(i)*12 +1/2)##←floatに変換する必要ある?
            pitch_list.append(copy.copy(notenumber))##形式はnotenumberが時間順に並んだ単純リスト

            
            
    return pitch_list


#住所2^nをtopoloの住所(n^n)に振り分ける
def ad2topolo(note,topolo_list):


    choice = 2#どの振り分けを選択する？


    ###1:単純+1巡回型振り分け
    if choice == 1:

        #1,2,3,1,2,3と繰り返しリストに貯めていく
        repeat = len(topolo_list)

        #出力する住所(n^n)
        output = [0]*repeat

        #粗い位相から先に貯められる
        for i in note:

            p = i%(repeat) #pは足される位相
            output[p] += 1 #転移追加


    ###2:全五度巡回型振り分け
    if choice == 2:

        #1,2,3,1,2,3と繰り返しリストに貯めていく
        repeat = len(topolo_list)

        #出力する住所(n^n)
        output = [0]*repeat

        #粗い位相から先に貯められる
        for i in note:

            p = i%(repeat) #pは足される位相


            search = 0#変数、検索子

            if Fraction(3,2) in topolo_list[p]:#bug例外処理

                while topolo_list[p][search] != Fraction(3,2):#五度が見つかるまでの間
                    search += 1#検索子を走らせる

                output[p] += search #転移追加


    return output



#####それぞれの位相の音階を決定する
def make_topolo():

    choice = 3#どのtopolo_listを使う？

    ###1.2.単純ユークリッド的位相
    if choice == 1 or 2:

        maxe = Fraction(2,1)#定数、一位相の最大長さ

        longa = Fraction(2,1)#定数
        vrevis = Fraction(3,2)#定数

        #topolo→変数、元は[周波数]　ただし8vaを含まない



        topolo_list = []#変数、元はtopolo
        white_topolo_list =[]#

        messy = 5 #定数、位相の細かさ

        vrevis_list = []#変数、longaとvrevisの判定に用いる
        new_vrevis_list = []#変数、longaとvrevisの判定に用いる
        prev_topolo = [Fraction(1,1)]#変数、最初に前世代のtopoloを定めておく


        ###########ここでtopololistに初期topolosを加えておく必要がある。
        topolo_list.append(prev_topolo)


        for i in range(messy):

            new_topolo = []#ここに新しいtopoloを作る
            white_topolo = []#ここに新しいwhite_topoloを作る

            howmany = 0#longaがvrevisいくつ分に当たるのかを計算する
            while vrevis**howmany < longa:
                howmany+=1
            howmany-=1

            #prev_topoloからnew_topoloを生成する。
            
            for i  in prev_topolo:#前音階のそれぞれの音について、
                new_topolo.append(copy.copy(i))#その音を次なるtopoloに引き継ぐ
                white_topolo.append(copy.copy(i))

                if not (i in vrevis_list):#その音がlongaならば,
                    
                    #howmanyの数だけvrevis音を追加
                    for j in range(howmany):
                        new_topolo.append( i*(vrevis**(j+1)) )#vrevis音 = 幹音 × vrevisのn乗で求まる
                        white_topolo.append( i*(vrevis**(j+1)) )
                    
                    new_vrevis_list.append(i*(vrevis**howmany))#最終音はvrevisとなる
                    white_topolo.remove( i*(vrevis**howmany) )#white_topoloから最終音は外される

                        

            #new_topoloの生成完成
            topolo_list.append(new_topolo)#完成したtopoloをリストに加える
            prev_topolo = copy.copy(new_topolo)#前世代のtopoloを更新.

            #新しいvrevisとlongaの定義
            new_vrevis = longa / (vrevis**howmany)
            longa = vrevis
            vrevis = new_vrevis

            #vrevis_listの更新
            vrevis_list = copy.copy(new_vrevis_list)
            new_vrevis_list = []

            #white_topoloの更新
            white_topolo_list.append(copy.copy(white_topolo))
            #これで一周終わり,次の周へ＞＞

        if choice == 2:#white_topoloを出力する場合
            topolo_list = white_topolo_list



    ###3.中間生成ユークリッド的位相（第二種最良近似分数）
    if choice == 3:

        maxe = Fraction(2,1)#定数、一位相の最大長さ

        longa = Fraction(2,1)#定数
        vrevis = Fraction(3,2)#定数

        #topolo→変数、元は[周波数]　ただし8vaを含まない



        topolo_list = []#変数、元はtopolo

        messy = 4 #定数、位相の細かさ

        vrevis_list = []#変数、longaとvrevisの判定に用いる
        new_vrevis_list = []#変数、longaとvrevisの判定に用いる
        prev_topolo = [Fraction(1,1)]#変数、最初に前世代のtopoloを定めておく


        ###########ここでtopololistに初期topolosを加えておく必要がある。
        topolo_list.append(prev_topolo)


        for i in range(messy):

            new_topolo = []#ここに新しいtopoloを作る

            howmany = 0#longaがvrevisいくつ分に当たるのかを計算する
            while vrevis**howmany < longa:
                howmany+=1
            howmany-=1

            #prev_topoloからnew_topoloを生成する。
            
            for i  in prev_topolo:#前音階のそれぞれの音について、
                new_topolo.append(copy.copy(i))#その音を次なるtopoloに引き継ぐ


            #############↓この部分が1のシステムと違う↓###############

            #howmanyの数だけ
            for j in range(howmany):


                for i  in prev_topolo:#前音階のそれぞれの音について、
                    if not (i in vrevis_list):#その音がlongaならば,
                    
                        #vrevis音を追加
                        new_topolo.append( i*(vrevis**(j+1)) )#vrevis音 = 幹音 × vrevisのn乗で求まる
    
                        if j == max(range(howmany)):#(最終回のみ)
                            new_vrevis_list.append(i*(vrevis**howmany))#最終音は次世代のvrevisとなる
        
                #毎回のhowmanyで位相を追加

                new_topolo.sort()
                topolo_list.append(copy.copy(new_topolo))


                        
            #(以降最終回は前と同じ)

            ##完全なnew_topoloの生成完成
            prev_topolo = copy.copy(new_topolo)#前世代のtopoloを更新.

            #新しいvrevisとlongaの定義
            new_vrevis = longa / (vrevis**howmany)
            longa = vrevis
            vrevis = new_vrevis

            #vrevis_listの更新
            vrevis_list = copy.copy(new_vrevis_list)
            new_vrevis_list = []

            #これで一周終わり,次の周へ＞＞

    return topolo_list



#後付け処理、ピッチの定義域を巡回群で抑える。
def pitch_limit(pitch_list):

    new_pitch_list = []
    
    cons = 42-18#定数、基準ピッチ
    circle = 12*6


    for i in pitch_list:
        new_pitch_list.append(i%circle + cons)

    return new_pitch_list


#########################
#velocityについて書き途中 #
#########################

def velocity_structure(tree):

    choice = 0

    if choice == 0:
        velocity_list = [100]*len(tree)

    #単純Σ型関数
    if choice == 1:
        velocity_list = []


        n = 6

        for note in tree:

            vel = 0

            #暫定的にΣ2^nとする。
            for i in range(n+1):
                if i in note:
                    vel += 2^(n-i)

            velocity_list.append(copy.copy(vel))

    #正規化

    div = 127/max(velocity_list)

    velocity_list = [int(i*div) for i in  velocity_list]

    return velocity_list



####################################################
#      声部関数　　                                 #
####################################################

def voice_structure(tree,choice=1):

    choice = 1

    if choice == 0:

        return [0]*len(tree)
    
    if choice == 1:

        voice_list = []

        for note in tree:
            voice = 0

            for branch in [x for x in note if x in [5,7,9,11,13] ]:
                voice = voice + 2**branch
                voice = (voice%128) + 1
            
            voice_list.append(voice)

        #休符の声部をなくす処理
        if True:

            no_empty_voice = list(set(voice_list))


            no_empty_voice_dict = {}
            
            for i in range(len(no_empty_voice)):
                
                no_empty_voice_dict[ no_empty_voice[i] ] = i

            new_voice_list = []

            for i in voice_list:
                new_voice_list.append( no_empty_voice_dict[i] )

            voice_list = new_voice_list

    return voice_list    


####################################################
#      ＭＩＤＩ出力                                 #
####################################################


#最終的に楽譜を生成する
def midinize(pitch_list,time_list,voice_list):

    
    
    length = 1/8 #一拍の長さ
    howmany_voice = max(voice_list) +1#声部の数

    #時間反転作用↓(Trueで作動)
    if True:
        pitch_list = pitch_list[::-1]
        time_list = time_list[::-1]
        voice_list = voice_list[::-1]

        total =  max(time_list) + length

        for i in range(len(time_list)):
            time_list[i] = total - time_list[i]




    #時間順にソート
    sort_list = []

    for i in range(len(pitch_list)):
        sort_list.append ( [time_list[i],pitch_list[i],voice_list[i]] )


    #（（タイムマーカーの追加））
    if True:
        for i in range(len(time_list)):
            for j in range(howmany_voice):
                sort_list.append( [i*length,998244353,j] )

    sort_list.sort()

    time_list = [ i[0] for i in sort_list]
    pitch_list = [ i[1] for i in sort_list]
    voice_list = [ i[2] for i in sort_list]




    midi_data = pretty_midi.PrettyMIDI(initial_tempo=120)#pretty_midiオブジェクトを作成する。
    


    for i in range(howmany_voice):#声部ごとに処理する。

        new_instrument =   pretty_midi.Instrument(program=2)  #instrumentsinstanceなるものを作成。


        #声部の音を抽出する

        loc_pitch_list = []
        loc_time_list = []

        for j in range(len(voice_list)):

            if voice_list[j] == i:
                loc_pitch_list.append( pitch_list[j] )
                loc_time_list.append( time_list[j] )




        #音の数
        howmany = len(loc_pitch_list)

        
        
        #tieで繋いだ音のリストを作る。
        tie_data = [] #note=[pitch,start,end]


        #tieで保持する音の辞書
        keep = {} #kptone={pitch→start}

        #現在の時刻におけるピッチリスト
        now_pitchlist = []

        time = -1

        #各音素に対して
        for i in range(howmany):
            #もしも時間が新しいならば
            if time != loc_time_list[i]:

                #時間を更新し
                time = loc_time_list[i]

                pop_list = []

                #辞書の中から
                for pitch,start in keep.items():
                    #tieで繋がれなかった音を記録して
                    if not pitch in now_pitchlist:
                        pop_list.append([pitch,start])
                        
                #真のリストに転移する
                for x in pop_list:
                    tie_data.append([x[0],x[1],time-length])
                    keep.pop(x[0])

                #現在のピッチリストを更新する
                now_pitchlist = [loc_pitch_list[i]]
                #もしも辞書にその音が入ってなかったら
                if not loc_pitch_list[i] in keep.keys():
                    #登録する
                    keep[loc_pitch_list[i]] = time
            

            #もしも時間が新しくないならば
            else:
                #現在のピッチリストに音を記録する
                now_pitchlist.append(loc_pitch_list[i])

                #もしも辞書にその音が入ってなかったら
                if not loc_pitch_list[i] in keep.keys():
                    #登録する
                    keep[loc_pitch_list[i]] = time

        #最後に辞書に残った音を転移させる
        for pitch,start in keep.items():
            tie_data.append([pitch,start,time+length])



        for i in tie_data:#各音に対して

            if i[0] != 998244353:#時間コントロール音でなければ

            # NoteInstanceを作成。
                midnote = pretty_midi.Note(
                velocity=127,
                pitch=i[0],
                start=i[1],
                end=i[2]
                )
                # 上記で作成したNoteInstanceをinstrument1に加える。
                new_instrument.notes.append(midnote)

        # 全ての音を追加し終わったら、instrument1をPrettyMIDIオブジェクトに加える。
        midi_data.instruments.append( copy.copy(new_instrument) )




    # PrettyMIDIオブジェクトをMIDIファイルとして書き出す。
    name = datetime.datetime.now().strftime('%Y%m%d%H%M')+'.mid'#日付の名前で
    midi_data.write(name)#書き出す。

    return None




####################################################
#      main関数　　                                 #
####################################################


def main():#まずここが実行される。処理の全体像を記述せよ。

    #定数、縮約木
    ref=5
    R_full_tree = glowing_function(repeat=ref,choice=0)###生成関数のchoice_function、choice=2から外部化
    R_full_tree = [[i for i in j if i>0] for j in R_full_tree]
    R_true_tree = R_full_tree[4:]

    #2進の木集合を生成する。
    tree = glowing_function(repeat=10,choice=0,R_true_tree=R_true_tree,ref=ref)

    #2進の木集合を楽譜に変換する。
    realisation(tree) 

    return None



if __name__ == '__main__':#このファイルが開かれたらmain関数を実行する。
    main()

    #test1()