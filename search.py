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
    df = pd.read_csv(os.path.expanduser("/home/ubuntu/prog/chatgpt001/embeddings.csv"))
    context = create_context(question, df, max_len=200)

    prompt = f"あなたはpaypayの営業マンです。コンテキストに基づいて、お客様からの質問に対して、効果的な営業施策を提案してください。その際、なるべくクーポン適用期間や決済金額、還元額について説明してください。その際は具体的な数字を必ず例として挙げてください。その際に例として挙げる数字は、コンテキストに基づいたものにしてください。\n\nコンテキスト: {context}\n\n---\n\n質問: {question}\n回答:"
    conversation_history.append({"role": "user", "content": prompt})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            temperature=1,
        )

        return response.choices[0]["message"]["content"].strip()
    except Exception as e:
        print(e)
        return ""

