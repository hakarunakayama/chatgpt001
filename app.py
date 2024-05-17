# このコードは日経ソフトウェア2024年5月号のP11のサンプルコードをベースとする
import os
from dotenv import load_dotenv
import openai
from flask import Flask, render_template, request
from search import *

# .envファイルのパス
# env_path = "/home/ubuntu/prog/chatgpt001/.env"
# 以下は開発用のローカル環境のディレクトリ（2024/5/17:os.pathモジュールを使ってカレントディレクトリを取得)
cur_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(cur_dir, '.env')
with open(env_path, "r") as file:
    for line in file:
        if line.strip() and not line.strip().startswith("#"):
            key, value = line.strip().split("=", 1)
            os.environ[key] = value

# os.environから、keyが"OPEN_API_KEY"のものを取得
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)
conversation_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    input_text = ""
    if request.method == 'POST':
        input_text = request.form['input_text']
        conversation_history.append({"role": "user", "content": input_text})
        answer = answer_question(input_text, conversation_history)
    return render_template('index.html', result=answer, input=input_text)

if __name__ == '__main__':
    app.run(debug=True)
