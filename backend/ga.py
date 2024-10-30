import random
import uuid
import PIL
from PIL import Image
import numpy as np
import pandas as pd
import csv
import os
from models_local import Artist
import image

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

# 指定された長さ（genelength）のランダムな「ACGT」文字列を生成
def birth(genelength):
    return ''.join(random.choice('ACGT') for _ in range(genelength))

# popsizeに基づいて新しい個体群を生成
def firstpop(popsize, genelength):
    first_pop = []
    for i in range(popsize):
        genome = birth(genelength)
        artist = Artist(generation=0, member=i, genome=genome)
        artist.id = str(uuid.uuid4())
        artist.fitness = 0.0  # 初期適応度
        artist.rank = None    # 初期ランク
        first_pop.append(artist)
    return first_pop

# 正規化関数
def normalized(a, axis=-1, order=np.inf):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)

# 遺伝子情報を基に画像を生成する関数
def display(agent, size=(200, 200)):
    """遺伝子情報を表す文字列を基に画像を生成"""
    # agent(ゲノム文字列)をもとにシード値を生成(再現性確保のため)
    random.seed(agent)
    np.random.seed(sum([ord(x) for x in agent]))  # agentの各文字のASCII値の合計

    # ゲノム文字列を基にしたピクセルデータをimage.read_geneを使って取得
    pixels = image.read_gene(agent, 0, 1, size)
    outnorm = normalized(pixels) * 255
    im = Image.fromarray(np.uint8(outnorm))
    return im



# 親の選択(ルーレット選択)
def select_parent(pop):
    fit_sum = sum(p.fitness for p in pop)
    thresh = random.uniform(0, fit_sum)
    acc = 0
    for artist in pop:
        acc += artist.fitness
        if acc >= thresh:
            return artist
    # 万が一閾値を超えない場合は最後の個体を返す
    return pop[-1]

# 交叉処理(二点交叉)
def crossover(p1_genome, p2_genome):
    if len(p1_genome) > len(p2_genome):
        p1_genome, p2_genome = p2_genome, p1_genome
    sp1 = random.randrange(0, len(p1_genome))
    sp2 = random.randrange(sp1, len(p1_genome))
    return p1_genome[:sp1] + p2_genome[sp1:sp2] + p1_genome[sp2:]

# 突然変異(ランダムにATCGのいずれかに書き換える)
def mutate(agent_genome, m_rate):
    agent = list(agent_genome)
    for i in range(len(agent)):
        if random.random() < m_rate:
            agent[i] = random.choice('ATCG')
    return ''.join(agent)

# ランクが1(優勝), 2(準優勝)の個体をエリートとして取得
def find_elite(population):
    elites = [artist for artist in population if artist.rank in [1, 2]]
    return elites

# 現在の個体群の情報を受け取り、新しい世代の個体群を生成する
def newpop(pop, genelength, gen_iteration):
    new_pop = []
    # エリート個体を選択
    elites = find_elite(pop)
    number_ex_elite = len(pop) - len(elites)  # エリート個体を除いた数

    # 90% は交叉・突然変異によって新しい個体を生成
    num_offspring = int(number_ex_elite * 0.9)
    for i in range(num_offspring):
        parent1 = select_parent(pop)
        parent2 = select_parent(pop)
        child_genome = crossover(parent1.genome, parent2.genome)
        child_genome = mutate(child_genome, m_rate=0.1)
        child = Artist(generation=gen_iteration, member=i, genome=child_genome, father=parent1.id, mother=parent2.id)
        child.id = str(uuid.uuid4())
        child.fitness = 0.0  # 初期適応度
        child.rank = None    # 初期ランク
        new_pop.append(child)

    # 残りの10%はランダムに新しい個体を生成
    num_random = number_ex_elite - num_offspring
    for i in range(num_random):
        genome = birth(genelength)
        child = Artist(generation=gen_iteration, member=i + num_offspring, genome=genome)
        child.id = str(uuid.uuid4())
        child.fitness = 0.0  # 初期適応度
        child.rank = None    # 初期ランク
        new_pop.append(child)

    # エリート個体を新しい世代に引き継ぐ
    for elite in elites:
        elite.generation = gen_iteration
        elite.member = len(new_pop)
        elite.id = str(uuid.uuid4())
        new_pop.append(elite)

    # メンバー番号を再割り当て
    for idx, artist in enumerate(new_pop):
        artist.member = idx
        artist.id = str(uuid.uuid4())

    return new_pop

# 不要になった関数はコメントアウトまたは削除
# tournament関数とassign_scores関数はapp.pyで処理されるため削除

# 追加で必要な関数や処理があればここに記述

