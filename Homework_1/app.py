from flask import Flask
from flask import render_template
from flask import request
from urllib.parse import quote
from urllib.request import urlopen
import json


app = Flask(__name__)

OPEN_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&APPID={1}"
#PEN_WEATHER_URL_LOCATION = "http://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&units=metric&APPID={2}"
OPEN_WEATHER_KEY = '456c1a3c436150042b033dd0e6261e4a'

OPEN_COVID19_URL = "http://newsapi.org/v2/everything?q={0}&language=en&sortBy=publishedAt&pageSize=5&apiKey={1}"
OPEN_COVID19_KEY = '0f123f4c5b4f45a6b33d7ca370bbaf05'

OPEN_NEWS_URL = "http://newsapi.org/v2/everything?q={0}&language=en&sortBy=publishedAt&apiKey={1}"

@app.route('/index')
@app.route("/")
def home():
    city = request.args.get('city')

    news = request.args.get('news')
    

    if not city:
        city = 'bangkok'
    
    if not news:
        news = 'covid-19'

    
    weather = get_weather(city, OPEN_WEATHER_KEY)
    covid19 = get_covid19(news, OPEN_COVID19_KEY)

    return render_template("home.html", weather=weather, covid19=covid19)

@app.route('/news')
def news():
    news = request.args.get('news')
    if not news:
        news = 'covid-19'

    news = get_searchNews(news, OPEN_COVID19_KEY)

    return render_template('news.html', news=news)

@app.route('/about')
def about():
   return render_template('about.html')

def get_weather(city,API_KEY):
    query = quote(city)     #ทำให้เวลามี space มาก็ไปเติม string ให้ทำให้ url รันได้
    url = OPEN_WEATHER_URL.format(query, API_KEY)      #แทนที่ {0}, {1}
    data = urlopen(url).read()      #ยิง req แล้วจะตอบกลับมาเป็น json
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):

        description = parsed['weather'][0]['description']
        temperature = parsed['main']['temp']
        city = parsed['name']
        country = parsed['sys']['country']
        wind = parsed['wind']['speed']
        pressure = parsed['main']['pressure']
        humidity = parsed['main']['humidity']
        icon = parsed['weather'][0]['icon']

        weather = {'description': description,
                   'temperature': temperature,
                   'city': city,
                   'country': country,
                   'wind' : wind,
                   'pressure' : pressure,
                   'humidity' : humidity,
                   'icon' : icon
                   }
    return weather

def get_covid19(news,API_KEY):
    queryNews = quote(news)
    url = OPEN_COVID19_URL.format(queryNews, OPEN_COVID19_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)

    covid19 = None
    if parsed.get('articles'):
        title = []
        description = []
        url = []
        urlToImage = []
        content = []
        for x in range(0,5):
            title.append(parsed['articles'][x]['title'])
            description.append(parsed['articles'][x]['description'])
            url.append(parsed['articles'][x]['url'])
            urlToImage.append(parsed['articles'][x]['urlToImage'])
            content.append(parsed['articles'][x]['content'])
    
   
 
    covid19 = {'title': title,
                'description' : description,
                'url' : url,
                'urlToImage' : urlToImage,
                'content' : content
    }
    return covid19

def get_searchNews(news, API_KEY):
    queryNews = quote(news)
    url = OPEN_NEWS_URL.format(queryNews, API_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)
    news = parsed.get('articles')
    return news

if __name__ == '__main__':
    app.run(debug=True,use_reloader=True)