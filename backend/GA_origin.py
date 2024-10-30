import random
import PIL
from PIL import Image, ImageColor
import numpy as np
import math
from itertools import chain
import pandas as pd
import image as image
#import conrad.image as image
from models_local import Artist
import csv
import os



def list_to_dict(data_list):
    keys = ["id", "generation", "member", "genome", "fitness", "father", "mother", "rank"]
    return dict(zip(keys, data_list))



def write_to_csv(file_path, data_list):
    data_dict = list_to_dict(data_list)  # リストを辞書に変換
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "generation", "member", "genome", "fitness", "father", "mother", "rank"])
        
        if not file_exists:
            writer.writeheader()  # ファイルが新規作成される場合はヘッダーを書き込む
        
        writer.writerow(data_dict)



#指定された長さ（popsize）のランダムな「ACGT」文字列を生成
def birth(popsize):
    return ''.join([random.sample('ACGT', 1)[0] for i in range(popsize)])



# popsizeに基づいて新しい個体群を生成
def firstpop(popsize, genelength):
    first_pop =[]
    for i in range(popsize):
        a = Artist(generation=0, member=i, genome=birth(genelength))
        first_pop.append(a)
    return(first_pop)



# Not genuine normalization but the images are improved
    #To do - reconcile these two
def normalized(a, axis=-1, order=np.inf):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)



#遺伝子情報を表す文字列を基に画像を生成
def display(agent, size=(200, 200)):
    # agent(ゲノム文字列)をもとにシード値を生成(再現性確保のため)
    random.seed(agent)
    np.random.seed(sum([ord(x) for x in agent])) #agentの各文字のASCII値の合計

    pixels = image.read_gene(agent, 0, 1, size)
    outnorm = normalized(pixels) * 255
    im = Image.fromarray(np.uint8(outnorm))
    return im


# 要注目！
# 現在：トーナメントの勝者は、ユーザーが左なら1、右なら2をターミナルから入力することで決定される
# 変更：トーナメントの勝者は、フロントエンドでのユーザーの選択によって決定される


# トーナメント戦を実行する関数
def tournament(pop):
    """トーナメント戦を実行し、各ラウンドの勝者を返す関数。
    
    Args:
        artists (list): Artistオブジェクトのリスト。
    
    Returns:
        list: 各ラウンドの勝者のリストのリスト。
    """
    winners = pop  # 現在のラウンドの勝者を保持するリスト
    rounds = []  # 各ラウンドの勝者を格納するリストのリスト
    rounds.append(pop)

    # 勝者が1人になるまでトーナメントを続ける
    while len(winners) > 1:
        next_round_winners = []  # 次のラウンドの勝者を格納する一時リスト
        # 現在のラウンドの全試合を処理
        for i in range(0, len(winners), 2):

            candidate1 = winners[i]
            print(f"candidate : {str(candidate1)}")
            candidate2 = winners[i+1]
            print(f"candidate : {str(candidate2)}")

            ### この2枚の画像をフロントエンドに送信して、ユーザーが選択した画像を勝者として決定する
            image1 = display(candidate1.genome)
            image2 = display(candidate2.genome)

            prompt ="""
# 質問\n
画像内の図形に注目し、左側の画像と右側の画像のどちらかに「ぬもる(numolu)」という名前を付けるならばどちらに名付けますか？\n
「ぬもる(numolu)」と名付ける方をクリックしてください。\n
"""

            ### ここに次のような実装をしたい ###
            # ①フロントエンドに2枚の画像とプロンプトを送信
            # ②ユーザーが選択した画像を勝者(winner)として決定



            next_round_winners.append(winner)

        rounds.append(next_round_winners)  # このラウンドの勝者リストを追加
        winners = next_round_winners  # 次のラウンドの勝者リストを更新

    return rounds  # 各ラウンドの勝者リストを返す



# 各個体にスコアとランクを割り振る関数
def assign_scores(rounds):
    """各個体にスコアとランクを割り振る関数。
    
    Args:
        artists (list): Artistオブジェクトのリスト。
        rounds (list): トーナメントの各ラウンドの勝者のリストのリスト。
    """
    base_score = 1/6  # 基本スコア(準優勝者のスコア。)（優勝者だけボーナス2倍!）
    # 各ラウンドを処理（1回戦から決勝まで）
    for round in rounds:
        score_per_artist = base_score / ( len(round) * 1/2 )  # このラウンドの各個体に割り振るスコア。個体数は2倍あるので、1/2をかける。
        # このラウンドの各勝者にスコアとランクを割り振る
        for artist in round:
            artist.fitness = score_per_artist
            artist.rank = len(round)  # このラウンドの順位を設定



#親の選択(ルーレット選択)
def select_parent(pop):
    fit_sum = 0
    for p in pop:
        fit_sum = fit_sum + p.fitness

    thresh = random.random() * fit_sum
    acc = 0
    for artist in pop:
        acc += artist.fitness
        if acc >= thresh:
            return artist



#交叉処理(二点交叉) 両親のゲノムを受け取って、交叉して返す
def crossover(p1, p2):
    if len(p1) > len(p2):
        p1, p2 = p2, p1
    sp1 = random.randrange(0, len(p1))
    sp2 = random.randrange(sp1, len(p1))
    return p1[:sp1] + p2[sp1:sp2] + p1[sp2:len(p1)]



#突然変異(ランダムにATCGのいずれかに書き換える) 両親のゲノムを受け取って、突然変異して返す
def mutate(agent, m_rate):
    a = list(agent)
    for i in range(len(agent)):
        if random.random() < (m_rate/2):
            a[i] = random.choice('ATCG')
    if random.random() < (m_rate * 2):
        a = [random.choice('ATCG') for i in range(3)] + a  #potential for genome growth
    return ''.join(a)



# ランクが1(優勝), 2(準優勝)の個体をエリートとして取得
def find_elite(generation):
    df = pd.read_csv(rf"results/sample.csv")
    df['rank'] = pd.to_numeric(df['rank'], errors='coerce')
    
    filtered_df = df[df['generation'] == generation]
    top_2 = filtered_df[filtered_df['rank'].isin([1, 2])]
    
    artists = [Artist(id=row['id'], genome=row['genome'], generation=row['generation'], 
                      member=row['member'], fitness=row['fitness'], father=row['father'], mother=row['mother'], rank=row['rank']) 
               for index, row in top_2.iterrows()]
    
    return artists



#現在の個体群の情報を受け取り、新しい世代の個体群を生成する
def newpop(pop, genelength, gen_iteration):
    new_pop = []

    number_ex_elite = len(pop) - 2 # エリートの2個体を除いた数

    # 9割は交叉や突然変異によって新しい個体を生む
    for i in range(number_ex_elite - int(number_ex_elite/10)):
        parent1 = select_parent(pop)
        parent2 = select_parent(pop)
        child = Artist(generation=gen_iteration, member=i + 1, genome=birth(genelength), father = str(parent1), mother = str(parent2))
        child.id = str(child)
        child.genome = crossover(parent1.genome, parent2.genome)
        child.genome = mutate(child.genome, 0.1)
        new_pop.append(child)
    
    # 1割はランダムに新しく生成
    for i in range(int(number_ex_elite/10)):
        new_child = Artist(generation=gen_iteration, member=i + 1 +(number_ex_elite - int(number_ex_elite/10)), genome=birth(genelength))
        new_child.id = str(new_child)
        new_pop.append(new_child)
    
    random.shuffle(new_pop)

    # エリートの2個体はそのまま次の世代へ
    elites = find_elite(gen_iteration - 1)

    elite1 = elites[0]
    elite1.generation = elite1.generation + 1
    elite1.member = 0 # シード権を与えるため(第一シード)
    new_pop.insert(0, elite1)

    elite2 = elites[1]
    elite2.generation = elite2.generation + 1
    elite2.member = 31 # シード権を与えるため(第二シード)
    new_pop.append(elite2)
    
    # 適応度評価
    rounds = tournament(new_pop)
    assign_scores(rounds)
    
    return(new_pop)