import pandas as pd
import random
import GA_experiment
import image
import perlin_noise_python_numpy as perlin
from models_local import Artist 


# 保存先パラメータの設定
CSV_file_path = r"C:\Users\shint\Downloads\conrad-master\conrad-master\conrad_ALIFE2024\genetic_algorithm_examinee2_numolu.csv"

# 遺伝的アルゴリズムのパラメータ設定
popsize = 32
genelength = 30
gene_iteration = 10000




# # CSVファイルの読み込み
# try:
#     # CSVファイルの読み込みを試みる
#     df = pd.read_csv(CSV_file_path)
#     df_empty = df.empty
# except FileNotFoundError:
#     df_empty = True

# # DataFrameが空でないか確認
# if not df_empty:
  
#     # 最大のgenerationを見つける
#     max_generation = df['generation'].max()
    
#     # 最大generationに属する全ての個体を取得
#     max_gen_individuals = df[df['generation'] == max_generation]
    
#     # 該当する個体をArtistクラスのインスタンスとして取得
#     pop = [Artist(id=row['id'], genome=row['genome'], generation=row['generation'], 
#                       member=row['member'], fitness=row['fitness'], father=row['father'], mother=row['mother']) 
#                for index, row in max_gen_individuals.iterrows()]
    
#     #print(pop)
    
#     artist = random.choice(pop)
    
#     # 親選択・交叉・突然変異を全世代に。
#     for i in range(gene_iteration):
#         generation = i + 1 + artist.generation
#         print(f"##### generation : {generation} #####")
#         pop = GA_experiment.newpop(pop, genelength, generation)

#         # CSVファイルに書き込み
#         for p in pop:
#             pop_list = [str(p), p.generation, p.member, p.genome, p.fitness, p.father, p.mother]
#             GA_experiment.write_to_csv(CSV_file_path, pop_list)
    

# else:

# 初期集団の生成
print(f"##### generation : 0 #####")

pop = GA_experiment.firstpop(popsize, genelength)
rounds = GA_experiment.tournament(pop)
GA_experiment.assign_scores(rounds)

# CSVファイルに書き込み
for p in pop:
    pop_list = [str(p), p.generation, p.member, p.genome, p.fitness, p.father, p.mother]
    GA_experiment.write_to_csv(CSV_file_path, pop_list)


# 親選択・交叉・突然変異を全世代に。
for i in range(gene_iteration):
    generation = i + 1
    print(f"##### generation : {generation} #####")
    pop = GA_experiment.newpop(pop, genelength, generation)

    # CSVファイルに書き込み
    for p in pop:
        pop_list = [str(p), p.generation, p.member, p.genome, p.fitness, p.father, p.mother]
        GA_experiment.write_to_csv(CSV_file_path, pop_list)
