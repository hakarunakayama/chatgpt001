# このコードは日経ソフトウェア2024年5月号のP11のサンプルコードをベースとする
import os
import openai
from flask import Flask, render_template, request
from search import *

# .envファイルのパス
# strip()メソッドは、文字列から空白や改行を削除する
env_path = ".env"
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
