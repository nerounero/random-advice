from flask import Flask, jsonify, request
from openai import OpenAI
from dotenv import load_dotenv
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

# 環境変数をロード
load_dotenv()

app = Flask(__name__)
CORS(app)
limiter = Limiter(get_remote_address, app=app)

# OpenAIのAPIキーを環境変数から取得
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def generate_advice():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # または "gpt-4"
        messages=[
            {"role": "system", "content": "あなたはユニークで奇妙な日本語のアドバイスを生成するアシスタントです。また、「」で囲んでください。意味のある文章ではないです。"},
            {"role": "user", "content": "40文字以内でユニークで奇妙なアドバイスをください。"}
        ],
        max_tokens=60,  # トークン数で40文字以内に収める
        temperature=0.7  # 創造的な応答を得るために設定
    )
    advice = response.choices[0].message.content
    return advice

@app.route('/random-advice', methods=['GET'])
@limiter.limit("5 per minute") 
def get_random_advice():
    try:
        advice = generate_advice()
        return jsonify({"advice": advice})
    except:
        return jsonify({"advice":"制限中です"}), 429

if __name__ == '__main__':
    app.run(debug=True)
