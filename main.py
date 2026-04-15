from flask import Flask, render_template, request, Response, stream_with_context
from g4f.client import Client

app = Flask(__name__)
client = Client()

@app.route('/')
def index(): return render_template('index.html')

@app.route('/chat_page')
def chat_page(): return render_template('chat.html')

@app.route('/stocks_page')
def stocks_page(): return render_template('stocks.html')

@app.route('/stream')
def chat_stream():
    user_input = request.args.get('user_input')
    def generate():
        try:
            # هنا بنخلي المكتبة تختار الموديل الشغال حالياً تلقائياً
            response = client.chat.completions.create(
                model="", # تركناه فاضي عشان هو يختار الأسرع
                messages=[{"role": "user", "content": user_input}],
                stream=True,
            )
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content: yield content
        except Exception:
            yield "⚠️ السيرفر يحاول الاتصال.. اضغط إرسال مرة ثانية."
    return Response(stream_with_context(generate()), mimetype='text/plain')

@app.route('/stream_stocks')
def stocks_stream():
    target = request.args.get('target')
    prompt = f"حلل استثمار {target} في الإمارات بالدرهم."
    def generate():
        try:
            response = client.chat.completions.create(
                model="",
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content: yield content
        except Exception:
            yield "⚠️ جاري جلب البيانات المالية.."
    return Response(stream_with_context(generate()), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=5000)