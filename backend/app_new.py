from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
import os
import csv
import uuid
from datetime import timedelta
import GA_origin as ga
from models_local import Artist
import logging


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2) # 2時間でセッションの有効期限を設定
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
RESULTS_DIR = 'results/sample.csv'

for dir in [RESULTS_DIR]:
    if not os.path.exists(dir):
        os.makedirs(dir)

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


@app.route('/experiment', methods=['GET'])
def get_experiment():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'status': 'failure', 'message': 'ログインが必要です。'}), 401

    # 初期集団の生成
    print(f"##### generation : 0 #####")

    pop = ga.firstpop(POPULATION_SIZE, GENE_LENGTH)

    # 要注目！
    # 次のトーナメントで、勝者の決定方法はフロントエンド側でのユーザーの選択によるものに変更する必要がある。

    rounds = ga.tournament(pop)
    ga.assign_scores(rounds)

    # CSVファイルに書き込み
    for p in pop:
        pop_list = [str(p), p.generation, p.member, p.genome, p.fitness, p.father, p.mother, p.rank]
        ga.write_to_csv(RESULTS_DIR, pop_list)


    # 親選択・交叉・突然変異を全世代に。
    for i in range(GENERATIONS):
        generation = i + 1
        print(f"##### generation : {generation} #####")
        pop = ga.newpop(pop, GENE_LENGTH, generation)

        # CSVファイルに書き込み
        for p in pop:
            pop_list = [str(p), p.generation, p.member, p.genome, p.fitness, p.father, p.mother, p.rank]
            ga.write_to_csv(RESULTS_DIR, pop_list)


if __name__ == '__main__':
    app.run(debug=True)