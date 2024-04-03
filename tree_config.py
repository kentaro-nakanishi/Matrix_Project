
import numpy as np
def to_bool_config(tree_name='none',bool_pattern=0, D=0,U=0,R=0):
    '''
    変換代数において、縮約、非縮約を決定するbool値を返す。
    '''

    if tree_name =='time':

        if bool_pattern == 0:##org_treeにて、縮約番号の指示を出す
            return ((D-U*(1/2)+(R))<=4)

        if bool_pattern == 1:#2-変換代数のleft_treeにて、縮約番号の指示を出す
            #dim_pattern
            return D>=10

        if bool_pattern == 2:#2-変換代数のright_treeにて、縮約番号の指示を出す
            #dim_pattern
            return D>=10

        if bool_pattern == 3:#make_brotherのmatching_patternの検索。
            #dim_pattern
            return 2

        if bool_pattern == 4:#bool_pattern == 0がTrueのとき、　更に  1_変換代数のdim_patternを設定する。
            dim_pattern = {'D':D,'U':U,'R':R}
            return dim_pattern

    if tree_name =='pitch':

        if bool_pattern == 0:##org_treeにて、縮約番号の指示を出す
            return (D<5)

        if bool_pattern == 1:#2-変換代数のleft_treeにて、縮約番号の指示を出す
            #dim_pattern
            return True

        if bool_pattern == 2:#2-変換代数のright_treeにて、縮約番号の指示を出す
            #dim_pattern
            return True

        if bool_pattern == 3:#make_brotherのmatching_patternの検索。
            #dim_pattern
            return 3

        if bool_pattern == 4:#bool_pattern == 0がTrueのとき、　更に  1_変換代数のdim_patternを設定する。
            dim_pattern = {'D':D,'U':U,'R':R}
            return dim_pattern

    if tree_name =='voice':

        if bool_pattern == 0:##org_treeにて、縮約番号の指示を出す
            return True

        if bool_pattern == 1:#2-変換代数のleft_treeにて、縮約番号の指示を出す
            return D>=10

        if bool_pattern == 2:#2-変換代数のright_treeにて、縮約番号の指示を出す
            return D>=10

        if bool_pattern == 3:#make_brotherのmatching_patternの検索。
            return 2

        if bool_pattern == 4:#bool_pattern == 0がTrueのとき、　更に  1_変換代数のdim_patternを設定する。
            dim_pattern = {'D':D,'U':U,'R':R}
            return dim_pattern

    if tree_name =='velocity':

        if bool_pattern == 0:##org_treeにて、縮約番号の指示を出す
            return  (D%2)

        if bool_pattern == 1:#2-変換代数のleft_treeにて、縮約番号の指示を出す
            return D>=10

        if bool_pattern == 2:#2-変換代数のright_treeにて、縮約番号の指示を出す
            return D>=10

        if bool_pattern == 3:#make_brotherのmatching_patternの検索。
            return 2

        if bool_pattern == 4:#bool_pattern == 0がTrueのとき、　更に  1_変換代数のdim_patternを設定する。
            dim_pattern = {'D':D,'U':U,'R':R}
            return dim_pattern

    if tree_name =='pan':

        if bool_pattern == 0:##org_treeにて、縮約番号の指示を出す
            return  (D%3)

        if bool_pattern == 1:#2-変換代数のleft_treeにて、縮約番号の指示を出す
            return D>=10

        if bool_pattern == 2:#2-変換代数のright_treeにて、縮約番号の指示を出す
            return D>=10

        if bool_pattern == 3:#make_brotherのmatching_patternの検索。
            return 2

        if bool_pattern == 4:#bool_pattern == 0がTrueのとき、　更に  1_変換代数のdim_patternを設定する。
            dim_pattern = {'D':D,'U':U,'R':R}
            return dim_pattern

    if tree_name =='attack':

        if bool_pattern == 0:##org_treeにて、縮約番号の指示を出す
            return  (D-U)%2

        if bool_pattern == 1:#2-変換代数のleft_treeにて、縮約番号の指示を出す
            return D>=10

        if bool_pattern == 2:#2-変換代数のright_treeにて、縮約番号の指示を出す
            return D>=10

        if bool_pattern == 3:#make_brotherのmatching_patternの検索。
            return 2

        if bool_pattern == 4:#bool_pattern == 0がTrueのとき、　更に  1_変換代数のdim_patternを設定する。
            dim_pattern = {'D':D,'U':U,'R':R}
            return dim_pattern

    if tree_name =='tonecolor':

        if bool_pattern == 0:##org_treeにて、縮約番号の指示を出す
            return  (D-U)%3

        if bool_pattern == 1:#2-変換代数のleft_treeにて、縮約番号の指示を出す
            return True

        if bool_pattern == 2:#2-変換代数のright_treeにて、縮約番号の指示を出す
            return True

        if bool_pattern == 3:#make_brotherのmatching_patternの検索。
            return 2

        if bool_pattern == 4:#bool_pattern == 0がTrueのとき、　更に  1_変換代数のdim_patternを設定する。
            dim_pattern = {'D':D,'U':U,'R':R}
            return dim_pattern


    print('to_bool_config error')
    return None







def output_range_config(tree,tree_name='none'):

    if tree_name =='time':
        return [[i*1/8 for i in j] for j in tree]
    if tree_name =='pitch':
        return [[i*19/31 +0 for i in j] for j in tree]
    if tree_name =='voice':
        return tree
    if tree_name =='velocity':

        #平均化
        velocity_list = [sum(i)/len(i) for i in tree]
        max_velocity = max(velocity_list)
        min_velocity = min(velocity_list)
        range_velocity = max_velocity-min_velocity

        #値域を1～127の整数値に設定
        return [ [int(1+ 126*(i-min_velocity)/range_velocity)] for i in velocity_list]

    if tree_name =='pan':

        #平均化
        pan_list = [sum(i)/len(i) for i in tree]
        max_pan = max(pan_list)
        min_pan = min(pan_list)
        range_pan = max_pan-min_pan

        #値域を-1～1に設定
        return [ [-1+ 2*(i-min_pan)/range_pan] for i in pan_list]


    if tree_name =='attack':

        max_velocity = max([max(i) for i in tree])
        min_velocity = min([min(i) for i in tree])
        range_velocity = max_velocity-min_velocity

        #値域を1～127の整数値に設定
        return [[ int(1+ 126*(i-min_velocity)/range_velocity) for i in j] for j in tree]

    if tree_name =='tonecolor':

        max_velocity = max(sum(tree, []))
        min_velocity = min(sum(tree, []))
        range_velocity = max_velocity-min_velocity

        #値域を1～127の整数値に設定

        return [[ int(1+ 126*(i-min_velocity)/range_velocity) for i in j] for j in tree]


    print('output_range_config error')
    return None







def cycle_trans_config(tree_name='none'):
    '''
    循環変換代数の有効化/無効化を切り替える。
    '''

    if tree_name =='time':
        return True
    if tree_name =='pitch':
        return True
    if tree_name =='voice':
        return False
    if tree_name =='velocity':
        return False
    if tree_name =='pan':
        return False
    if tree_name =='attack':
        return False
    if tree_name =='tonecolor':
        return False

    print('cycle_trans_config error')
    return False