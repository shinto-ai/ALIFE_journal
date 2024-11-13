# ga.py

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
    data_dict = list_to_dict(data_list)
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "generation", "member", "genome", "fitness", "father", "mother", "rank"])
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(data_dict)

# グローバル定数を定義
POPULATION_SIZE = 32
GENE_LENGTH = 30
GENERATIONS = 30

def birth(genelength):
    return ''.join(random.choice('ACGT') for _ in range(genelength))

def assign_id(generation, member):
    return "g{0}_m{1}".format(generation, member)

def firstpop(popsize, genelength):
    first_pop = []
    for i in range(popsize):
        genome = birth(genelength)
        artist = Artist(generation=0, member=i, genome=genome)
        # artist.id = str(uuid.uuid4())
        artist.id = assign_id(artist.generation, artist.member)
        artist.fitness = 0.0
        artist.rank = None
        first_pop.append(artist)
    return first_pop

def normalized(a, axis=-1, order=np.inf):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)

def display(agent_genome, size=(200, 200)):
    random.seed(agent_genome)
    np.random.seed(sum([ord(x) for x in agent_genome]))
    pixels = image.read_gene(agent_genome, 0, 1, size)
    outnorm = normalized(pixels) * 255
    im = Image.fromarray(np.uint8(outnorm))
    return im

def select_parent(pop):
    fit_sum = sum(p.fitness for p in pop)
    thresh = random.uniform(0, fit_sum)
    acc = 0
    for artist in pop:
        acc += artist.fitness
        if acc >= thresh:
            return artist
    return pop[-1]

def crossover(p1_genome, p2_genome):
    if len(p1_genome) > len(p2_genome):
        p1_genome, p2_genome = p2_genome, p1_genome
    sp1 = random.randrange(0, len(p1_genome))
    sp2 = random.randrange(sp1, len(p1_genome))
    return p1_genome[:sp1] + p2_genome[sp1:sp2] + p1_genome[sp2:]

def mutate(agent_genome, m_rate):
    agent = list(agent_genome)
    for i in range(len(agent)):
        if random.random() < m_rate:
            agent[i] = random.choice('ATCG')
    return ''.join(agent)

def find_elite(population):
    elites = [artist for artist in population if artist.rank in [1, 2]]
    return elites

def newpop(pop, genelength, gen_iteration):
    new_pop = []
    # エリート個体を選択
    elites = find_elite(pop)
    
    # ランク1とランク2のエリート個体を特定
    rank1_elite = None
    rank2_elite = None
    for elite in elites:
        if elite.rank == 1:
            rank1_elite = elite
        elif elite.rank == 2:
            rank2_elite = elite
    
    # 子個体を生成
    number_ex_elite = POPULATION_SIZE - len(elites)
    num_offspring = int(number_ex_elite * 0.9)
    offspring = []
    for i in range(num_offspring):
        parent1 = select_parent(pop)
        parent2 = select_parent(pop)
        child_genome = crossover(parent1.genome, parent2.genome)
        child_genome = mutate(child_genome, m_rate=0.1)
        child = Artist(generation=gen_iteration, member=0, genome=child_genome, father=parent1.id, mother=parent2.id)
        child.id = assign_id(child.generation, child.member)
        # child.id = str(uuid.uuid4())
        child.fitness = 0.0
        child.rank = None
        offspring.append(child)
    
    # ランダム個体を生成
    num_random = number_ex_elite - num_offspring
    random_individuals = []
    for i in range(num_random):
        genome = birth(genelength)
        child = Artist(generation=gen_iteration, member=0, genome=genome)
        child.id = assign_id(child.generation, child.member)
        # child.id = str(uuid.uuid4())
        child.fitness = 0.0
        child.rank = None
        random_individuals.append(child)
    
    # 子個体とランダム個体をまとめてシャッフル
    other_individuals = offspring + random_individuals
    random.shuffle(other_individuals)
    
    # 新しい個体群を再構築
    new_pop = []
    if rank1_elite:
        rank1_elite.generation = gen_iteration
        # rank1_elite.id = assign_id(artist.generation, artist.member)
        # rank1_elite.id = str(uuid.uuid4())
        new_pop.append(rank1_elite)  # 先頭に追加
    new_pop.extend(other_individuals)
    if rank2_elite:
        rank2_elite.generation = gen_iteration
        # rank2_elite.id = assign_id(artist.generation, artist.member)
        # rank2_elite.id = str(uuid.uuid4())
        new_pop.append(rank2_elite)  # 末尾に追加
    
    # メンバー番号を再割り当て
    for idx, artist in enumerate(new_pop):
        artist.member = idx
        if artist.rank != 1 and artist.rank != 2: # エリート個体のID
            # artist.id = str(uuid.uuid4())
            artist.id =assign_id(artist.generation, artist.member)

    return new_pop
