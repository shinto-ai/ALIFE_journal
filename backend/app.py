from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
import os
import csv
import uuid
from datetime import timedelta
import ga
from models_local import Artist
import logging
import base64
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)  # 2時間でセッションの有効期限を設定
Session(app)

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CORS(
    app,
    supports_credentials=True,
    resources={r"/*": {"origins": "http://localhost:3000"}},
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"]
)

# グローバル設定
POPULATION_SIZE = 32
GENERATIONS = 30
GENE_LENGTH = 30
RESULTS_DIR = 'results'
RESULTS_FILE = os.path.join(RESULTS_DIR, 'sample.csv')

if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

# CSVファイルが存在しない場合はヘッダーを書き込む
if not os.path.isfile(RESULTS_FILE):
    with open(RESULTS_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "generation", "member", "genome", "fitness", "father", "mother", "rank"])
        writer.writeheader()

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
    prompt = 'デモ：どちらの画像が好みですか？'
    return jsonify({'images': images, 'prompt': prompt})

# Artistオブジェクトを辞書に変換
def artist_to_dict(artist):
    return {
        'id': artist.id,
        'genome': artist.genome,
        'generation': artist.generation,
        'member': artist.member,
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
    prompt = """
画像内の図形に注目し、左側の画像と右側の画像のどちらかに「ぬもる(numolu)」という名前を付けるならばどちらに名付けますか？
「ぬもる(numolu)」と名付ける方をクリックしてください。
"""
    data = {
        'candidate1': {
            'id': candidate1['id'],
            'image_base64': image1_base64
        },
        'candidate2': {
            'id': candidate2['id'],
            'image_base64': image2_base64
        },
        'prompt': prompt
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

    # 初期集団の生成
    pop = ga.firstpop(POPULATION_SIZE, GENE_LENGTH)
    # トーナメントの初期化
    tournament_state = initialize_tournament(pop)
    # トーナメントの状態をセッションに保存
    session['tournament_state'] = tournament_state
    # 世代数をセッションに保存
    session['generation'] = 0

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
            for p_data in population_data:
                pop_list = [p_data['id'], p_data['generation'], p_data['member'], p_data['genome'],
                            p_data['fitness'], p_data['father'], p_data['mother'], p_data['rank']]
                ga.write_to_csv(RESULTS_FILE, pop_list)

            # 世代数を更新
            generation = session.get('generation', 0) + 1
            session['generation'] = generation

            # 世代数が最大値に達したか確認
            if generation >= GENERATIONS:
                return jsonify({'status': 'experiment_finished', 'message': '全ての世代が終了しました。'})
            else:
                # 新しい個体群を生成
                prev_population = [dict_to_artist(p_data) for p_data in population_data]
                new_population = ga.newpop(prev_population, GENE_LENGTH, generation)

                # トーナメントの初期化
                tournament_state = initialize_tournament(new_population)
                session['tournament_state'] = tournament_state

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

if __name__ == '__main__':
    app.run(debug=True)
