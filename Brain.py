from datetime import datetime
import Ears
import Mouth
import os
import subprocess as sp
import requests
import wikipedia
from decouple import config
import webbrowser
import wolframalpha

paths = {
    'chrome': "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Chrome.lnk",
    'zoom': "C:\\Users\\jomej\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Zoom\\Zoom.lnk",
    'calculator': "C:\\Windows\\System32\\calc.exe"
}

tongue = Mouth.Mouth()

BOTNAME = config("BOTNAME")
NEWS_API_KEY = config("NEWS_API_KEY")
OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID")
appId = config("APPID")

wolframClient = wolframalpha.Client(appId)


def open_chrome():
    os.startfile(paths['chrome'])


def open_zoom():
    os.startfile(paths['zoom'])


def open_cmd():
    os.system('start cmd')


def open_calculator():
    sp.Popen(paths['calculator'])


def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)


def greet_user():
    """Greets the user according to the time"""

    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        tongue.speak("Good Morning Sir")
    elif (hour >= 12) and (hour < 16):
        tongue.speak("Good afternoon Sir")
    elif (hour >= 16) and (hour < 22):
        tongue.speak("Good Evening Sir")
    else:
        tongue.speak("Its very late Sir")
    tongue.speak("How may I assist you?")


def goodbye_user():

    hour = datetime.now().hour

    if 21 <= hour < 6:
        tongue.speak("Good night sir, take care!")
    else:
        tongue.speak('Have a good day sir!')
    exit()


def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]


def list_or_dict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']


def search_wolframalpha(query=''):
    response = wolframClient.query(query)

    # @success: Wolfram Alpha was able to resolve the query
    # @numpods: Number of results returned
    # pod: List of results. This can also contain subpods
    if response['@success'] == 'false':
        return 'Could not compute'

    # Query resolved
    else:
        result = ''
        # Question
        pod0 = response['pod'][0]
        pod1 = response['pod'][1]
        # May contain the answer, has the highest confidence value
        # if it's primary, or has the title of result or definition, then it's the official result
        if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or (
                'definition' in pod1['@title'].lower()):
            # Get the result
            result = list_or_dict(pod1['subpod'])
            # Remove the bracketed section
            return result.split('(')[0]
        else:
            question = list_or_dict(pod0['subpod'])
            # Remove the bracketed section
            return question.split('(')[0]
            # Search wikipedia instead
            tongue.speak('Computation failed. Querying universal databank.')
            return search_wikipedia(question)


def get_latest_news():
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    result = '\n'.join(map(str, news_headlines[:5]))
    return result


def get_weather_report(city):
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric").json()
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃"


def search_chrome(query):
    search = f'{query}'
    webbrowser.open_new_tab(f"http://www.google.com/search?q={search}")


def search_youtube(query):
    search = f'{query}'
    webbrowser.open_new_tab(f"https://www.youtube.com/results?search_query={search}")


def log(a):
    tongue.speak('Recording your note')
    new_note = a.lower()
    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    with open('note_%s.txt' % now, 'w') as newFile:
        newFile.write(new_note)
        tongue.speak('Note written')
        print('\nNote written\n')
    return 'after closing the application you view your note sir'


def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]


def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']


TMDB_API_KEY = config("TMDB_API_KEY")


def get_trending_movies():
    trending_movies = []
    res = requests.get(
        f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
    results = res["results"]
    for r in results:
        trending_movies.append(r["original_title"])
    result = '\n'.join(map(str, trending_movies[:5]))
    return result


def date():
    now = datetime.now()
    my_date = datetime.today()

    year_name = now.year
    month_name = now.month
    day_name = now.day
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                   'November', 'December']
    ordinalnames = ['1st', '2nd', '3rd', ' 4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th',
                    '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24rd', '25th',
                    '26th', '27th', '28th', '29th', '30th', '31st']

    tongue.speak("Today is " + month_names[month_name - 1] + " " + ordinalnames[day_name - 1] + '.')
    a = "Today is " + str(month_names[month_name - 1]) + " " + str(ordinalnames[day_name - 1]) + ' ' + str(year_name)
    return a


def search_wikipedia(query=''):
    search_results = wikipedia.search(query)
    if not search_results:
        return 'No result received'
    try:
        wiki_page = wikipedia.page(search_results[0])
    except wikipedia.DisambiguationError as error:
        wiki_page = wikipedia.page(error.options[0])
    wiki_summary = wikipedia.summary(query, sentences=2)
    return wiki_page.title + '\n' + wiki_summary
