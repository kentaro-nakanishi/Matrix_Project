import numpy as np#汎用
import datetime#listsoundで保存するファイル名前を決めるのに時に使う。
from scipy.io.wavfile import write#listsound()に使う。
import matplotlib.pyplot as plt#makegraph,makegraph2に使う。



def listsound(list,txt='',rate=44100*2,nomal=True):#listを日付で保存する。txtは.wav無しの文字列。rateはサンプリングレート。nomalは音量の正規化。
    if nomal == True:#もし正規化がオンなら音量を正規化する。
        list = list * (2**15-1)/np.amax(np.abs(list))  #max(abs(list.real))

    list = list.astype(np.int16)#listの型を変える。虚部は消える。
    write(datetime.datetime.now().strftime('%Y%m%d%H%M')+txt+'.wav',rate,list)#44100Hz(*2)で書き出す。

    #makegraph(list)

    return None#音声ファイルを作成するだけで、何も返さず処理を終了する。

def makegraph(list):#グラフを表示して可視化する。
    listcnp = np.array(list,dtype=complex)#複素数型のndarrayにしておく。
    x = np.arange(len(listcnp))#グラフの横軸は、0から個数-1までの数列。+1すると周波数になる。

    listreal = listcnp.real#実数部を抽出。
    listimag = listcnp.imag#虚数部を抽出。
    listabs = np.abs(listcnp)#絶対値を抽出。
    #listangle = np.angle(listcnp)#偏角を抽出。

    plt.plot(x, listabs, "g",label="abs")#絶対値は緑で表示
    plt.plot(x, -listabs, "g")#絶対値の正負を入れ替えたものも表示
    plt.plot(x, listimag, "r",label="imag")#虚部は赤で表示
    plt.plot(x, listreal, "b",label="real")#実部は青で表示
    #plt.plot(x, listangle, "k")#偏角も黒で表示できる。
    plt.legend(loc="best")#凡例の表示
    plt.show()#グラフを表示
    return None




def wavenize(pitch_list,time_list,voice_list,velocity_list,pan_list,attack_list,tonecolor_list):


    length = 1/8 #一拍の長さ

    #同一音の排除↓(Trueで作動)
    if True:
        total_list=[pitch_list,time_list,voice_list,velocity_list]
        total_list=np.array(total_list).T.tolist()
        total_list=[tuple(x) for x in total_list]
        total_list=list(set(total_list))
        total_list=[list(x) for x in total_list]
        total_list=np.array(total_list).T.tolist()

        pitch_list = total_list[0]
        time_list = total_list[1]
        voice_list = total_list[2]
        velocity_list = total_list[3]

    #時間反転作用↓(Trueで作動)
    if True:
        pitch_list = pitch_list[::-1]
        time_list = time_list[::-1]
        voice_list = voice_list[::-1]
        velocity_list = velocity_list[::-1]

        total =  max(time_list) + length

        for i in range(len(time_list)):
            time_list[i] = total - time_list[i]




    one_note_seconds = 1/6
    sampling_late = 40000

    right_music_wave = np.zeros(int(total * 8 * one_note_seconds * sampling_late) +sampling_late)#最後に一秒間の余韻（残響部）を加える
    left_music_wave = np.zeros(int(total * 8 * one_note_seconds * sampling_late) +sampling_late)#最後に一秒間の余韻（残響部）を加える

    right_music_wave = right_music_wave.astype(np.float32)
    left_music_wave = left_music_wave.astype(np.float32)


    for i in range(len(pitch_list)):#それぞれの音素について、

        note_start_time = int (time_list[i] * 8 * one_note_seconds * sampling_late)

        new_note_wave_right,new_note_wave_left = make_note_wave(
            note_number=pitch_list[i],
            velocity=velocity_list[i],
            pan=pan_list[i],
            attack=attack_list[i],
            tonecolor=tonecolor_list[i],
            note_start_time=note_start_time,
            one_note_seconds=one_note_seconds,
            sampling_late=sampling_late)


        right_music_wave[note_start_time:note_start_time+len(new_note_wave_right)] =right_music_wave[note_start_time:note_start_time+len(new_note_wave_right)] + new_note_wave_right
        left_music_wave [note_start_time:note_start_time+len(new_note_wave_left )] = left_music_wave[note_start_time:note_start_time+len(new_note_wave_left )] + new_note_wave_left


    music_wave= np.array([right_music_wave,left_music_wave]).T

    #音声の生成完了。wavとして出力する。
    listsound(list=music_wave,txt='wave_matrix',rate=sampling_late,nomal=True)



    return None





def make_note_wave(note_number,velocity,pan,attack,tonecolor,note_start_time,one_note_seconds,sampling_late):


    feedin = 1-(attack/127)
    note_length = int (one_note_seconds * sampling_late * (1+feedin))

    #音強曲線
    loudness = (1- velocity/127) * (2/(tonecolor[1]+1))

    velocity_curve = np.full(note_length, loudness)
    velocity_curve[:int(note_length* (feedin/(1+feedin)) )] =np.linspace(0, loudness, int(note_length* (feedin/(1+feedin)) ))
    velocity_curve[int(note_length*(1-(feedin/(1+feedin)))):] =np.linspace(loudness, 0, note_length-int(note_length*(1-(feedin/(1+feedin)))))


    if 1> sampling_late / (440 * 2**(note_number/12) ):#例外処理：高すぎる音
        return np.zeros(1)

    one_pulse_length = int ( sampling_late / (440 * 2**( (note_number-60) /12) ) )


    edge = tonecolor[0]/127

    single_pitch_wave = np.zeros(one_pulse_length)

    single_pitch_wave[:int(one_pulse_length*edge/2)] = np.linspace(0,1,int(one_pulse_length*edge/2))
    single_pitch_wave[int(one_pulse_length*edge/2):] = np.linspace(1,0,one_pulse_length-int(one_pulse_length*edge/2))

    original_pitch_wave = np.tile(single_pitch_wave, int((note_length/one_pulse_length)+4))


    #位相調整
    phase_length = (note_start_time % one_pulse_length) + (2**(1/2))*one_pulse_length#最後の定数は位相が揃ってピークが重なるのを避けるため
    phase_length = int(phase_length)
    original_pitch_wave = original_pitch_wave[phase_length : phase_length+note_length]

    output_note_wave = np.multiply(velocity_curve,original_pitch_wave)

    #pan調整
    new_note_wave_right =output_note_wave *(1/2 + pan/2)
    new_note_wave_left  =output_note_wave *(1/2 - pan/2)

    return new_note_wave_right,new_note_wave_left


def test():

    pitch_list =[ 40, 40, 40, 40]
    time_list  =[4/4,5/4,6/4,7/4]
    voice_list =[  1,  1,  1,  1]
    wavenize(pitch_list,time_list,voice_list)

if __name__ == '__main__':#このファイルが開かれたらmain関数を実行する。
    test()