import re
import string
import random
import numpy as np
from wxpy import *
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
from datetime import datetime, timedelta
import time
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config
from iexfinance.stocks import Stock
from iexfinance.stocks import get_historical_data
from iexfinance.refdata import get_symbols

# create state
GREET = 0
INIT = 1
AUTHED = 2
CHOOSE_COMPANY = 3
CHOOSE_FUNCTION = 4
INPUT_TIME = 5
END = 6

global Company_name
global com_stock
global stock_data
global peer_flag
global state
global pending
global p_state
state = INIT
pending = None
p_state = None

picture_path = './historical_data.png'

# initial wechat robot
bot = Bot(cache_path=True)


keywords = {
            'greet': ['hello', 'hey'],
            'thankyou': ['thank', 'thx'],
            'goodbye': ['bye', 'farewell']
           }


respondses = {'greet':['Hello, {}!',
                       'Nice to meet you, {}!',
                       'Hey, {}, I\'m chat robot'],
              'thankyou':['You are welcome!',
                          'It\'s my pleasure!']
              }

policy_rules = {
    (INIT, "ask_explanation"): (INIT, "I'm a bot to help you search information of stock", None),
    (INIT, "inquire"): (INIT, "You'll have to log in first, what's your phone number?", AUTHED),
    (INIT, "number"): (AUTHED, "Perfect, welcome back!", None),
    (AUTHED, "inquire"): (CHOOSE_COMPANY, "Which company do you want to check?", None),
    (CHOOSE_COMPANY, "specify_company"): (CHOOSE_FUNCTION, "What information do you want to know from the {0}?", None),
    (CHOOSE_FUNCTION, "price"): (CHOOSE_FUNCTION, "Current Stock Price:{0} Anything else?", None),
    (CHOOSE_FUNCTION, "volume"): (CHOOSE_FUNCTION, "The latest Volume:{0} Do you want to know something else?", None),
    (CHOOSE_FUNCTION, "market cap"): (CHOOSE_FUNCTION, "Market Cap:{0}", None),
    (CHOOSE_FUNCTION, "specify_company"): (CHOOSE_FUNCTION, "What information do you want to know from the {0}?", None),
    (CHOOSE_FUNCTION, "history"): (CHOOSE_FUNCTION, "Well, please tell me range of date you want to check", INPUT_TIME),
    (CHOOSE_FUNCTION, "date"): (INPUT_TIME, "OK, wait a sec", None),
    (CHOOSE_FUNCTION, "peers"): (CHOOSE_FUNCTION, "There are some peers of {0}: {1}", None),
    (CHOOSE_FUNCTION, "bye"): (INIT, "GoodBye!", None),
    (INPUT_TIME, "history"): (CHOOSE_FUNCTION, "Here is the Chart of historical data", None),
}

# create a Trainer
trainer = Trainer(config.load("config_spacy.yml"))

# load the training data
training_data = load_data("ChatBot_train.json")

# Create an interpreter by training the model
interpreter = trainer.train(training_data)


patterns = {}

# Iterate over the keywords dictionary
for intent, keys in keywords.items():
    # Create regular expressions and compile them into pattern objects
    patterns[intent] = re.compile('|'.join(keys))


def match_intent(message):
    matched_intent = None
    for intent, pattern in patterns.items():
        # Check if the pattern occurs in the message
        if pattern.findall(message):
            matched_intent = intent
    return matched_intent

stock_token = 'sk_8fb388f4a81c4180b9840201cd65df22'

def find_name(message):
    name = None
    name_keyword = re.compile(r"\b(name|call)\b")
    name_pattern = re.compile(r"\b[A-Z]{1}[a-z]*\b")
    if name_keyword.search(message):
        name_words = name_pattern.findall(message)
        if len(name_words) > 0:
            name = ' '.join(name_words)
    return name

def respond(message):
    name = find_name(message)
    if name is None:
        return "Hi I'm chat robot!"
    else:
        return random.choice(respondses['greet']).format(name)

def interpret(message):
    global Company_name
    global com_stock
    global stock_data
    global peer_flag
    peer_flag = False
    msg = message.lower()
    if any([d in msg for d in string.digits]):
        date_keyword = re.compile(r"\b[0-9]{4}\s[0-9]*\s[0-9]*\b")
        date_string = date_keyword.findall(message)
        if len(date_string) > 0:
            start_date = datetime.strptime(date_string[0], "%Y %m %d")
            end_date = datetime.strptime(date_string[1], "%Y %m %d")
            historical_data = get_historical_data(Company_name, start_date, end_date, output_format='pandas', token = 'sk_8fb388f4a81c4180b9840201cd65df22')
            historical_data['close'].plot()
            plt.savefig('historical_data')
            return "date", None
    if msg.isdigit():
        return "number", None
    mat_intent = match_intent(message)
    if mat_intent == "greet":
        return "greet", None
    if mat_intent == "thankyou":
        return "thankyou", None

    data = interpreter.parse(message)
    intent = data["intent"]["name"]
    entities = data["entities"]
    if intent == 'stock_search':
        return "inquire", None

    if intent == "company_search":
        for ent in entities:
            Company_name = ent["value"]
        com_stock = Stock(Company_name, token = stock_token)
        stock_data = com_stock.get_quote()
        return "specify_company", stock_data['symbol']
    if intent == "explanation":
        return "ask_explanation", None
    if intent == "information_search":
        for ent in entities:
            if str(ent["value"]) == "price":
                return "price", stock_data['latestPrice']
            if str(ent["value"]) == "volume":
                return "volume", stock_data['latestVolume']
            if str(ent["value"]) == "market cap":
                return "market cap", stock_data['marketCap']
            if str(ent["value"]) == "historical data":
                return "history", None
            if str(ent["value"]) == "peers":
                peer_flag = True
                return "peers", ", ".join(com_stock.get_relevant_stocks()['symbols'])
    if intent == "goodbye":
        return "bye", None


@bot.register()
def send_message(msg):
    global Company_name
    global peer_flag
    global state
    global pending
    global p_state
    second_state, information = interpret(msg.text)
    if second_state == 'greet':
        msg.reply(respond(msg.text))
    else:
        if second_state == 'thankyou':
            msg.reply(random.choice(respondses['thankyou']))
        else:
            state, response, pending_state = policy_rules[(state, second_state)]
            if information is None:
                msg.reply(response)
                if (second_state == 'date'):
                    msg.reply_image(picture_path)
            else:
                if peer_flag == True:
                    msg.reply(response.format(Company_name, information))
                else:
                    msg.reply(response.format(information))
            if pending is not None:
                if p_state == state:
                    state, response, pending_state = policy_rules[pending]
                    msg.reply(response)
            if pending_state is not None:
                pending = (pending_state, second_state)
            p_state = pending_state

embed()


