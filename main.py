import os
from flask import Flask, render_template, request, Response, stream_with_context, session
from g4f.client import Client

app = Flask(__name__)
app.secret_key = "abdulrahman_syrian_hero_2026"
client = Client()

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

@app.route('/new_chat')
def new_chat():
    session['messages'] = []
    return "success"

@app.route('/stream')
def chat_stream():
    user_input = request.args.get('user_input')
    if 'messages' not in session: session['messages'] = []
    
    system_instr = "أنت مساعد ذكي في منصة عبد الرحمن AI. استخدم الإيموجي 🚀. أنت فخر الصناعة السورية 🇸🇾. إذا طلب المستخدم صورة أو فيديو، ساعده بالوصف."
    session['messages'].append({"role": "user", "content": user_input})
    messages = [{"role": "system", "content": system_instr}] + session['messages'][-10:]

    def generate():
        response = client.chat.completions.create(model="gpt-4", messages=messages, stream=True)
        full_res = ""
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                full_res += content
                yield content
        session['messages'].append({"role": "assistant", "content": full_res})
        session.modified = True
    return Response(stream_with_context(generate()), mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
