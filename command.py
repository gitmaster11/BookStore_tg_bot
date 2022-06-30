
from telegram import Update,ReplyKeyboardRemove
from telegram.ext import Updater,CallbackContext
from database import *
from Button import *
from geopy.geocoders import Nominatim
import time 
from pprint import pprint

def start(update: Update, context: CallbackContext) -> None:
    human = context.bot.get_chat_member("Group or Channel id",update.effective_user.id)
    
    admin="Bot Admin id"
    context.user_data['adm'] = admin
    if human.status == "left":
        update.message.reply_html('<b>Botimizdan foydalanish uchun guruhga azo bo\'ling</b>',reply_markup = join_channel())
        return 'state_check_join' 
   
    if update.effective_user.id == admin:
        update.message.reply_text("Siz adminsiz.Quyidagilardan birini tanlang\n",reply_markup = admin_button())
        return 'state_admin'

    if check_user(update.effective_user.id):
        update.message.reply_photo(open('Images/book.jpg','rb') ,caption="Izlayotgan  kitobingiz turini tanlang 👇", reply_markup = button_books())
        return 'state_main'
    update.message.reply_text(f'Assalomu alaykum botimizga xush kelibsiz\nRo\'yhatdan o\'tish uchun FIO yuboring',reply_markup = ReplyKeyboardRemove())
    return 'state_name'

    


    

def join_check_channel(update:Update,context:CallbackContext):
    query= update.callback_query
    data = query.data
    
    if data=='check_channel':
        human = context.bot.get_chat_member(-1001611421824,update.effective_user.id)
        if human.status == "left":
            context.bot.answerCallbackQuery(query.id,"Siz hali guruhga azo bo'lmadingiz ❌",show_alert = True)
            return 'state_check_join'
        else:
            admin=1306354017
            context.user_data['adm'] = admin
            if update.effective_user.id == admin:
                query.message.reply_text("Siz adminsiz.Quyidagilardan birini tanlang\n",reply_markup = admin_button())
                return 'state_admin'

            if check_user(update.effective_user.id):
                query.message.reply_photo(open('Images/book.jpg','rb') ,caption="Izlayotgan  kitobingiz turini tanlang 👇", reply_markup = button_books())
                return 'state_main'
            query.message.reply_text(f'Assalomu alaykum botimizga xush kelibsiz\nRo\'yhatdan o\'tish uchun FIO yuboring',reply_markup = ReplyKeyboardRemove())
            return 'state_name'


    

    

def command_main(update:Update,context:CallbackContext):
    data = update.message.text
    if data == 'Kategoriya qo\'shish':
        update.message.reply_text("Yangi Kategoriya nomini kiriting",reply_markup = ReplyKeyboardRemove())
        return "state_add_category"
    elif data  == 'Mahsulot qo\'shish':
        update.message.reply_text("Mahsulot qo'shadigan kategoriyangizni tanlang", reply_markup = category_button())
        return 'state_add_product'

    elif data == 'Asosiy Menuga o\'tish':
        update.message.reply_photo(open('Images/book.jpg','rb') ,caption="Izlayotgan  kitobingiz turini tanlang 👇",reply_markup = button_books())
        return 'state_main'
    
    elif data=='Reklama':
        update.message.reply_text('Yahshi endi reklamani yuboring',reply_markup = ReplyKeyboardRemove())
        return 'state_reklama'
    
    elif data=='Statistika':
        users = get_humans_all()
        update.message.reply_html(f"Botdagi foydalanuvchilar soni <b>{len(users)}ta</b>")


    

def command_send_reklama(update:Update,context:CallbackContext):
    message = update.message
    users  = get_humans_all()
    for i in users:
        try:
            context.bot.forward_message(i[1],update.effective_user.id,message.message_id)
        except Exception as e:
            print(e)
    update.message.reply_text("Reklama Yuborildi",reply_markup = admin_button())
    return 'state_admin'

    



def command_add_category(update:Update,context:CallbackContext):
    category = update.message.text
    add_category(category)
    update.message.reply_text('Kategoriya muvaffaqiyatli qo\'shildi',reply_markup = button_books())
    return 'state_main'


def add_product(update:Update,context:CallbackContext):
    query = update.callback_query
    data = str(query.data)
    query.message.delete()
    # print(data)
    if data.isdigit():
        context.user_data['cat_id'] = data
        query.message.reply_text('Yahshi endi mahsulot nomini kiriting')
        return 'state_add_product_name'

def add_product_name(update:Update,context:CallbackContext):
    product_name = update.message.text
    context.user_data['product_name'] = product_name
    update.message.reply_text('Yahshi endi mahsulot narxini kiriting')
    return 'state_price'

def add_price(update:Update,context:CallbackContext):
    price = update.message.text
    if price.isdigit():
        context.user_data['price'] = price
        update.message.reply_text("Yahshi endi mahsulot rasmini yuboring")
        return "state_image"
    else:
        update.message.reply_text("Siz narxni notog'ri kiritdingiz")
        return "state_price"

def add_image(update:Update,context:CallbackContext):
    update.message.photo[-1].get_file().download(f"Images/{context.user_data['product_name']}.jpg")
    add_product_by_id(context.user_data['cat_id'],context.user_data['product_name'],context.user_data['price'])
    update.message.reply_text("Mahsulot muaffaqiyatli qo'shildi",reply_markup = admin_button())
    return "state_admin"


   

def command_name(update:Update , context:CallbackContext):
   text =  update.message.text
   context.user_data['ism'] = text
   update.message.reply_text(f"Juda Yahshi {context.user_data['ism']}\nEndi Telefon raqamingizni yuboring",reply_markup = phone_button())
   return "state_phone"



def command_phone(update:Update , context:CallbackContext):
    try:
        contact = update.message.contact
        phone_number = contact.phone_number
    except Exception as exc:
        text_phone = update.message.text
        if (text_phone[0]=='+' and len(text_phone)==13 and text_phone[1:4]=='998') or  text_phone[:3]=='998' and len(text_phone)==12 or len(text_phone)==9:
            phone_number = text_phone
        else:
            update.message.reply_text(f"Siz notog'ri raqam kiritidingiz")
            return 'state_phone'


    context.user_data['number'] = phone_number
    update.message.reply_text(f"Sizning ismingiz {context.user_data['ism']}\n"
                             f"Siznig telefon raqamingiz {phone_number}\n"
                             f"Endi esa manzilingizni kiriting",reply_markup = ReplyKeyboardRemove())
    return 'state_viloyat'

def command_region(update:Update,context:CallbackContext):
    text = update.message.text
    update.message.reply_text(f"Sizning Isminigiz {context.user_data['ism']}\n"
                             f"Siznig telefon raqamingiz {context.user_data['number']}\n"
                             f"Sizning Manzilingiz {text}\n"
                             f"Muvaffaqiyatli ro'yhatdan o'tildi")
    update.message.reply_photo(open('Images/book.jpg','rb'), caption ="Izlayotgan  kitobingiz turini tanlang 👇", reply_markup = button_books())
    insert_table(update.effective_user.id,context.user_data['ism'],update.effective_user.first_name,context.user_data['number'],text)
    return 'state_main'







def add_box_books(update:Update,context:CallbackContext):
    query = update.callback_query
    data = query.data
    if data == 'retry':
        query.message.delete()
        query.message.reply_photo(open('Images/book.jpg','rb'), caption ="Izlayotgan  kitobingiz turini tanlang 👇", reply_markup = button_books())
        return 'state_main'

    elif data == "name":
        return 'state_box'

    elif data=='confirm':
        query.message.delete()
        query.message.reply_text(f"Juda Yahshi {update.effective_user.first_name} endi bizga joylashuvingizni yuboring",reply_markup = locat_button())
        return 'state_location'


    else:
        
        type, id = data.split('_')
        order_id = get_order(update.effective_user.id)
        ord_det = get_order_books(order_id)
        if type=="plus":
            update_order_det(int(id))

        else:
            if check_ord_det(int(id)):
                update_order_detail((id))
            


        order_id = get_order(update.effective_user.id)
        ord_det = get_order_books(order_id)
        if len(ord_det)==0:
        
            context.bot.answerCallbackQuery(query.id,"Savatchangizda kitob qolmadi. Qaytadan kitob tanlashingiz mumkin 🛒",show_alert = True)
            query.message.reply_photo(open('Images/book.jpg','rb') ,caption=f"Izlayotgan  kitobingiz turini tanlang 👇", reply_markup = button_books())
            return 'state_main'
        else:
            xabar = ""
            sanoq = 1
            jami = 0
                
            for i in ord_det:
                product = get_books(i[2])
                xabar +=f"{sanoq}:{product[2]} {i[3]} x {product[3]}={i[3]*product[3]}so'm\n "
                sanoq +=1
                jami += i[3]*product[3]
            xabar+=f"Jami:{jami} so'm"
            query.message.edit_text(xabar,reply_markup= button_box(ord_det),parse_mode = "HTML")
            return "state_box" 
    
def command_locat(update:Update,context:CallbackContext):
    latitude  = update.message.location.latitude
    longitude = update.message.location.longitude
    app = Nominatim(user_agent = 'tutorial')
    coordinates = f"{latitude},{longitude}"
    adres = app.reverse(coordinates,language='eng').raw['display_name']
    update.message.reply_html(f"<b>{adres}\nManzilingiz to'g'ri ekanligini tekshiring</b>",reply_markup = check_button_locat())
    context.user_data['lat'] = latitude
    context.user_data['long'] = longitude
    context.user_data['adres'] = adres

    return "state_check_button_locat"



def command_confirm(update:Update,context:CallbackContext):
    
    update.message.reply_html("<b>Buyurtma muvaffaqiyatli qabul qilindi</b> ✅",reply_markup = button_books())
    
    
    o_id = get_order(update.effective_user.id)
    order_id = list(get_order_confirm(update.effective_user.id))
    order_dets = get_order_books(o_id)

    
    
    change_order_status(o_id)
    about_user = get_done_status(update.effective_user.id)
    xabar = ""
    for i in about_user:
        context.user_data['time'] = i[2]


    xabar += f"<b>Yangi buyurtma</b> 🚕 \n<b>Buyurtma raqami</b>:№{order_id[0]}\n<b>Buyurtma Vaqti</b>:\n{context.user_data['time']}\n\n<b>Mahsulotlar</b> 📚:\n"
    about_humans = get_humans(update.effective_user.id)
    for i in order_dets:
        book = get_books(i[2])
        xabar +=f"<b>{book[2]}</b> ==> {i[3]} x {book[3]} = {i[3]*book[3]} so'm\n\n"
    
    for i in about_humans:
        xabar+=f"<b>Ismi</b> 🙎‍♂️:{i[3]}\n<b>Phone</b> ☎️:{i[4]}\n"

    xabar +=f"<b>Manzili</b> 🏠:\n{context.user_data['adres']}"
    context.bot.send_message("Group or Channel id",xabar,parse_mode = "HTML")
    context.bot.send_location("Group or Channel id",context.user_data['lat'],context.user_data['long'])
    
    return 'state_main'
    
    
def command_books_category(update:Update,context:CallbackContext):
    query = update.callback_query
    data = str(query.data)
    

    context.user_data['ortga']= data

    if data.isdigit():
        query.message.delete()
        cat_name = get_books_name_catid(data)
        for i in cat_name:
            context.user_data['cat_name'] = i[1]
        query.message.reply_photo(open('Images/book.jpg','rb'),caption=f"Bo'lim:<b>{context.user_data['cat_name']}</b>",reply_markup = books_name_button(int(data)),parse_mode = "HTML")
        
        return 'state_books'

    elif data == 'self_books':
        
        order_id = get_order(update.effective_user.id)
        ord_det = get_order_books(order_id)

        if len(ord_det)==0 :
            context.bot.answerCallbackQuery(query.id,"Kitob savatchangiz bo'sh 🛒",show_alert = True)

        
           

        else:
            query.message.delete()
            xabar = ""
            sanoq = 1
            jami = 0
            
            for i in ord_det:
                product = get_books(i[2])
                xabar += f"{sanoq}:{product[2]} {i[3]} x {product[3]}={i[3]*product[3]}so'm\n\n"
                sanoq+=1
                jami += i[3]*product[3]
            xabar+=f"Jami:{jami} so'm"
            query.message.reply_text(xabar,reply_markup= button_box(ord_det))

            return "state_box"
    elif data == 'admin':
        
        if update.effective_user.id == context.user_data['adm']:
            query.message.delete()
            query.message.reply_text("Siz adminsiz.Quyidagilardan birini tanlang\n",reply_markup = admin_button())
            return 'state_admin'
        else:
            context.bot.answerCallbackQuery(query.id,"Siz admin emassiz ❌",show_alert = True)
            
    elif  data == "history":

        order_get = get_done_status(update.effective_user.id)
        xabar = "<b>Sizning barcha buyurtmalaringiz</b> 📝\n\n"
        sanoq = 1
        jami = 0
        if len(order_get):
            query.message.delete()
            for i in order_get:
                xabar +=f"Vaqti:{i[2]}\n"
                order_details = get_order_books(i[0])
                for i in order_details:
                    book_about = get_books(i[2])
                   
                    xabar +=f"<b>{sanoq}: {book_about[2]}</b> ==> {i[3]}x{book_about[3]}={i[3]*book_about[3]} so'm\n\n"
                    sanoq+=1
                    jami+=i[3]*book_about[3]
                xabar+=f"<b>Jami:{jami} so'm</b>\n\n"
            query.message.reply_html(xabar,reply_markup = history_button())
            return 'state_history_button'
            
        else:
            context.bot.answerCallbackQuery(query.id,"Sizda buyurtmalar tarixi mavjud emas ❌",show_alert = True)

    elif data=='user':
        pass
        


def command_history(update:Update,context:CallbackContext):
    query = update.callback_query
    data = query.data 
    query.message.delete()
    if data =="back_home":
        query.message.reply_photo(open('Images/book.jpg','rb'), caption ="Izlayotgan  kitobingiz turini tanlang 👇", reply_markup = button_books())
        return 'state_main'
    elif data=="cls":
        
        delete_orders(update.effective_user.id)
        
        del_done_status(update.effective_user.id)
        
        context.bot.answerCallbackQuery(query.id,"Buyurtmalar tarixingiz muaffaqiyatli o'chirildi  ✅",show_alert = True)
        query.message.reply_photo(open('Images/book.jpg','rb'), caption ="Izlayotgan  kitobingiz turini tanlang 👇", reply_markup = button_books())
        return 'state_main'




            
            

    

def command_books(update:Update,context:CallbackContext):
    query = update.callback_query
    data = query.data
    query.message.delete()
    if data == 'back':
        query.message.reply_photo(open('Images/book.jpg','rb') ,caption=f"Izlayotgan  kitobingiz turini tanlang 👇", reply_markup = button_books()) 
        return 'state_main' 
    
    elif data.isdigit():
        data = get_book(int(data))
        context.user_data['kitob'] = data[2]
        context.user_data['narxi'] = data[3]
        context.user_data['product_id'] = data[0]
        xabar = f'''{data[2]} kitobi.Narxi:{data[3]} so'm'''
        try:
            query.message.reply_photo(open(f"Images/{data[2]}.jpg",'rb'),caption = xabar,reply_markup= quant_button())
        except:
            query.message.reply_photo(open(f"{data[4]} ","rb"), caption = xabar,reply_markup= quant_button())

        context.user_data['soni'] = ''
        return 'state_books_count'
    
           
           
           
           

def command_books_count(update:Update,context:CallbackContext):
    query = update.callback_query
    data = query.data
    soni= context.user_data['ortga']
    kitob = context.user_data['kitob']
    narx = context.user_data['narxi']
    if data == 'nazad':
        query.message.delete()
        xabar = f"<b>Bo'lim:{context.user_data['cat_name']}</b>"
        query.message.reply_photo(open('Images/book.jpg','rb'),caption = f"{xabar}",reply_markup= books_name_button(int(soni)), parse_mode ="HTML")
        return 'state_books'
    elif data =='brauzer':
        url = '<a href ="https://books.google.com">Search</a>'
        query.message.reply_html(f"Kitobingizni shu link orqali ham izlashingiz mumkin {url}")
    elif data.isdigit():
        soni = '0'
        if context.user_data['soni']:
            soni = context.user_data['soni']+data
            context.user_data['soni'] = soni
        elif data!='0' and not(context.user_data['soni']):
            soni = data
            context.user_data['soni']=soni
        else:
            return 'state_books_count'
        query.message.edit_reply_markup(reply_markup = quant_button(soni))
    elif data == 'del':
        if context.user_data['soni']:
            soni = context.user_data['soni'][:-1]
            context.user_data['soni'] = soni
            query.message.edit_reply_markup(reply_markup = quant_button(soni))
    elif data =='clear':
        if context.user_data['soni']:
            context.user_data['soni'] = ''
            query.message.edit_reply_markup(reply_markup = quant_button())

    elif data =='box':
        if context.user_data['soni']!='0' and context.user_data['soni']!='':
            order_id = get_order(update.effective_user.id)
            product_id = context.user_data['product_id']
            quantity = context.user_data['soni']
            tg_id = update.effective_user.id
            add_order_table(order_id,product_id,quantity,tg_id)
            query.message.delete()
            query.message.reply_html("<b>Kitoblar savatcha joylandi</b> ✅",reply_markup = button_books())
            return 'state_main' 
        else:
            context.bot.answerCallbackQuery(query.id,"Siz kitob tanlamadingiz 🛒",show_alert = True)

        
    
        


        




    


    