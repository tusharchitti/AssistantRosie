import json
import urllib.request
import datetime
import time
import pyttsx
import calendar
import feedparser

def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time

#build URL for API request
def url_builder(city_id):
	owm_api_key = '8e5a2130cd0ad59337fd79a2ab1db574'
	unit = 'imperial'
	api = 'http://api.openweathermap.org/data/2.5/weather?id='

	full_api_url = api + str(city_id) + '&mode=json&units=' + unit + '&APPID=' + owm_api_key
	return full_api_url

#API request
def data_fetch(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    return raw_api_dict

#labels all data from JSON object
def data_organizer(raw_api_dict):
    data = dict(
        city=raw_api_dict.get('name'),
        country=raw_api_dict.get('sys').get('country'),
        temp=raw_api_dict.get('main').get('temp'),
        temp_max=raw_api_dict.get('main').get('temp_max'),
        temp_min=raw_api_dict.get('main').get('temp_min'),
        humidity=raw_api_dict.get('main').get('humidity'),
        pressure=raw_api_dict.get('main').get('pressure'),
        sky=raw_api_dict['weather'][0]['main'],
        sunrise=time_converter(raw_api_dict.get('sys').get('sunrise')),
        sunset=time_converter(raw_api_dict.get('sys').get('sunset')),
        wind=raw_api_dict.get('wind').get('speed'),
        wind_deg=raw_api_dict.get('deg'),
        dt=time_converter(raw_api_dict.get('dt')),
        cloudiness=raw_api_dict.get('clouds').get('all')
    )
    return data

#print data to command line
def data_output(data):
    m_symbol = '\xb0' + 'C'
    print('---------------------------------------')
    print('Current weather in: {}, {}:'.format(data['city'], data['country']))
    print(data['temp'], m_symbol, data['sky'])
    print('Max: {}, Min: {}'.format(data['temp_max'], data['temp_min']))
    print('')
    print('Wind Speed: {}, Degree: {}'.format(data['wind'], data['wind_deg']))
    print('Humidity: {}'.format(data['humidity']))
    print('Cloud: {}'.format(data['cloudiness']))
    print('Pressure: {}'.format(data['pressure']))
    print('Sunrise at: {}'.format(data['sunrise']))
    print('Sunset at: {}'.format(data['sunset']))
    print('')
    print('Last update from the server: {}'.format(data['dt']))
    print('---------------------------------------')

city_id = input('Enter city ID: ')
weather_data = data_organizer(data_fetch(url_builder(city_id)))
data_output(weather_data)

#concat today's  date into a handy lil string
my_date = str(datetime.date.today().strftime("%A") + ', ' + datetime.date.today().strftime("%B") + ' ' + datetime.date.today().strftime("%d"))

#grab top 5 headlines from NBC NY rss feed
url1 = "http://www.nbcboston.com/news/top-stories/?rss=y&embedThumb=y&summary=y"
[print (i.title) for i in feedparser.parse(url1).entries[:5]]


engine = pyttsx.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

engine.say('Good morning hoozayfa')
engine.say('Today is ')
engine.say(my_date)

engine.say('Current weather in: {}, {}:'.format(weather_data['city'], weather_data['country']))
engine.say('It is currently {} degrees, with {}'.format(int(round(weather_data['temp'], 0)), weather_data['sky']))

engine.say('Top headlines for today from NBC Boston: ')
for i in feedparser.parse(url1).entries[:5]:
	engine.say(i.title)

engine.runAndWait()