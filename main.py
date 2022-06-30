
from telegram.ext import Updater, CommandHandler,MessageHandler,Filters,CallbackQueryHandler,ConversationHandler
from Button import *
from database  import *
from command import *



conv_hand = ConversationHandler(
    entry_points = [
        CommandHandler('start', start)
    ],
    states = {
        "state_name":[
            CommandHandler('start',start),
            MessageHandler(Filters.text,command_name)
        ],
        "state_phone":[
            MessageHandler(Filters.text,command_phone),
            MessageHandler(Filters.contact,command_phone)   
        ],

        "state_viloyat":[
            CommandHandler('start',start),
            MessageHandler(Filters.text,command_region)
        ],
        'state_main':[
            CallbackQueryHandler(command_books_category)
        ],
        'state_books':[ 
            CallbackQueryHandler(command_books)
        ],
        'state_books_count':[
            CallbackQueryHandler(command_books_count)
        ],
        'state_admin':[
            CommandHandler('start',start),
            MessageHandler(Filters.text,command_main)
        ],
        'state_add_category':[
            CommandHandler('start',start),
            MessageHandler(Filters.text,command_add_category)
        ],
        'state_add_product':[
            CommandHandler('start',start),
            CallbackQueryHandler(add_product)
        ],
        'state_add_product_name':[
            CommandHandler('start',start),
            MessageHandler(Filters.text,add_product_name)
        ],
        'state_price':[
            CommandHandler('start',start),
            MessageHandler(Filters.text,add_price)
        ],
        "state_image":[
            CommandHandler("start",start),
            MessageHandler(Filters.photo,add_image)
        ],
        'state_box':[
            CallbackQueryHandler(add_box_books)
        ],
        'state_location':[
            MessageHandler(Filters.location,command_locat)
        ],
        'state_check_button_locat':[
            MessageHandler(Filters.text,command_confirm),
            MessageHandler(Filters.location,callback = command_locat)
        ],
        'state_history_button':[
            CallbackQueryHandler(command_history)
        ],
        'state_check_join':[
            CallbackQueryHandler(join_check_channel)
        ],
        'state_reklama':[
            CommandHandler('start',start),
            MessageHandler(Filters.all,command_send_reklama)
        ]


    },
    fallbacks= [
        CommandHandler("start",start)
    ]
)




token = '5537052451:AAHazSuq6QMP5e2COxpSc_5vCN-b4KdxwBA'

updater = Updater("Bot Token")

updater.dispatcher.add_handler(conv_hand)


updater.start_polling()
updater.idle()  