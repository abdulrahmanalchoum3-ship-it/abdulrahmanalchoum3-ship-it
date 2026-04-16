from flask import Flask, render_template, request, Response, stream_with_context
from g4f.client import Client

app = Flask(__name__)
app.secret_key = "abdulrahman_final_v1_2026"
client = Client()

# بيانات المنصة
SUPPORT_LINK = "https://www.binance.com/referral/earn-together/refer2earn-usdc/claim?hl=en&ref=GRO_28502_NRJGG"
CONTACT_EMAIL = "abdulrahman.sory.dev@gmail.com"

@app.route('/')
def index():
    return render_template('index.html', support_link=SUPPORT_LINK, email=CONTACT_EMAIL)

@app.route('/chat_page')
def chat_page():
    return render_template('chat.html')

@app.route('/stocks_page')
def stocks_page():
    return render_template('stocks.html')

@app.route('/stream')
def chat_stream():
    user_input = request.args.get('user_input')
    def generate():
        system_prompt = (
            "أنت المساعد الذكي الرسمي لمنصة المبرمج عبدالرحمن الصانع سوري. "
            "نحن الآن في أبريل 2026. أنت تمتلك أحدث المعلومات العالمية. "
            "أسلوبك راقٍ وذكي مثل Google Gemini. يمنع أي محتوى غير لائق."
        )
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

@app.route('/stream_stocks')
def stream_stocks():
    target = request.args.get('target')
    def generate():
        system_prompt = "أنت خبير مالي متقدم لعام 2026. حلل البيانات بدقة واحترافية."
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
    app.run(debug=True)
