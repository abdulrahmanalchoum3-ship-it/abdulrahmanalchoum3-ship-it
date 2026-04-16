from flask import Flask, render_template, request, Response, stream_with_context
from g4f.client import Client

app = Flask(__name__)
app.secret_key = "abdulrahman_final_2026"
client = Client()

# رابط الدعم الخاص بك
SUPPORT_LINK = "https://www.binance.com/referral/earn-together/refer2earn-usdc/claim?hl=en&ref=GRO_28502_NRJGG"

@app.route('/')
def index():
    return render_template('index.html', support_link=SUPPORT_LINK)

@app.route('/chat_page')
def chat_page():
    return render_template('chat.html')

@app.route('/stocks_page')
def stocks_page():
    return render_template('stocks.html')

# محرك الدردشة الذكي (مع حماية المحتوى)
@app.route('/stream')
def chat_stream():
    user_input = request.args.get('user_input')
    def generate():
        system_prompt = "أنت مساعد ذكي في منصة عبدالرحمن. يمنع منعاً باتاً تقديم أي محتوى جنسي أو غير لائق. التزم بالأدب."
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_input}],
            stream=True
        )
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content: yield content
    return Response(stream_with_context(generate()), mimetype='text/plain')

# محرك الأسهم والعقارات (تم الإصلاح)
@app.route('/stream_stocks')
def stream_stocks():
    target = request.args.get('target')
    def generate():
        system_prompt = "أنت خبير مالي. قدم تحليلاً دقيقاً ومختصراً للسهم أو العقار المطلوب."
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": target}],
            stream=True
        )
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content: yield content
    return Response(stream_with_context(generate()), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
