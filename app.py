# このコードは日経ソフトウェア2024年5月号のP11のサンプルコードをベースとする
import os
from dotenv import load_dotenv
import openai
from flask import Flask, render_template, request
from search import *

# .envファイルのパス
# strip()メソッドは、文字列から空白や改行を削除する
env_path = os.path.expanduser("~/prog/chatgpt001/.env")
load_dotenv(env_path)

# os.environから、keyが"OPEN_API_KEY"のものを取得
openai.api_key = os.getenv("OPENAI_API_KEY")

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
