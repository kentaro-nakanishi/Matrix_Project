import copy#リストに要素を代入するときに使う。

#自作モジュールのインポート
import tree_structure
import synth
import midinize

####################################################
####################################################
#      MATRIX_PROJEKT                              #
####################################################
####################################################


#################################################
#   TERMINAL                                    #
#################################################

#二分木を楽譜に変換する関数
def realisation(tree):

    time_object = tree_structure.List_Adress_Tree(adresses=tree,tree_name='time')
    time_list = time_object.make_time_list()

    pitch_object = tree_structure.List_Adress_Tree(adresses=tree,tree_name='pitch')
    pitch_list = pitch_object.make_time_list()

    voice_object = tree_structure.List_Adress_Tree(adresses=tree,tree_name='voice')
    voice_list = voice_object.make_time_list()

    velocity_object = tree_structure.List_Adress_Tree(adresses=tree,tree_name='velocity')
    velocity_list = velocity_object.make_time_list()

    pan_object = tree_structure.List_Adress_Tree(adresses=tree,tree_name='pan')
    pan_list = pan_object.make_time_list()

    attack_object = tree_structure.List_Adress_Tree(adresses=tree,tree_name='attack')
    attack_list = attack_object.make_time_list()

    tonecolor_object = tree_structure.List_Adress_Tree(adresses=tree,tree_name='tonecolor')
    tonecolor_list = tonecolor_object.make_time_list()


    time_list,pitch_list,voice_list,velocity_list,pan_list,attack_list,tonecolor_list = transP3_unite(time_list,pitch_list,voice_list,velocity_list,pan_list,attack_list,tonecolor_list)



    #midi化する
    midinize.midinize(pitch_list,time_list,voice_list)

    #wave化する
    synth.wavenize(pitch_list,time_list,voice_list,velocity_list,pan_list,attack_list,tonecolor_list)

    return None



def transP3_unite(time_list,pitch_list,voice_list,velocity_list,pan_list,attack_list,tonecolor_list):
    '''
    変換代数後の結合層  tpv直積体を取り、音素に分解する。
    '''

    new_time_list =[]
    new_pitch_list =[]
    new_voice_list =[]
    new_velocity_list =[]
    new_pan_list=[]
    new_attack_list=[]
    new_tonecolor_list=[]

    for index in range(len(time_list)):


        for time in time_list[index]:
            for pitch in pitch_list[index]:
                for voice in voice_list[index]:
                    for velocity in velocity_list[index]:
                        for pan in pan_list[index]:
                            for attack in attack_list[index]:
                                for tonecolor in tonecolor_list[index]:

                                    new_time_list.append(time)
                                    new_pitch_list.append(pitch)
                                    new_voice_list.append(voice)
                                    new_velocity_list.append(velocity)
                                    new_pan_list.append(pan)
                                    new_attack_list.append(attack)
                                    new_tonecolor_list.append([tonecolor,len(tonecolor_list[index])]) ####MIXING_TOOL


    return new_time_list,new_pitch_list,new_voice_list,new_velocity_list,new_pan_list,new_attack_list,new_tonecolor_list



####################################################
#      二分木の元の生成　                            #
####################################################

#木の成長関数
def glowing_function(repeat=18):

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

            #その音に指標を加え(結合関数)
            note.append(digit)

            #木に加える
            new_tree.append(copy.copy(note))

        #関数の再帰化
        tree = copy.copy(new_tree)

    return tree



####################################################
#      main関数　　                                 #
####################################################


def main():#まずここが実行される。処理の全体像を記述せよ。

    #2進の木集合を生成する。
    tree = glowing_function(repeat=9)

    #2進の木集合を楽譜に変換する。
    realisation(tree)

    return None



if __name__ == '__main__':#このファイルが開かれたらmain関数を実行する。
    main()
