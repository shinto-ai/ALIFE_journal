# import statements
import numpy as np
import math
import perlin_noise_python_numpy as perlin
#import conrad.perlin_noise_python_numpy as perlin
import matplotlib.cm as cm
import random
from scipy import signal
from scipy import ndimage



# Numbers
# 特定の数学的特性（例：X軸とY軸の位置、円周率、ネイピア数、ランダムな値）を組み合わせて、視覚的なテクスチャやパターンを生成するために使用

# 200×200のグリッドを生成
x_inds = np.array([[[x / 100, x / 100, x / 100] for x in range(-100, 100)] for i in range(200)])
y_inds = np.array([[[y / 100, y / 100, y / 100] for i in range(200)] for y in range(-100, 100)])
e_inds = np.array([[[math.e, math.e, math.e] for i in range(200)] for y in range(200)])
pi_inds = np.array([[[math.pi, math.pi, math.pi] for i in range(200)] for y in range(200)])


# ランダムな[0,1)範囲の数値を各要素に3つ持つ200×200のグリッドを生成
def r_inds():
    r3 = [random.random(), random.random(), random.random()]
    return np.array([[r3 for i in range(200)] for y in range(200)])


# 500×500のグリッドを生成
x_inds500 = np.array([[[x / 250, x / 250, x / 250] for x in range(-250, 250)] for i in range(500)])
y_inds500 = np.array([[[y / 250, y / 250, y / 250] for i in range(500)] for y in range(-250, 250)])
e_inds500 = np.array([[[math.e, math.e, math.e] for i in range(500)] for y in range(500)])
pi_inds500 = np.array([[[math.pi, math.pi, math.pi] for i in range(500)] for y in range(500)])


# ランダムな[0,1)範囲の数値を各要素に3つ持つ500×500のグリッドを生成
def r_inds500():
    r3 = [random.random(), random.random(), random.random()]
    return np.array([[r3 for i in range(500)] for y in range(500)])


# #より大きなグリッド (800×800)
# x_inds800 = np.array([[[x / 400, x / 400, x / 400] for x in range(-400, 400)] for i in range(800)])
# y_inds800 = np.array([[[y / 400, y / 400, y / 400] for i in range(800)] for y in range(-400, 400)])
# e_inds800 = np.array([[[math.e, math.e, math.e] for i in range(800)] for y in range(800)])
# pi_inds800 = np.array([[[math.pi, math.pi, math.pi] for i in range(800)] for y in range(800)])
#
# def r_inds800():
#     r3 = [random.random(), random.random(), random.random()]
#     return np.array([[r3 for i in range(800)] for y in range(800)])


# #より大きなグリッド (デスクトップサイズ)
# x_inds_desktop = np.array([[[x/1920, x/1920, x/1920] for x in range(-960, 960)] for i in range(1080)])
# y_inds_desktop = np.array([[[y/1080, y/1080, y/1080] for i in range(1920)] for y in range(-540, 540)])
# e_inds_desktop = np.array([[[math.e, math.e, math.e] for i in range(1920)] for y in range(1080)])
# pi_inds_desktop = np.array([[[math.pi, math.pi, math.pi] for i in range(1920)] for y in range(1080)])
# r3 = [random.random(), random.random(), random.random()]
# r_inds_desktop = np.array([[r3 for i in range(1920)] for y in range(1080)])


# #より大きなグリッド (ヘッダーサイズ)
# x_inds_header = np.array([[[x/100, x/100, x/100] for x in range(-1000, 1000)] for i in range(2000)])
# y_inds_header = np.array([[[y/100, y/100, y/100] for i in range(2000)] for y in range(-1000, 1000)])
# e_inds_header = np.array([[[math.e, math.e, math.e] for i in range(2000)] for y in range(2000)])
# pi_inds_header = np.array([[[math.pi, math.pi, math.pi] for i in range(2000)] for y in range(2000)])
#
# def r_inds_header():
#     r3 = [random.random(), random.random(), random.random()]
#     return np.array([[r3 for i in range(2000)] for y in range(2000)])


# 各グリッドを辞書型で保持
num_dict = {'x': x_inds, 'y': y_inds, 'p': pi_inds, 'e': e_inds, 'r': r_inds()}
num_dict500 = {'x': x_inds500, 'y': y_inds500, 'p': pi_inds500, 'e': e_inds500, 'r': r_inds500()}
# num_dict800 = {'x': x_inds800, 'y': y_inds800, 'p': pi_inds800, 'e': e_inds800, 'r': r_inds800()}
# num_dict_desktop = {'x':x_inds_desktop, 'y':y_inds_desktop, 'p':pi_inds_desktop, 'e':e_inds_desktop, 'r':r_inds_desktop}
# num_dictheader = {'x': x_inds_header, 'y': y_inds_header, 'p': pi_inds_header, 'e': e_inds_header, 'r': r_inds_header()}





# 指定されたコードと配列サイズに基づいて、特定の数値パターンを持つ配列を生成する
def numbers(code, array_size=(200, 200)):
    if array_size == (200, 200):
        dict = num_dict
    elif array_size == (500, 500):
        dict = num_dict500
    # elif array_size == (800, 800):
    #     dict = num_dict800
    # elif array_size == (1920, 1080):
    #     dict = num_dictheader
    # elif array_size == (2000, 2000):
    #     dict = num_dictheader
        
    # codeのkeyで指定されたグリッドを取得
    el0 = dict[code[0]]
    el1 = dict[code[1]]
    el2 = dict[code[2]]

    # これらの配列を組み合わせて3次元配列outを生成
    out = np.array(
        [[[el0[y][i][0], el1[y][i][1], el2[y][i][2]] for i in range(array_size[0])] for y in range(array_size[1])])
    return out

# Safe array functions
# エラーや数学的に定義できない動作を避けるための関数集

# 符号反転
def invert(no):
    return (no * -1)


# 自然対数の計算において負の値や0を避ける(noが配列)
def myloge(no):
    no[no <= 0] = 0.001
    return np.log(no)


# mylogeと同様だが、基数を指定できる(noが配列)
def mylog(no, base):
    no[no <= 0] = 0.001
    return np.log(no)


# 自然対数の計算において負の値や0を避ける(noが単一の数値)
def myslog(no):
    if no <= 0:
        no = 0.001
    return math.log(no)


# mod計算。0で割らないようにする。
def mymod(no, div):
    div[div == 0] = 1
    return no % div


# 割り算。0で割らないようにする。
def mydiv(no, div):
    div[div == 0] = 1
    return no / div


# 引き算
def myminus(a, b):
    return a - b


# 掛け算
def myproduct(a, b):
    return (a * b)


# べき乗計算。オーバーフローやアンダーフローを防ぐ。
def myexp(a, b):
    try:
        b = np.round(b)
        a[np.bitwise_and(a <= 0, b <= 1)] = abs(a[np.bitwise_and(a <= 0, b <= 1)])
        a[a == 0] = 0.00001
        b[b > 10] = mylog(b[b > 10] * 2300, 10)
        a[a > 300] = mylog(a[a > 300] * 6.474754650804084e+127, 10)
        out = a ** b
        return out
    except:
        # print("EXP FAIL ON {0} ** {1}").format(a, b)
        print("EXP FAIL")
        return a ** 2

# # aが負の時にエラー出るので変更。⇒ やっぱりやめた。
# def myexp(a, b):
#     try:
#         b = np.round(b)
#         negative_base_mask = a < 0
#         a[negative_base_mask] = abs(a[negative_base_mask])
#         a[a == 0] = 0.00001
#         b[b > 10] = mylog(b[b > 10] * 2300, 10)
#         a[a > 300] = mylog(a[a > 300] * 6.474754650804084e+127, 10)
#         out = a ** b
#         out[negative_base_mask] = -out[negative_base_mask]  # 負の底を持つべき乗の結果を負にする
#         return out
#     except:
#         # print("EXP FAIL ON {0} ** {1}").format(a, b)
#         print("EXP FAIL")
#         return a ** 2



# 足し算
def mysum(a, b):
    return a + b


# round関数をベクトル化し、配列の各要素を個別に丸めることができる。
npround = np.vectorize(round)


# bを調整することで丸め性度をカスタム可。
def myround(a, b):
    b = abs(b) * 10
    b[b<1] = b[b<1] +1
    return npround(a, b.astype(int))

# 2倍
def by2(no):
    return no * 2


# 10倍
def by10(no):
    return no * 10


# 100倍
def by100(no):
    return no * 100


# 平方根(絶対値に変換してから。)
def mysqrt(no):
    return np.sqrt(abs(no))


# 引数にランダムな数をかける。
def mynoise(no):
    return (1.0 * (no)) * random.random()


# 4つの入力を乱数に基づく条件で操作
def myif(a, b, c, d):
    try:
        h, i, j, k = random.sample([a, b, c, d], 4)
        #h, i, j, k = a, b, c, d
        out = h
        out[j > i] = k[j > i]
        return out
    except ValueError:
        print(ValueError, a.shape, b.shape, c.shape, d.shape)
        return a
    return np.array(out)


# myifの文字列バージョン
def s_myif(a, b, c, d):
    h, i, j, k = random.sample([a, b, c, d], 4)
    #h, i, j, k = a, b, c, d
    return ("{0} if {1} > {2} else {3}".format(h, i, j, k))


# 平均
def mymean(a, b):
    return (a + b) / 2


# 平方。10000以上の場合は対数を取って定数倍
def mysquare(no):
    out = no
    out[no < 100000] = no[no < 100000] ** 2
    out[no >= 100000] = np.log(no[no >= 100000]) * 1087
    return out


# 配列の合計が大きい方を返す
def mymax(a, b):
    at = a.sum()
    bt = b.sum()
    if at >= bt:
        return a
    else:
        return b


# 配列の合計が小さい方を返す
def mymin(a, b):
    at = a.sum()
    bt = b.sum()
    if at <= bt:
        return a
    else:
        return b


# 与えられた配列に対して、波形の変形（ワーピング）を適用
def warp(array, array2):
    shift_func = random.choice([np.sin, np.cos, np.tan])
    k = random.choice([0.1, 0.5, 1, 2, 10])#[int(np.sum(array2[:, :, 0]) % 5)]
    A = array.shape[0] / 3.0
    w = 2.0 / array.shape[1]

    #shift = lambda x: A * shift_func(k * np.pi * x * w)
    shift = lambda x: shift_func(k * np.pi * x)

    for i in range(array.shape[0]):
        array[:, i] = np.roll(array[:, i], int(shift(i)))
    return array


# 配列の勾配を計算しelement(何これ)を適用
def gradient(array, codon):
    out = np.gradient(array)
    return element(out)


# 配列の勾配を計算し、x成分を返す
def gradient0(array):
    out = np.gradient(array)
    return out[0]


# 配列の勾配を計算し、y成分を返す
def gradient1(array):
    out = np.gradient(array)
    return out[1]


# 配列の勾配を計算し、y成分を返す
def gradient2(array):
    out = np.gradient(array)
    return out[2]


# 畳み込み(全ての要素が1の3×1のカーネル)
def quick_convolve(array1):
    k = [[[1,1,1]]]
    out = ndimage.convolve(array1, k, mode='constant', cval=0.0)
    return out


# バンドパスフィルタの適用
def band_pass(img):
    f = np.fft.fft2(img)                  #do the fourier transform
    fshift1 = np.fft.fftshift(f)          #shift the zero to the center
    f_ishift = np.fft.ifftshift(fshift1)  #inverse shift
    img_back = np.fft.ifft2(f_ishift)     #inverse fourier transform
    img_back = np.abs(img_back)
    return img_back


# ランダムなカーネルを使用した畳み込み
def convolve(array1, codon):
    k = np.array([[[random.randint(0, 5) for x in range(3)]]])
    out = ndimage.convolve(array1, k, mode='constant', cval=0.0)
    return out


#  画像に放射状の変形を適用し、色のマッピングを通じて視覚的なエフェクトを生成
def radial(array, codon):
    fraction = random.choice([0.5, 0.25, 0.1, 0.05])#[int(np.sum(array2[:, :, 0]) % 4)]
    sx, sy, _ = array.shape
    X, Y = np.ogrid[-sx/2:sx/2, -sy/2:sy/2]
    X = X/(sx/2)
    Y = Y/(sy/2)
    r = np.hypot(X, Y)
    rbin = ((fraction) * r/r.max())

    cmap = 'hsv'
    rgba = cm.ScalarMappable(cmap='hsv').to_rgba(rbin)
    rgb = rgba[:, :, :3]
    out = array * rgb
    return out


# 与えられた数値の約数を生成
def divisorGenerator(n):
    for i in range(1,int(n/2)+1):
        if n%i == 0: yield i
    yield n


# Perlinノイズを適用し、特定の色マッピングを通じてエフェクトを生成
def perlin_noise(array, codon):
    size = array.shape[0]
    divisors = list(divisorGenerator(size))
    divisors.sort(reverse=True)
    no_filters = {'A':1, 'C':1, 'G':2, 'T':3}[codon[0]]
    start = {'A':1, 'C':2, 'G':3, 'T':4}[codon[1]]
    noises = []
    for i in range(start, start+no_filters):
        ns = divisors[i]
        noise = perlin.generate_2D_perlin_noise(size, ns)
        noises.append(noise)
    noise = sum(noises)/len(noises)
    cmap = {'A':'hsv', 'C':'terrain', 'G':'gist_rainbow', 'T':'inferno'}[codon[2]]
    noisergba = cm.ScalarMappable(cmap=cmap).to_rgba(noise)
    noisergb = noisergba[:, :, :3]
    out = array * noisergb
    return out


# 画像を特定の方向にシフト（ロール）させることで、画像を平行移動させる
def roll(array, codon):
    ysize = array.shape[0]
    xsize = array.shape[1]
    fraction =  {'A':-2, 'C':-1, 'G':1, 'T':2}[codon[1]] * {'A':0.05, 'C':0.15, 'G':0.25, 'T':0.5}[codon[2]]
    yshift = int(fraction * ysize)
    xshift = int(fraction * xsize)
    out = {'A':np.roll(array, yshift, axis = 0),
           'C':np.roll(array, xshift, axis = 1),
           'G':np.roll(np.roll(array, yshift, axis = 0), xshift, axis = 1),
           'T':np.roll(np.roll(array, -yshift, axis = 0), xshift, axis = 1)}[codon[0]]
    return out


# 画像を指定された角度で回転
def rotate(array, codon='CAG'):
    m = {'A':'constant', 'C':'nearest', 'G':'wrap', 'T':'reflect'}[codon[0]]
    angle = {'A':1, 'C':2, 'G':3, 'T':4}[codon[1]] * {'A':5, 'C':15, 'G':45, 'T':90}[codon[2]]
    out = ndimage.rotate(array, angle, mode=m, reshape=False, cval=0.05)
    return out


# 画像に放射状の色彩変化を適用
def radial(array, codon):
    """Adapted from https://www.scipy-lectures.org/advanced/image_processing/auto_examples/plot_radial_mean.html"""
    fraction = {'A':0.5, 'C':0.1, 'G':0.05, 'T':0.02}[codon[0]]
    sx, sy, _ = array.shape
    X, Y = np.ogrid[-sx/2:sx/2, -sy/2:sy/2]
    if codon[1] in ['G', 'T']:
        offset = {'GA':(-0.5,-0.5), 'GC':(-0.25, -0.25), 'GG':(0.25, 0.25), 'GT':(0.5, 0.5),
                  'TA': (0, -0.5), 'TC': (-0.5, 0), 'TG': (-0.5, 0.5), 'TT': (0.5, -0.5)}[codon[1:3]]
    else:
        offset = (0,0)
    X = X/(sx/2)
    Y = Y/(sy/2)
    r = np.hypot(X+offset[0], Y+offset[1])
    rbin = ((fraction * sx) * r/r.max()).astype(int)
    rgba = cm.ScalarMappable(cmap='hsv').to_rgba(rbin)
    rgb = rgba[:, :, :3]
    out = array * rgb
    return out


# コドンによってカーネルを生成し畳み込みを適用
def convolve(array1, codon):
    k = np.array([[[{'A':0, 'C':1, 'G':2, 'T':3}[x] for x in codon]]])
    out = ndimage.convolve(array1, k, mode='constant', cval=0.0)
    return out


# 画像に曲線的な色彩変化を適用
def curvy(array, codon):
    fraction = {'A': 0.5, 'C': 0.1, 'G': 0.05, 'T': 0.02}[codon[0]]
    sx, sy, _ = array.shape
    X, Y = np.ogrid[-sx / 2:sx / 2, -sy / 2:sy / 2]
    xfunc = {'A':np.sin, 'C':np.cos, 'G':np.tan, 'T':np.arctan}[codon[1]]
    yfunc = {'A': np.sin, 'C': np.cos, 'G': np.tan, 'T': np.arctan}[codon[2]]
    X = X / (sx / 2)
    Y = Y / (sy / 2)
    rx = [random.random()/50 for r in range(sx)]
    ry = [random.random()/50 for r in range(sy)]
    r = (yfunc(Y) * xfunc(X))
    rbin = ((fraction * sx) * r / r.max()).astype(int)
    rgba = cm.ScalarMappable(cmap='hsv').to_rgba(rbin)
    rgb = rgba[:, :, :3]
    out = array * rgb
    return out


# 引数によって指定された軸と方向に反射させる
def reflect_kernel(array, axis, mirror, direction):
    sy, sx, _ = array.shape
    if axis == 0:
        if direction == 0:
            if mirror == 0:
                array[round(sy / 2):, :] = array[0:round(sy/2),::]
            elif mirror == 1:
                array[round(sy / 2):, :] = np.flipud(array[0:round(sy / 2), ::])
        elif direction == 1:
            if mirror == 0:
                 array[0:round(sy/2),::] = array[round(sy / 2):, :]
            elif mirror == 1:
                array[0:round(sy / 2), ::] = np.flipud(array[round(sy / 2):, :])
    elif axis == 1:
        if direction == 0:
            if mirror == 0:
                array[:, round(sx / 2):, :] = array[:,:round(sx / 2),:]
            elif mirror == 1:
                array[:, round(sx / 2):, :] = np.fliplr(array[:, :round(sx / 2), :])
        elif direction == 1:
            if mirror == 0:
                 array[:,:round(sx / 2),:] = array[:, round(sx / 2):, :]
            elif mirror == 1:
                array[:, :round(sx / 2), :] = np.fliplr(array[:, round(sx / 2):, :])
    return array


# コドンに基づいて反射させる
def reflect(array, codon):
    axis = {'A':0, 'C':0, 'G':1, 'T':1}
    mirror = {'A': 0, 'C': 1, 'G': 1, 'T': 1}
    direction = {'A':0, 'C':0, 'G':1, 'T':1}


    if codon[2] in ['A', 'T']:
        temp = reflect_kernel(array, axis[codon[0]], mirror[codon[1]], direction[codon[2]])
        out = reflect_kernel(temp, 1 - axis[codon[0]], mirror[codon[0]], direction[codon[1]])
    else:
        out = reflect_kernel(array, axis[codon[0]], mirror[codon[1]], direction[codon[2]])
    return out


# 画像を波形に変形（ワープ）させることで、動的な視覚エフェクトを生成
def warp(array, codon):
    shift_func = {'A':np.sin, 'C':np.cos, 'G':np.tan, 'T':np.arctan}[codon[0]]
    k = {'A':0.5, 'C':1, 'G':2, 'T':4}[codon[1]]
    A = array.shape[0] / 3.0
    w = k / array.shape[1]

    shift = lambda x: A * shift_func(k * np.pi * x * w)

    for i in range(array.shape[0]):
        array[:, i] = np.roll(array[:, i], int(shift(i)), axis=0)
    return array



# Read Gene Variables
# コドンに基づいて特定の関数を選択し、実行するための変数と辞書を定義

#コドンを特定の文字列にマッピング
num = {"AA": 'xxx', "AC": 'xxy', "AG": 'xyx', "AT": 'yxx',
       "CA": 'yyy', "CC": "yyx", "CG": "yxy", "CT": "xyy",
       "GA": 'xxr', "GC": "xry", "GG": "yxr", "GT": "ryy",
       "TA": 'per', "TC": "rep", "TG": "epe", "TT": "rrr"}

# 単一の引数を取る関数にコドンをマッピング
onearg = {"AA": abs, "AC": mysquare, "AG": invert, "AT": mynoise,
          "CA": gradient2, "CC": by10, "CG": by100, "CT": by2,
          "GA": np.sin, "GC": np.cos, "GG": np.tan, "GT": gradient1,
          "TA": myloge, "TC": band_pass, "TG": mysqrt, "TT": gradient0}

# 2つの引数を取る関数にコドンをマッピング
twoargs = {"AA": mysum, "AC": mysum, "AG": myminus, "AT": myminus,
           "CA": myproduct, "CC": myproduct, "CG": mydiv, "CT": mydiv,
           "GA": mymod, "GC": myround, "GG": myexp, "GT": mylog,
           "TA": mymax, "TC": mymin, "TG": mymean, "TT": myround}

# 画像処理や特定のエフェクトを適用する関数にコドンをマッピング
oneargplus = {"AA": perlin_noise, "AC": perlin_noise, "AG": convolve, "AT": convolve,
           "CA": radial, "CC": radial, "CG": roll, "CT": roll,
           "GA": curvy, "GC": curvy, "GG": rotate, "GT": rotate,
           "TA": reflect, "TC": reflect, "TG": warp, "TT": warp}

control = {"A": onearg, "C": twoargs, "G": myif, "T": oneargplus}
first = {"A": onearg, "C": twoargs, "G": myif, "T": oneargplus}



# Print Gene variables
# 上記の関数と変数のマッピングを、よりシンプルで直接的な文字列ベースの表現に変換

s_num = {"AA": 'numbers("xxx")', "AC": 'numbers("xxy")', "AG": 'numbers("xyx")', "AT": 'numbers("yxx")',
       "CA": 'numbers("yyy")', "CC": "numbers('yyx')", "CG": "numbers('yxy')", "CT": "numbers('xyy')",
       "GA": 'numbers("xxr")', "GC": "numbers('xry')", "GG": "numbers('yxr')", "GT": "numbers('ryy')",
       "TA": 'numbers("per")', "TC": "numbers('rep')", "TG": "numbers('epe')", "TT": "numbers('rrr')"}

s_onearg = {"AA": 'abs', "AC": 'square', "AG": 'invert', "AT": 'noise',
            "CA": 'gradient[2]', "CC": '10 *', "CG": '100 *', "CT": '2 *',
            "GA": 'sin', "GC": 'cos', "GG": 'tan', "GT": 'gradient[1]',
            "TA": 'logn', "TC": 'band pass', "TG": 'sqrt', "TT": 'gradient[0]'}

s_twoargs = {"AA": 'sum', "AC": 'sum', "AG": 'minus', "AT": 'minus',
             "CA": 'product', "CC": 'product', "CG": 'divide', "CT": 'divide',
             "GA": 'mod', "GC": 'round', "GG": 'exp', "GT": 'log',
             "TA": 'max', "TC": 'min', "TG": 'mean', "TT": 'round'}


s_oneargplus = {"AA": 'perlin_noise', "AC": 'perlin_noise', "AG": 'convolve', "AT": 'convolve',
           "CA": 'radial', "CC": 'radial', "CG": 'roll', "CT": 'roll',
           "GA": 'curvy', "GC": 'curvy', "GG": 'rotate', "GT": 'rotate',
           "TA": 'reflect', "TC": 'reflect', "TG": 'warp', "TT": 'warp'}

s_control = {"A": s_onearg, "C": s_twoargs, "G": myif, "T": s_oneargplus}
s_first = {"A": s_onearg, "C": s_twoargs, "G": myif, "T": s_oneargplus}



# Read Genomes
# 遺伝子配列（genome）を解析し、対応する画像処理関数を再帰的に適用することで、最終的な画像やパターンを生成するロジックを実装


# 遺伝子配列を読み取り、指定された深さ（depth）と現在の位置（acc）に基づいて、適切な画像処理関数を再帰的に適用
def read_gene(genome, depth, acc, size):
    if depth >= (len(genome) - 1) - acc:
        return numbers(num[genome[acc:acc + 2]], size)
    elif depth == 0:
        d = first[genome[acc - 1]]
    else:
        d = control[genome[acc - 1]]

    if d == onearg:
        arg1 = read_gene(genome, depth + 3, acc + 3, size)
        return d[genome[acc:acc + 2]](arg1)
    elif d == oneargplus:
        return d[genome[acc:acc + 2]](read_gene(genome, depth + 3, acc + 3, size),
                                      genome[acc+6:acc+9])
    elif d == twoargs:
        return d[genome[acc:acc + 2]](read_gene(genome, depth + 3, acc + 3, size),
                                      read_gene(genome, depth + 6, acc + 6, size))
    elif d == num:
        return numbers(num[genome[acc:acc + 2]], size)
    else:
        return myif(read_gene(genome, depth + 3, acc + 3, size), read_gene(genome, depth + 6, acc + 6, size),
                    read_gene(genome, depth + 9, acc + 9, size), read_gene(genome, depth + 12, acc + 12, size))



# read_gene関数に対応する文字列表現を生成し、遺伝子配列がどのような画像処理操作を表しているかを示す
def print_gene(genome, depth, acc):
    if depth >= (len(genome) - 1) - acc:
        return s_num[genome[acc:acc + 2]]
    elif depth == 0:
        d = s_first[genome[acc - 1]]
    else:
        d = s_control[genome[acc - 1]]
    if d == s_onearg:
        return "{0}({1})".format(d[genome[acc:acc + 2]], str(print_gene(genome, depth + 3, acc + 3)))
    elif d == oneargplus:
        return "{0}({1}, {2})".format(d[genome[acc:acc + 2]](print_gene(genome, depth + 3, acc + 3),
                                      genome[acc+6:acc+9]))
    elif d == s_twoargs:
        return "{0}({1}, {2})".format(d[genome[acc:acc + 2]], print_gene(genome, depth + 3, acc + 3),
                                      print_gene(genome, depth + 6, acc + 6))
    elif d == num:
        return s_num[genome[acc:acc + 2]]
    else:
        return s_myif(print_gene(genome, depth + 3, acc + 3), print_gene(genome, depth + 6, acc + 6),
                      print_gene(genome, depth + 9, acc + 9), print_gene(genome, depth + 12, acc + 12))


