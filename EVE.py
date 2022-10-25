import Mouth
import Brain
import Ears
from utlis import opening_text
from random import choice
import requests

mouth = Mouth.Mouth()
activation = 'computer'


def get_response(msg):
    msg = msg.lower().split()
    if msg[0] == activation:
        msg.pop(0)

        # list commands
        if msg[0] == "repeat":
            mouth.speak(choice(opening_text))
            msg.pop(0)  # Remove say
            speech = ' '.join(msg)
            mouth.speak(speech)
            return speech

        elif msg[0] == "log":
            query = ' '.join(msg[1:])
            return Brain.log(query)

        elif msg[0] == "weather":
            ip_address = Brain.find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            mouth.speak(f"Getting weather report for your city {city}")
            weather, temperature, feels_like = Brain.get_weather_report(city)
            mouth.speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
            mouth.speak(f"Also, the weather report talks about {weather}")
            mouth.speak("For your convenience, I am printing it on the screen sir.")
            return f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}"

        elif msg[0] == "news":
            mouth.speak(f"I'm reading out the latest news headlines, sir")
            mouth.speak(Brain.get_latest_news())
            mouth.speak("For your convenience, I am printing it on the screen sir.")
            return Brain.get_latest_news()

        elif msg[0] == "joke":
            mouth.speak(f"Hope you like this one sir")
            joke = Brain.get_random_joke()
            mouth.speak(joke)
            mouth.speak("For your convenience, I am printing it on the screen sir.")
            return joke.replace('. ', '.\n')  # pprint

        elif msg[0] == "ip":
            ip_address = Brain.find_my_ip()
            mouth.speak(
                f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen '
                f'sir.')
            return f'Your IP Address is {ip_address}'

        elif msg[0] == 'date':
            return Brain.date()

        elif msg[0] == "advice":
            mouth.speak(f"Here's an advice for you, sir")
            advice = Brain.get_random_advice()
            mouth.speak(advice)
            mouth.speak("For your convenience, I am printing it on the screen sir.")
            return advice  # pprint

        elif msg[0] == "trending":
            mouth.speak(f"Some of the trending movies are: {Brain.get_trending_movies()}")
            mouth.speak("For your convenience, I am printing it on the screen sir.")
            return Brain.get_trending_movies()

        elif msg[0] == "wikipedia":
            mouth.speak(choice(opening_text))
            msg = ' '.join(msg[1:])
            mouth.speak('Querying the universal databank.')
            mouth.speak(Brain.search_wikipedia(msg))
            mouth.speak("For your convenience, I am printing it on the screen sir.")
            return Brain.search_wikipedia(msg)

        elif msg[0] == "compute":
            mouth.speak(choice(opening_text))
            msg = ' '.join(msg[1:])
            mouth.speak('Computing')
            try:
                result = Brain.search_wolframalpha(msg)
                mouth.speak(result)
                return result
            except Exception:
                mouth.speak('Unable to compute.')

        elif msg[0] == "open":
            msg.pop(0)
            if msg[0] == "chrome":
                mouth.speak(choice(opening_text))
                Brain.open_chrome()

            elif msg[0] == "zoom":
                mouth.speak(choice(opening_text))
                Brain.open_zoom()
                return "opening zoom"

            elif msg[0] == "command":
                mouth.speak(choice(opening_text))
                Brain.open_cmd()
                return "opening command"

            elif msg[0] == "camera":
                mouth.speak(choice(opening_text))
                Brain.open_camera()
                return "opening camera"

            elif msg[0] == "calculator":
                mouth.speak(choice(opening_text))
                Brain.open_calculator()
                return "opening calculator"

            else:
                mouth.speak("The command is unavailable!")

        elif msg[0] == "search":
            msg.pop(0)
            if msg[0] == "youtube":
                mouth.speak(choice(opening_text))
                query = ' '.join(msg[1:])
                Brain.search_youtube(query)
                return f"searching {query} on youtube"

            elif msg[0] == "chrome":
                mouth.speak(choice(opening_text))
                query = ' '.join(msg[1:])
                Brain.search_chrome(query)
                return f"searching {query} on chrome"

        else:
            mouth.speak("The command is unavailable!")

    elif 'quit' in msg:
        Brain.goodbye_user()

    else:
        mouth.speak("The activation code is incorrect!")
