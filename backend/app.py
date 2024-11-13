# app.py

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
import os
import csv
from datetime import timedelta
import ga
from models_local import Artist
import logging
import base64
from io import BytesIO
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)  # セッションの有効期限を2時間に設定
Session(app)

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CORS(
    app,
    supports_credentials=True,
    resources={r"/*": {"origins": "http://35.72.8.64"}},
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"]
)

# グローバル設定
POPULATION_SIZE = 32
GENERATIONS = 4
GENE_LENGTH = 30
RESULTS_DIR = 'results'

# 必要なディレクトリを作成
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

# CSVファイルのパスを定義
USERS_CSV_PATH = 'data/users.csv'

# ユーザー認証関数
def authenticate_user(user_id, password):
    with open(USERS_CSV_PATH, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['user_id'] == user_id and row['password'] == password:
                return True
    return False

# ユーザーごとの結果ファイルのパスを取得
def get_results_file(user_id):
    user_dir = os.path.join(RESULTS_DIR, str(user_id))
    os.makedirs(user_dir, exist_ok=True)
    return os.path.join(user_dir, f'{user_id}.csv')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')

    # リクエストデータをログに出力
    logger.info(f"Login attempt with user_id: {user_id}")

    if not user_id or not password:
        return jsonify({'status': 'failure', 'message': 'ユーザーIDとパスワードが必要です。'}), 400

    if not authenticate_user(user_id, password):
        return jsonify({'status': 'failure', 'message': 'ユーザーIDまたはパスワードが正しくありません。'}), 401

    try:
        session.permanent = True
        session['user_id'] = user_id

        logger.info(f"User {user_id} logged in. Session initialized.")
        return jsonify({'status': 'success', 'message': 'ログインに成功しました。'})
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return jsonify({'status': 'failure', 'message': '初期化中にエラーが発生しました。'}), 500

@app.route('/instructions', methods=['GET'])
def instructions():
    instructions_text = "ここに注意事項や説明を記載します。"
    return jsonify({'instructions': instructions_text})

@app.route('/demo', methods=['GET'])
def demo():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'status': 'failure', 'message': 'ログインが必要です。'}), 401

    images = [['/static/images/demo1.png', '/static/images/demo2.png']]
    return jsonify({'images': images})

# Artistオブジェクトを辞書に変換
def artist_to_dict(artist):
    return {
        'id': artist.id,
        'generation': artist.generation,
        'member': artist.member,
        'genome': artist.genome,
        'fitness': artist.fitness,
        'father': artist.father,
        'mother': artist.mother,
        'rank': artist.rank
    }

# 辞書からArtistオブジェクトを生成
def dict_to_artist(data):
    return Artist(
        id=data['id'],
        genome=data['genome'],
        generation=data['generation'],
        member=data['member'],
        fitness=data['fitness'],
        father=data['father'],
        mother=data['mother'],
        rank=data['rank']
    )

# 対戦ペアのデータを準備
def prepare_match_data(candidate1, candidate2):
    # 画像の生成とBase64エンコード
    image1_base64 = generate_image_base64(candidate1)
    image2_base64 = generate_image_base64(candidate2)
    data = {
        'candidate1': {
            'id': candidate1['id'],
            'image_base64': image1_base64
        },
        'candidate2': {
            'id': candidate2['id'],
            'image_base64': image2_base64
        }
    }
    return data

# 画像を生成し、Base64エンコードして返す
def generate_image_base64(candidate_data):
    candidate = dict_to_artist(candidate_data)
    # 画像の生成
    image = ga.display(candidate.genome)
    # 画像をバイト列に変換
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    # Base64エンコード
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    return img_base64

# トーナメントの初期化
def initialize_tournament(pop):
    """トーナメントの初期化"""
    current_round = [artist_to_dict(a) for a in pop]
    tournament_state = {
        'rounds': [current_round],  # 各ラウンドの勝者を保持
        'current_round_index': 0,
        'match_index': 0,
        'winners': []
    }
    return tournament_state

# ユーザーの選択を処理し、トーナメントを進行させる
def process_user_choice(tournament_state, selected_candidate_id):
    current_round = tournament_state['rounds'][tournament_state['current_round_index']]
    match_index = tournament_state['match_index']
    candidate1 = current_round[match_index]
    candidate2 = current_round[match_index + 1]

    # 勝者を決定
    if candidate1['id'] == selected_candidate_id:
        winner = candidate1
    elif candidate2['id'] == selected_candidate_id:
        winner = candidate2
    else:
        # 不正な選択
        raise ValueError("Invalid candidate selected")

    tournament_state['winners'].append(winner)
    tournament_state['match_index'] += 2  # 次の試合へ

    # ラウンドの終了チェック
    if tournament_state['match_index'] >= len(current_round):
        # 次のラウンドへ
        if len(tournament_state['winners']) == 1:
            # トーナメント終了
            tournament_state['rounds'].append(tournament_state['winners'])
            tournament_state['winners'] = []
            tournament_state['current_round_index'] += 1
            tournament_state['match_index'] = 0
            return tournament_state, True  # トーナメント終了
        else:
            tournament_state['rounds'].append(tournament_state['winners'])
            tournament_state['current_round_index'] += 1
            tournament_state['match_index'] = 0
            tournament_state['winners'] = []

    return tournament_state, False

# 適応度とランクを割り振る関数
def assign_scores(rounds):
    base_score = 1 / 6
    for round in rounds:
        rank = len(round)
        score_per_artist = base_score / (len(round) * 0.5)
        for artist_data in round:
            artist_data['fitness'] = score_per_artist
            artist_data['rank'] = rank

@app.route('/experiment/start', methods=['POST'])
def start_experiment():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'status': 'failure', 'message': 'ログインが必要です。'}), 401

    # ユーザーの結果ファイルを取得
    results_file_path = get_results_file(user_id)

    # 結果ファイルが存在し、データがある場合は再開
    if os.path.exists(results_file_path):
        try:
            df = pd.read_csv(results_file_path)
            if not df.empty:
                max_generation = df['generation'].max()
                # 最新の世代の個体群を取得
                latest_population_data = df[df['generation'] == max_generation]
                # 個体群を再構築
                latest_population = []
                for _, row in latest_population_data.iterrows():
                    artist = Artist(
                        id=row['id'],
                        genome=row['genome'],
                        generation=row['generation'],
                        member=row['member'],
                        fitness=row['fitness'],
                        father=row['father'],
                        mother=row['mother'],
                        rank=row['rank']
                    )
                    latest_population.append(artist)

                # 世代数を前回の最大値に+1して設定
                max_generation = max_generation + 1
                session['generation'] = max_generation
                logger.info(f"Resuming experiment for user {user_id} from generation {max_generation}.")

                # 前世代の個体から新しい個体群を生成
                new_population = ga.newpop(latest_population, GENE_LENGTH, max_generation)

                # トーナメントの初期化
                tournament_state = initialize_tournament(new_population)
                session['tournament_state'] = tournament_state

                # # 世代数を前回の最大値に+1して設定
                # session['generation'] = max_generation + 1
                # logger.info(f"Resuming experiment for user {user_id} from generation {max_generation + 1}.")
            else:
                # データがない場合は新規開始
                raise FileNotFoundError
        except Exception as e:
            logger.error(f"Error reading CSV file for user {user_id}: {str(e)}")
            # 新規実験を開始
            pop = ga.firstpop(POPULATION_SIZE, GENE_LENGTH)
            tournament_state = initialize_tournament(pop)
            session['tournament_state'] = tournament_state
            session['generation'] = 0
            logger.info(f"Starting new experiment for user {user_id}.")
    else:
        # 結果ファイルが存在しない場合は新規開始
        pop = ga.firstpop(POPULATION_SIZE, GENE_LENGTH)
        tournament_state = initialize_tournament(pop)
        session['tournament_state'] = tournament_state
        session['generation'] = 0
        logger.info(f"Starting new experiment for user {user_id}.")

    # 最初の対戦ペアを取得
    current_round = tournament_state['rounds'][tournament_state['current_round_index']]
    match_index = tournament_state['match_index']
    candidate1 = current_round[match_index]
    candidate2 = current_round[match_index + 1]
    data = prepare_match_data(candidate1, candidate2)
    return jsonify(data)

@app.route('/experiment/choose', methods=['POST'])
def choose_candidate():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'status': 'failure', 'message': 'ログインが必要です。'}), 401

    data = request.get_json()
    selected_candidate_id = data.get('selected_candidate_id')

    # トーナメントの状態を取得
    tournament_state = session.get('tournament_state')
    if not tournament_state:
        return jsonify({'status': 'failure', 'message': 'トーナメントが開始されていません。'}), 400

    try:
        # ユーザーの選択を処理
        tournament_state, is_finished = process_user_choice(tournament_state, selected_candidate_id)
        # トーナメントの状態を更新
        session['tournament_state'] = tournament_state

        if is_finished:
            # トーナメント終了時の処理
            assign_scores(tournament_state['rounds'])

            # 個体群の結果をCSVファイルに保存
            population_data = tournament_state['rounds'][0]
            results_file_path = get_results_file(user_id)
            for p_data in population_data:
                pop_list = [p_data['id'], p_data['generation'], p_data['member'], p_data['genome'],
                            p_data['fitness'], p_data['father'], p_data['mother'], p_data['rank']]
                ga.write_to_csv(results_file_path, pop_list)

            # # 現在の世代数を取得
            # generation = session.get('generation', 0)

            # 世代数を更新
            generation = session.get('generation', 0) + 1
            session['generation'] = generation

            # 世代数が最大値に達したか確認
            if generation > GENERATIONS:
                return jsonify({'status': 'experiment_finished', 'message': '全ての世代が終了しました。'})
            else:
                # 新しい個体群を生成
                prev_population = [dict_to_artist(p_data) for p_data in population_data]
                new_population = ga.newpop(prev_population, GENE_LENGTH, generation)

                # トーナメントの初期化
                tournament_state = initialize_tournament(new_population)
                session['tournament_state'] = tournament_state

                # # 世代数を更新
                # session['generation'] = generation + 1

                # 最初の対戦ペアを取得
                current_round = tournament_state['rounds'][tournament_state['current_round_index']]
                match_index = tournament_state['match_index']
                candidate1 = current_round[match_index]
                candidate2 = current_round[match_index + 1]
                data = prepare_match_data(candidate1, candidate2)
                return jsonify(data)
        else:
            # 次の対戦ペアを取得
            current_round = tournament_state['rounds'][tournament_state['current_round_index']]
            match_index = tournament_state['match_index']
            candidate1 = current_round[match_index]
            candidate2 = current_round[match_index + 1]
            data = prepare_match_data(candidate1, candidate2)
            return jsonify(data)
    except ValueError as e:
        return jsonify({'status': 'failure', 'message': str(e)}), 400
    

@app.route('/result', methods=['GET'])
def result():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'status': 'failure', 'message': 'ログインが必要です。'}), 401

    # ユーザーの結果ファイルを取得
    results_file_path = get_results_file(user_id)

    if os.path.exists(results_file_path):
        # 結果データを読み込む（必要に応じて）
        # 今回は簡単のため、メッセージのみ返す
        return jsonify({'status': 'success', 'message': '実験が終了しました。ご協力ありがとうございました。'})
    else:
        return jsonify({'status': 'failure', 'message': '結果データが見つかりません。'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

