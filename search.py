import os
import pandas as pd
import openai
import numpy as np
from openai.embeddings_utils import distances_from_embeddings

def create_context(question, df, max_len=1800):
    q_embeddings = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']
    df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].apply(eval).apply(np.array).values, distance_metric='cosine')

    returns = []
    cur_len = 0

    for  _, row in df.sort_values('distances', ascending=True).iterrows():
        cur_len += row['n_tokens'] + 4
        if cur_len > max_len:
            break
        returns.append(row["text"])
    
    return "\n\n###\n\n".join(returns)

def answer_question(question, conversation_history):
    # df = pd.read_csv(os.path.expanduser("/home/ubuntu/prog/chatgpt001/embeddings.csv"))
    # 以下は開発用ローカルディレクトリ（2024/5/17:os.pathモジュールを使ってカレントディレクトリを取得)
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(cur_dir, 'embeddings.csv'))
    context = create_context(question, df, max_len=200)

    prompt = f"あなたはPayPayの営業マンです。以下のコンテキストに基づいて、お客様からの質問に対して、効果的な営業施策を提案してください。回答は3行以内で簡潔にまとめ、具体的な数字と例を含めてください。\n\nコンテキスト: {context}\n\n---\n\n質問: {question}\n回答:"
    conversation_history.append({"role": "user", "content": prompt})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            # ここのconversation_historyは、セッションが続くにつれてトークン数が増えていく。
            messages=conversation_history,
            temperature=1,
        )

        return response.choices[0]["message"]["content"].strip()
    except Exception as e:
        print(e)
        return ""

