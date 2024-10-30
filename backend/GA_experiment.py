import random
import numpy as np
from PIL import Image
import pandas as pd
import image as image
from models_local import Artist
import csv
import os

def birth(popsize):
    """指定された長さ（popsize）のランダムな「ACGT」文字列を生成"""
    return ''.join(random.choice('ACGT') for _ in range(popsize))

def firstpop(popsize, genelength):
    """初期集団を生成"""
    population = []
    for i in range(popsize):
        artist = Artist(generation=0, member=i, genome=birth(genelength))
        artist.id = str(artist)  # id を設定
        population.append(artist)
    return population

def normalized(a, axis=-1, order=np.inf):
    """画像のノーマライズ処理"""
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)

def generate_image(genome, size=(200, 200)):
    """遺伝子情報を基に画像を生成"""
    random.seed(genome)
    np.random.seed(sum(ord(x) for x in genome))
    pixels = image.read_gene(genome, 0, 1, size)
    outnorm = normalized(pixels) * 255
    return Image.fromarray(np.uint8(outnorm))

def select_parent(pop):
    """親の選択（ルーレット選択）"""
    fit_sum = sum(p.fitness for p in pop)
    thresh = random.random() * fit_sum
    acc = 0
    for artist in pop:
        acc += artist.fitness
        if acc >= thresh:
            return artist

def crossover(p1, p2):
    """交叉処理（二点交叉）"""
    if len(p1) > len(p2):
        p1, p2 = p2, p1
    sp1 = random.randrange(0, len(p1))
    sp2 = random.randrange(sp1, len(p1))
    return p1[:sp1] + p2[sp1:sp2] + p1[sp2:len(p1)]

def mutate(agent, m_rate):
    """突然変異処理"""
    a = list(agent)
    for i in range(len(agent)):
        if random.random() < (m_rate/2):
            a[i] = random.choice('ATCG')
    if random.random() < (m_rate * 2):
        a = [random.choice('ATCG') for _ in range(3)] + a
    return ''.join(a)

# ga_experiment.py

def tournament(pop):
    """トーナメント戦の構造を生成する関数"""
    import random
    rounds = []
    current_round = pop.copy()
    random.shuffle(current_round)

    while len(current_round) > 1:
        pairs = []
        next_round = []
        for i in range(0, len(current_round), 2):
            if i + 1 < len(current_round):
                pairs.append((current_round[i], current_round[i + 1]))
                next_round.append(None)  # 勝者はまだ決まっていないので仮の値
            else:
                # 奇数の場合、最後の一人は次のラウンドに自動進出
                next_round.append(current_round[i])
        rounds.append(pairs)
        current_round = next_round
    return rounds



def prepare_image_pair(pair, image_dir, user_id, generation):
    """画像ペアを生成し、保存パスを返す"""
    paths = []
    for i, artist in enumerate(pair):
        image = generate_image(artist.genome)
        path = os.path.join(image_dir, f"{user_id}_gen{generation}_img{i+1}.png")
        image.save(path)
        paths.append(path)
    return paths



def process_tournament_round(population, image_dir, user_id, generation):
    """トーナメントの1ラウンドを処理"""
    pairs = list(zip(population[::2], population[1::2]))
    return [prepare_image_pair(pair, image_dir, user_id, generation) for pair in pairs]


# app.pyで使われてないぞ？
def process_user_choices(tournament_structure, user_choices):
    """ユーザーの選択に基づいてトーナメント結果を処理する関数"""
    results = []
    for round_pairs, round_choices in zip(tournament_structure[1:], user_choices):
        round_winners = []
        for (artist1, artist2), choice in zip(round_pairs, round_choices):
            winner = artist1 if choice == 1 else artist2
            round_winners.append(winner)
        results.append(round_winners)
    
    return results

def assign_scores(population):
    """トーナメントの結果に基づいて適応度を割り当てる"""
    # ランクに基づいて適応度を設定
    for artist in population:
        if artist.rank == 1:
            artist.fitness = 1.0  # 優勝者の適応度
        elif artist.rank == 2:
            artist.fitness = 0.8
        elif artist.rank == 3:
            artist.fitness = 0.6
        elif artist.rank == 4:
            artist.fitness = 0.4
        elif artist.rank == 5:
            artist.fitness = 0.2
        else:
            artist.fitness = 0.1  # その他の個体の適応度


def assign_ranks(population, tournament_structure, user_choices):
    """トーナメントの結果に基づいて順位を割り当てる"""
    total_rounds = len(tournament_structure)
    elimination_rounds = {artist.id: total_rounds for artist in population}

    current_round_artists = {artist.id: artist for artist in population}

    for round_number, (round_pairs, choices) in enumerate(zip(tournament_structure, user_choices), start=1):
        next_round_artists = {}
        for (artist1, artist2), choice in zip(round_pairs, choices):
            if choice == 1:
                winner = artist1
                loser = artist2
            elif choice == 2:
                winner = artist2
                loser = artist1
            else:
                continue  # 無効な選択
            next_round_artists[winner.id] = winner
            # 負けた個体の淘汰ラウンドを更新
            elimination_rounds[loser.id] = round_number
        current_round_artists = next_round_artists

    # 各個体に順位を割り当てる
    for artist in population:
        elimination_round = elimination_rounds[artist.id]
        # 順位の割り当て
        if elimination_round == total_rounds:
            artist.rank = 1  # 優勝
        elif elimination_round == total_rounds - 1:
            artist.rank = 2  # 準優勝
        elif elimination_round == total_rounds - 2:
            artist.rank = 3  # ベスト4
        elif elimination_round == total_rounds - 3:
            artist.rank = 4  # ベスト8
        elif elimination_round == total_rounds - 4:
            artist.rank = 5  # ベスト16
        else:
            artist.rank = 6  # ベスト32以降


def find_elite(generation):
    """前世代のエリートを2個体返す"""
    df = pd.read_csv(r"data\sound_symbolism\numolu\subject1.csv")
    df['fitness'] = pd.to_numeric(df['fitness'], errors='coerce')
    
    filtered_df = df[df['generation'] == generation]
    top_2 = filtered_df.sort_values(by='fitness', ascending=False).head(2)
    
    artists = [Artist(id=row['id'], genome=row['genome'], generation=row['generation'], 
                      member=row['member'], fitness=row['fitness'], father=row['father'], mother=row['mother']) 
               for index, row in top_2.iterrows()]
    
    return artists

def newpop(pop, genelength, gen_iteration, user_choices):
    """新しい世代の個体群を生成する"""
    tournament_structure = tournament(pop)
    tournament_results = process_user_choices(tournament_structure, user_choices)
    
    # 順位を割り当てる
    assign_ranks(pop, tournament_structure, user_choices)
    
    # 適応度の割り当て
    assign_scores(tournament_results)
    
    new_pop = []
    elites = tournament_results[-1][:2]  # 決勝ラウンドの上位2個体をエリートとする
    
    elite1, elite2 = elites
    elite1.generation = gen_iteration
    elite1.member = 0  # 第一シード
    elite2.generation = gen_iteration
    elite2.member = len(pop) - 1  # 第二シード
    new_pop.append(elite1)
    
    # 交叉・突然変異による個体の生成（個体数に応じて調整）
    for i in range(1, len(pop) - 3):
        parent1 = select_parent(pop)
        parent2 = select_parent(pop)
        child = Artist(generation=gen_iteration, member=i, genome=birth(genelength), 
                       father=str(parent1), mother=str(parent2))
        child.id = str(child)
        child.genome = crossover(parent1.genome, parent2.genome)
        child.genome = mutate(child.genome, 0.1)
        new_pop.append(child)
    
    # ランダム生成個体の追加（3個体）
    for i in range(len(pop) - 3, len(pop) - 1):
        new_child = Artist(generation=gen_iteration, member=i, genome=birth(genelength))
        new_child.id = str(new_child)
        new_pop.append(new_child)
    
    new_pop.append(elite2)
    
    return new_pop

def save_results(file_path, data):
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["id", "Generation", "Member", "Genome", "Fitness", "Father", "Mother"])
        for artist in data:
            writer.writerow([f"g{artist.generation}_m{artist.member}", artist.generation, artist.member, artist.genome, artist.fitness, artist.father, artist.mother])