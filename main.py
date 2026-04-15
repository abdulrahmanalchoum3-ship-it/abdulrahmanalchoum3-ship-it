import os
from flask import Flask, render_template, request, Response, stream_with_context, session
from g4f.client import Client

app = Flask(__name__)
app.secret_key = "abdulrahman_pro_2026_key" # مفتاح الذاكرة والخصوصية
client = Client()

# رابط الدعم المباشر الخاص بك
SUPPORT_LINK = "https://www.binance.com/referral/earn-together/refer2earn-usdc/claim?hl=en&ref=GRO_28502_NRJGG"

@app.route('/')
def index():
    return render_template('index.html', support_link=SUPPORT_LINK)

@app.route('/new_chat')
def new_chat():
    session['messages'] = []
    return "success"

@app.route('/stream')
def chat_stream():
    user_input = request.args.get('user_input')
    if 'messages' not in session: session['messages'] = []
    
    # تعليمات البوت الاحترافية
    system_instr = "أنت مساعد ذكي في منصة عبد الرحمن AI. استخدم الإيموجي دائماً 🚀. اكتب الأكواد البرمجية بدقة. أنت خبير أيضاً في تحليل الأسهم والعقارات."
    
    session['messages'].append({"role": "user", "content": user_input})
    messages = [{"role": "system", "content": system_instr}] + session['messages'][-10:]

    def generate():
        try:
            response = client.chat.completions.create(model="gpt-4", messages=messages, stream=True)
            full_res = ""
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    full_res += content
                    yield content
            session['messages'].append({"role": "assistant", "content": full_res})
            session.modified = True
        except Exception:
            yield "⚠️ السيرفر مشغول قليلاً، حاول مجدداً يا بطل!"
    return Response(stream_with_context(generate()), mimetype='text/plain')

@app.route('/stream_stocks')
def stocks_stream():
    target = request.args.get('target')
    prompt = f"حلل سهم أو عقار {target} بعمق. اذكر التوقعات، المخاطر، ونصيحة استثمارية ذكية مع استخدام إيموجيات مالية 📈🏘️."
    def generate():
        response = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}], stream=True)
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content: yield content
    return Response(stream_with_context(generate()), mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
