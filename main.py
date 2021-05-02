#!/usr/bin/env python
import check_places
import telebot
import time
import env

bot = telebot.TeleBot(env.token)

bot.send_message(env.id_users[0], '/start')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Ну привет!')
    if message.chat.id in env.id_users:
        bot.send_message(message.chat.id, f"Access is allowed! \nYour id:{message.chat.id}")
        time.sleep(5)
        old_sum_nums = 0
        while True:
            list_all_carts, sum_nums = check_places.get_data(check_places.get_html(env.base_url))
            if bool(list_all_carts) is True and sum_nums > old_sum_nums:
                for chat_id in env.id_users:
                    bot.send_message(chat_id,
                                     'Have a new free place!\nhttps://my.greenforest.com.ua/profile/courses')
                    for cart in list_all_carts:
                        bot.send_message(chat_id, cart)
                old_sum_nums = sum_nums
                time.sleep(300)
            else:
                time.sleep(300)
    else:
        bot.send_message(message.chat.id,
                         f"Access denied! \nYour id:{message.chat.id} \nSend your id to administrator!")


@bot.message_handler(content_types=['text'])
def handle(message):
    if message.chat.id in env.id_users:
        bot.send_message(message.chat.id, f"Access is allowed! \nYour id:{message.chat.id}")

    else:
        bot.send_message(message.chat.id, f"Access denied! \nYour id:{message.chat.id}")


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    if message.chat.id in env.id_users:
        bot.send_message(message.chat.id, message)
    else:
        bot.send_message(message.chat.id, f"Access denied! \nYour id:{message.chat.id}")


bot.polling(none_stop=True, interval=0)
