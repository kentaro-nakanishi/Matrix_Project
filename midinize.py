import datetime#保存するファイル名前を決めるのに時に使う。
import pretty_midi#midinizeでmidiを書き出す時に使う。
import copy#リストに要素を代入するときに使う。

####################################################
#      ＭＩＤＩ出力                                 #
####################################################


#最終的に楽譜を生成する
def midinize(pitch_list,time_list,voice_list):

    length = 1/8 #一拍の長さ
    howmany_voice = int(max(voice_list) +1)#声部の数

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

        new_instrument =   pretty_midi.Instrument(program=2)  #instrumentsinstanceを作成。


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
                pitch=int(i[0]),
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