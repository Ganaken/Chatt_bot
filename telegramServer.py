# importing modules
import pymysql as pymysql
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
import FAQChattbot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import time
# Our tokens instance
updater = Updater(token='613480097:AAEgNDeElBmbzDD138Um-HZiSL8bRFTTxR4')
# create our dispatcher
dispatcher = updater.dispatcher
# for logging(it is used for applicatuon building to keep track of your application errors nad daily functiolning
import logging
# call the logging basic config
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
contextvar = [] # to map the context of the conversation
user =[] # to keep a log of users
fine_context = [] #to keep track of a specific fine
intent_context=[]
expire_details=[]
card_context = []
card_exp = []
card_cvc = []
balance = []
vehicle = []
global card_number
global expiry_date
global cvc_number
global chk

def echo(bot, update):
    print('echo',update.message.text)# to check the user input debugging porpose
    # when ever the user says one of the words below the buttons appear
    if (update.message.text).lower() == 'hi' or (update.message.text).lower() == 'hello'or (update.message.text).lower() == 'done'or (update.message.text).lower() == 'thanks'or (update.message.text).lower() == 'reset':

        # declaration of buttons
        keyboard = [[InlineKeyboardButton("Traffic Violation Penalties", callback_data='FAQs'),
                     InlineKeyboardButton("Fine Payment", callback_data='Fine Payment')],

                    ]
        # saving the buttons in a variable
        reply_markup = InlineKeyboardMarkup(keyboard)
        # whenevr you want to send simple text messages use bot.send_message
        bot.send_message(chat_id=update.message.chat_id, text="Hi Welcome to Dubai Police Please ask your queries!")
        # finally sending the buttons
        update.message.reply_text('Please choose:', reply_markup=reply_markup)

    else:
        print(contextvar[-1])
        # enters this part of the code if no greeting provided
        import requests
        import json
        # my dialogue flow http address

        # dialoguefolw code starts
        url = "https://api.dialogflow.com/v1/query"
        # specifying the language
        querystring = {"lang": "en", "query": update.message.text, "sessionId": "12345", "context": "alexa"}

        headers = {
            'Content-Type': "application/json",
            'Cache-Control': "no-cache",
            'Authorization': "Bearer 7af305dfce0b4ed7b5d8632ae0975591",# you get 4157a13018924c4c88b16ec4ebdc356e from dialogue flow everything thing else remains same
        }#  my bearer token 7af305dfce0b4ed7b5d8632ae0975591

        response = requests.request("GET", url, headers=headers, params=querystring)
        # dialogue flow api code ends

        print(response.text)
        # we convert our response to json
        api_data = json.loads(response.text)
        # there are going to be times when yiu will have no intent
        try:
            #extracting the intent from the response
            intent = api_data['result']['metadata']['intentName']
        except KeyError:
            intent = ''
        # Now we start testing for intents
        # intent checks the intentions. And contextvar is getting the name for that specific
        # context(button pressed )
        if intent == 'get_name' and (contextvar[-1]).lower() == 'fine payment by vehicle number':
            # storing the name value (entity)
            name = api_data['result']['parameters']['name']
            print(name)
            intent_context.append(intent)
            # append the name of the user that is chatting with the chatbot
            user.append(name)
            print(name)
            # enter the database and search user
            if name !="":
                sql = "SELECT * from user_master where user_name ='" + name + "'"
                import pymysql
                db = pymysql.connect("localhost", "root", "lol123lol", "DubaiPolice")
                # sets the pointer at the begining of the table
                cursor = db.cursor()
                print("sql ghussa")

                try:
                    # execute sql query
                    cursor.execute(sql)
                    # fetch all results
                    results = cursor.fetchall()
                    # send list of vehicles registered under that user name
                    bot.send_message(chat_id=update.message.chat_id,
                                     text="We have identified "+str(len(results))+" Vehicle/s under your name.\nPlease provide the vehicle number of your choice.")
                    bot.send_message(chat_id=update.message.chat_id,
                                   text="List of registered vehicle/s")
                    # print the list of registered vehicles
                    for row in results:
                        bot.send_message(chat_id=update.message.chat_id,
                                         text=str(row[2]))

                except:
                    print("Error: unable to fecth data")

                # disconnect from server
                db.close()
            # if unable to identify user name
            else:
                bot.send_message(chat_id=update.message.chat_id,
                                text="Unable to identify the user")
        elif intent == 'get_vehicle_no' and (contextvar[-1]).lower()== 'fine payment by vehicle number':
            vehicle_no = api_data['result']['parameters']['vehicle_no']
            print(vehicle_no)
            intent_context.append(intent)
            if vehicle_no !="":
                sql = "select sum(fine), vehicle_no from fine_master where vehicle_no ='"+ vehicle_no + "'"
                import pymysql
                db = pymysql.connect("localhost", "root", "lol123lol", "DubaiPolice")
                cursor = db.cursor()

                cursor.execute(sql)
                results = cursor.fetchone()
                bot.send_message(chat_id=update.message.chat_id,
                             text="Fine for this vehicle is "+str(results[0])+" AED")
                bot.send_message(chat_id=update.message.chat_id,
                                text="Are you sure you want to pay?")
                print(results[0])
                # saving fines price
                fine_context.append(results[0])
                vehicle.append((results[1]))
                db.close()
                # ------------------------------------------------------------------------------------------------
                # sql = "SELECT * from creditcard_master where user_name ='" + user[-1] + "'"
                # import pymysql
                # db = pymysql.connect("localhost", "root", "lol123lol", "DubaiPolice")
                # cursor = db.cursor()
                # try:
                #     cursor.execute(sql)
                #     results = cursor.fetchall()
                #     bot.send_message(chat_id=update.message.chat_id,
                #                      text="We have identified " + str(len(
                #                          results)) + " card/s under your name.\nPlease provide the last 4 digit for the card of your choice.")
                #     bot.send_message(chat_id=update.message.chat_id,
                #                      text="List of registered card/s")
                #     for row in results:
                #         bot.send_message(chat_id=update.message.chat_id,
                #                          text=str(row[3]))
                #
                # except:
                #     print("Error: unable to fecth data")

                # disconnect from server

                db.close()
                # ------------------------------------------------------------------------------------------------

            else:
                bot.send_message(chat_id=update.message.chat_id,
                                text="Unable to identify the Vehicle")
        # elif intent == 'get_vehicle_no' and (contextvar[-1]).lower() == 'vehicle enquery':
        #     vehicle_no = api_data['result']['parameters']['vehicle_no']
        #     print(vehicle_no)
        #     if vehicle_no != "":
        #         sql = "select * from vehicle_info where vehicle_no = '" + vehicle_no + "'"
        #         import pymysql
        #         db = pymysql.connect("localhost", "root", "lol123lol", "DubaiPolice")
        #         cursor = db.cursor()
        #
        #         cursor.execute(sql)
        #         results = cursor.fetchone()
        #         try:
        #             bot.send_message(chat_id=update.message.chat_id,
        #                          text="Vehicle Number: "+str(results[0])+"\n"+"Vehicle colour :"+str(results[1])
        #                               +"\n"+"Registration Year :"+str(results[2])+"\n"+"Model :"+str(results[4])+
        #                               "\n" + "Brand :" + str(results[5]) )
        #         except:
        #             bot.send_message(chat_id=update.message.chat_id,
        #                              text="No Registered vehicle found")
        #
        #         db.close()
        elif intent == 'get_trafficfile_no' and (contextvar[-1]).lower() == 'fine payment by traffic file number':
            trafficfile_no = api_data['result']['parameters']['trafficfile_no']
            print(trafficfile_no)
            intent_context.append(intent)
            if trafficfile_no != "":
                sql = "select sum(fine) from fine_master where traffic_file_no='" + trafficfile_no + "'"
                import pymysql
                db = pymysql.connect("localhost", "root", "lol123lol", "DubaiPolice")
                cursor = db.cursor()

                cursor.execute(sql)
                results = cursor.fetchone()
                print(results[0])
                try:
                    bot.send_message(chat_id=update.message.chat_id,
                                 text="Your total fine is :"+str(results[0])+" AED" )

                except:
                    bot.send_message(chat_id=update.message.chat_id,
                                     text="No fine associated with this traffic file number")

                db.close()

        elif intent == 'positive' and (contextvar[-1]).lower()=='fine payment by vehicle number':
            intent_context.append(intent)
            bot.send_message(chat_id = update.message.chat_id, text ="Please provide your card number")
        elif intent == 'negative' and (contextvar[-1]).lower() == 'fine payment by vehicle number':
            # declaration of buttons
            intent_context.append(intent)
            keyboard = [[InlineKeyboardButton("FAQs", callback_data='FAQs'),
                         InlineKeyboardButton("Fine Payment", callback_data='Fine Payment')],

                        ]
            # saving the buttons in a variable
            reply_markup = InlineKeyboardMarkup(keyboard)
            # whenevr you want to send simple text messages use bot.send_message
            bot.send_message(chat_id=update.message.chat_id, text="Alright! no problem what would you like to do next?")
            # finally sending the buttons
            update.message.reply_text('Please choose:', reply_markup=reply_markup)
        elif intent == 'get_card_no' and (contextvar[-1]).lower() == 'fine payment by vehicle number':
            card_no = api_data['result']['parameters']['card_no']
            intent_context.append(intent)
            card_context.append(card_no)
            print(card_no)
            if card_no != "":
                sql = "select * from creditcard_master where card_no = "+str(card_no)+""
                import pymysql
                db = pymysql.connect("localhost", "root", "lol123lol", "DubaiPolice")
                cursor = db.cursor()

                cursor.execute(sql)
                results = cursor.fetchone()
                card_number = str(results[3])
                expiry_date = str(results[4])
                cvc_code = str(results[5])
                bal = str(results[6])
                card_exp.append(expiry_date)
                card_cvc.append(cvc_code)
                balance.append(bal)
                print("Card number " + card_number)
                print("Expiry Date " + expiry_date)
                print("CVC number " + cvc_code)
                if(card_number == card_no):
                    bot.send_message(chat_id=update.message.chat_id,text="Please provide expiry date (mm/yy)")
                else:
                    bot.send_message(chat_id=update.message.chat_id, text="Incorrect card number")
                chk = True

                 # if fine_context[-1]<=results[0]:
                #     bot.send_message(chat_id=update.message.chat_id,
                #                      text="Sufficient Balance in card")
                #     bot.send_message(chat_id=update.message.chat_id,
                #                      text="Please Pay the fine Here :---->\nhttps://traffic.rta.ae/trfesrv/public_resources/ffu/fines-payment.do")
                # else:
                #     bot.send_message(chat_id=update.message.chat_id,
                #                      text="Insufficient Balance in card, please select some other card.")
                db.close()

        elif intent == 'get_expiry_date' and (contextvar[-1]).lower() == 'fine payment by vehicle number':
            exp_date1 = api_data['result']['parameters']['number']
            num = exp_date1
            exp_date2 = api_data['result']['parameters']['number1']
            count = 0
            while (int(num) > 0):
                count = count + 1
                num = int(num) // 10
            print(str(count))
            if count == 1:
                u_input = str("0" + str(exp_date1) + "/" + str(exp_date2))
            else:
                u_input = str(exp_date1 + "/" + exp_date2)

            print(u_input)
            print(card_exp[0])
            if u_input != "":
                if u_input == str(card_exp[0]):
                    bot.send_message(chat_id=update.message.chat_id, text="Please enter cvc code")
                else:
                    bot.send_message(chat_id=update.message.chat_id, text="Incorrect expiry date")

        elif intent == 'get_card_cvc' and (contextvar[-1]).lower() == 'fine payment by vehicle number':
            cvc = api_data['result']['parameters']['card_cvc']
            if cvc != "":
                import pymysql
                if str(cvc) == str(card_cvc[0]):
                    db = pymysql.connect("localhost", "root", "lol123lol", "DubaiPolice",autocommit = True)
                    cursor = db.cursor()
                    sql = "update fine_master set fine = '0' where  vehicle_no = '" + vehicle[0] + "'"
                    if float(balance[0]) > float(fine_context[0]):
                        cursor.execute(sql)
                        bot.send_message(chat_id=update.message.chat_id, text="Payement successful!!!!")
                    else:
                        bot.send_message(chat_id=update.message.chat_id, text="Sorry Insuffcient funds")
                else:
                    bot.send_message(chat_id=update.message.chat_id, text="Incorrect details")
            db.close()
        else:
            if (contextvar[-1]).lower()=='fine payment by vehicle number' and (contextvar[-2]).lower()=='fine payment' and (intent_context[-1]).lower()!='get_card_no':
                bot.send_message(chat_id=update.message.chat_id,
                                 text="Unable to find the relevant car details")


            elif (intent_context[-1]).lower()=='get_card_no' and (contextvar[-1]).lower()=='fine payment by vehicle number':
                if (update.message.text).lower() == expire_details[-1]:
                    bot.send_message(chat_id=update.message.chat_id,
                                 text="Correct deatils")
                    bot.send_message(chat_id=update.message.chat_id,
                                 text="Please Pay the fine Here :---->\nhttps://traffic.rta.ae/trfesrv/public_resources/ffu/fines-payment.do")
                else:
                    bot.send_message(chat_id=update.message.chat_id,
                                 text="Incorrect details")

            else:
                answer = FAQChattbot.main_bot(1, update.message.text)
                bot.send_message(chat_id=update.message.chat_id, text=answer)


echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


def start(bot, update):
    keyboard = [[InlineKeyboardButton("FAQs", callback_data='FAQs'),
                 InlineKeyboardButton("Fine Payment", callback_data='Fine Payment')],

                [InlineKeyboardButton("Vehicle Enquery", callback_data='Vehicle Enquery')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=update.message.chat_id, text="Hi Welcome to Dubai Police Please ask your queries!")
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def button(bot, update):
    # the user button callback value
    query = update.callback_query
    # append contextvar with intention
    contextvar.append(query.data)
    #
    if (query.data).lower() == 'fine payment':
        keyboard1 = [[InlineKeyboardButton("By Vehicle Number", callback_data='fine payment by vehicle number'),
                     InlineKeyboardButton("By Traffic file Number", callback_data='fine payment by traffic file number')]]

        reply_markup1 = InlineKeyboardMarkup(keyboard1)
        query.message.reply_text('Please select an option for fine payment:', reply_markup=reply_markup1)
    elif (query.data).lower()== 'faqs':
        bot.edit_message_text(text="Selected option: {}".format(query.data),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        bot.send_message(chat_id=query.message.chat_id, text="Please ask about traffic violations penalties")
    elif ((query.data).lower() == 'fine payment by vehicle number'):
        bot.send_message(chat_id=query.message.chat_id, text="Please provide your vehicle number")
    elif ((query.data).lower() == 'fine payment by traffic file number'):
        bot.send_message(chat_id=query.message.chat_id, text="Please provide your traffic file number")
    else:
        pass

updater.dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()

