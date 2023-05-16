import telebot
# from PIL import Image
# import qrcode
import json
import datetime
# import cv2 
from telebot import types 
import openai
import requests
user_data_array = []
from aiogram.types import ChatActions
import pickle

with open('key.json', 'rb') as file:
    key = pickle.load(file)
openai.api_key = key
image = False

print('Starting a bot....')

#? 1 way to get the users from model Users
# def get_users_info(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         users = json.loads(response.text)
#         return users

# users = get_users_info('http://127.0.0.1:8000/api/users/?format=json')


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).get("choices")[0].get("text")
    return response


with open('token.json', 'rb') as file:
     token = pickle.load(file)
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Instagram', url='https://www.instagram.com/_1nurbek/')
    button2 = types.InlineKeyboardButton('Github', url='https://github.com/bugsssssss')
    markup.add(button1, button2)
    bot.send_message(message.chat.id, f"What is ChatGPT? \nChatGPT is a large language model created by OpenAI that uses deep learning algorithms to understand and generate human-like text. It can be used for a variety of natural language processing tasks, such as language translation, question answering, and text summarization, among others.")
    bot.send_message(message.chat.id, 'Find me on: ', reply_markup=markup)
    bot.send_message(message.chat.id, 'Let\'s start, try to type something... or if you want to create an image based on your message you can use <b>/create</b> command:', parse_mode='HTML')
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # white = types.KeyboardButton('create')



@bot.message_handler(commands=['create'])
def get(message):
    global image_data, image
    image = True
    print(message.chat.id)
    bot.send_message(message.chat.id, 'Okay cool, it\'s almost done, describe what it should look like: ')

    print(message.chat.id)
@bot.message_handler(content_types=['text'])
def start(message):
    global user_data_array, image
    if image == False:
        # try:
        # bot.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        print(message.chat.id)

        # bot.send_message(message.chat.id, '...')

        ai_response = generate_response(message.text + '.')
        user_data = {
            'type': 'text',
            'user': message.from_user.first_name,
            'prompt': message.text,
            'response': ai_response,
            'time': datetime.datetime.today().strftime('%D %H:%M:%S'),

        }
        bot.send_message(message.chat.id, ai_response)
        bot.send_message(657061394, f'''type: text,
user: {message.from_user.first_name}
prompt: {message.text}
response: {ai_response}
time: {datetime.datetime.today().strftime('%D %H:%M:%S')}''')

        # user = Users(id=message.chat.id, username=message.from_user.first_name, usertext=message.text)
        # user.save()
        # except ConnectionError:
        #     bot.send_message(message.chat.id, 'I\'m afraid somewthing went wrong. Please try again later.')
    else:
        print('Processing...')
        bot.send_message(message.chat.id, 'Processing, please wait...')
        image = False
        response = openai.Image.create(
        prompt=message.text,
        n=1,
        size="512x512"
        )
        image_url = response['data'][0]['url']
        r = requests.get(image_url, stream=True)
        if r.status_code == 200:
            with open('generated_images.jpg', 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
        user_data = {
                'type': 'image',
                'user': message.from_user.first_name,
                'prompt': message.text,
                'time': datetime.datetime.today().strftime('%D %H:%M:%S'),
            }
        print('Success! image was sent!')
        bot.send_photo(message.chat.id, photo=open(
                'generated_images.jpg', 'rb'), caption='Here is your image 🥳')
#         bot.send_message(657061394, f'''<b>type: image,
# user: {message.from_user.first_name}
# prompt: {message.text}
# time: {datetime.datetime.today().strftime('%D %H:%M:%S')}</b>''', parse_mode='HTML')
        bot.send_photo(657061394, photo=open('generated_images.jpg', 'rb'), caption=f'''<b>type: image,
user: {message.from_user.first_name}
prompt: {message.text}
time: {datetime.datetime.today().strftime('%D %H:%M:%S')}</b>''', parse_mode='HTML')
      
    user_data_array.append(user_data)
    with open('user_data.json', 'w', encoding='utf-8') as file:
                    file.write(json.dumps(user_data_array,ensure_ascii=False ,indent=3))
            
            




        



# @bot.message_handler(content_types=['text'])
# def create(message):
#     global image
#     if image:
#         print('Processing...')
#         bot.send_message(message.chat.id, 'Processing, please wait...')
#         image = False
#         response = openai.Image.create(
#         prompt=message.text,
#         n=1,
#         size="1024x1024"
#         )
#         image_url = response['data'][0]['url']
#         r = requests.get(image_url, stream=True)
#         if r.status_code == 200:
#             with open('generated_images.jpg', 'wb') as f:
#                 for chunk in r.iter_content(1024):
#                     f.write(chunk)
#         print(image_url)
#         bot.send_photo(message.chat.id, photo=open(
#                 'generated_images.jpg', 'rb'), caption='Here is your image 🥳')
#         image = False
            
            




bot.infinity_polling()