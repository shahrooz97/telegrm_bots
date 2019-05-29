from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from telegram import ReplyKeyboardMarkup, ChatAction, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

#from mysql_dbhelp import *
import logging
from functools import wraps
import datetime
import os




token = '567750227:AAFstiaYUIchEHalnV4ZWwGdxAIcKwbx_rc'

#setup_db()
logging.basicConfig(filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def restricted(func):
    @wraps(func)
    def wrapped (update, context, *args, **kwargs):
        user_id = update.effective_user.id 
        chatid = update.message.chat_id
        user_status = context.bot.get_chat_member(chatid, user_id)
        val = {'creator', 'administrator'}
        if user_status.status not in val:
            #print('Unauthorized access denied for {}'.format(user_id))
            return 
        return func(update, context, *args, **kwargs)
    return wrapped


def start(update, context):
    keybord = ReplyKeyboardMarkup([['راهنما']], resize_keyboard=True)
    userid = update.effective_user.id 
    chatid = update.message.chat_id
    #print(update.message)
    #print(context.bot.get_chat_member(chatid, userid))

    try:
        username = update.effective_user.username 
        userid = update.effective_user.id
        if len(get_db(where=userid)) < 1:
            insert_to_db((id, user_name, None, None, None))
        else:
            pass
    except Exception as e:
        print(e)


def button(update, context):
    chatid = update.message.chat_id
    userid = update.effective_user.id
    user_status = context.bot.get_chat_member(chatid, userid)
    msg = update.message
    
    #check if new member who added by the user is a bot return true or false if not
    is_bot = msg.new_chat_members[0]['is_bot']

    admins = {'creator', 'administrator'}
    if user_status.status not in admins:
        if is_bot:
            context.bot.kick_chat_member(chatid, msg.new_chat_members[0]['id'])
            msg.reply_text('شما اجزه ندادی دبات اضافه کنید')
        else:
            keyboard = [
                    [InlineKeyboardButton('من ربات نیستم',callback_data=1),
                        InlineKeyboardButton('من رباتم', callback_data=2)]
                    ]

            context.bot.restrict_chat_member(chatid, userid,can_send_message=False, can_send_other_messages=False)

            reply_markup = InlineKeyboardMarkup(keyboard)
            txt = """
            برای جلوگیری از ورود رباتها به سوال زیر پاسخ دهید
        در صورت پاسخ اشتباه شما بی صدا خواهید شد
        آیا شما ربات هستید؟ 

            """
            update.message.reply_text(txt, reply_markup=reply_markup)


def button_callback(update, context):
    query = update.callback_query
    userid = update.effective_user.id
    f_name = update.effective_user.first_name
    chatid = query.message.chat_id
    if query.data=='1':
        query.edit_message_text(text='خوش آمدید {}'.format(f_name))
        context.bot.restrict_chat_member(chatid, userid,can_send_message=True, can_send_other_messages=True)
    else:
        context.bot.delete_message(chatid, query.message.message_id)



def get_admins(update, context):
    admins = []
    msg = update.message 
    r=context.bot.get_chat_administrators(msg.chat_id)
    for admin in r:
        user_name = admin.user['username']
        status = ['سازنده گروه' if admin.status=='creator' else 'ادمین']
        is_bot = ['🤖' if admin.user['is_bot']==True else '👤']
        admins.append("""
 {}\n@{}\n{}\n{}\n
                """.format(admin.user['first_name'],user_name, status[0], is_bot[0]))
    context.bot.send_message(msg.chat_id, '\n'.join(admins))

@restricted
def get_gp_link(update, context):
    msg = update.message
    gp_link = context.bot.export_chat_invite_link(msg.chat_id)
    update.message.reply_text('لینک گروه\n\n'+gp_link)

@restricted
def kick_member(update, context):
    msg = update.message.reply_to_message 
    chatid = msg.chat_id
    userid = msg.from_user.id
    #print(msg)
    context.bot.kick_chat_member(chatid, userid)

@restricted
def unban_chat_member(update, context):
    msg = update.message.reply_to_message 
    chatid = msg.chat_id
    userid = msg.from_user.id
    context.bot.unban_chat_member(chatid, userid)

@restricted
def restrict_member(update, context):
    msg = update.message.reply_to_message 
    f_name = msg.from_user.first_name
    chatid = msg.chat_id
    userid = msg.from_user.id
    context.bot.restrict_chat_member(chatid, userid,
            can_send_message=False,
            can_send_other_messages=False)
    update.message.reply_text('{} بی صدا شد'.format(f_name))

@restricted
def unrestrict_member(update, context):
    msg = update.message.reply_to_message 
    f_name = msg.from_user.first_name
    chatid = msg.chat_id
    userid = msg.from_user.id
    context.bot.restrict_chat_member(chatid, userid,
            can_send_message=True,
            can_send_other_messages=True)
    update.message.reply_text('{} از محدودیت درآمد'.format(f_name))

@restricted
def get_user_info(update, context):
    msg = update.message.reply_to_message 
    chatid = msg.chat_id
    userid = msg.from_user.id
    r = context.bot.get_chat_member(chat_id=chatid, user_id=userid)
    context.bot.send_message(chatid, 'نام: {}\n\nایدی: {}\n\nنام کاربری: @{}\n\nربات: {}'.format(r.user.first_name, r.user.id, r.user.username, r.user.is_bot))


@restricted
def pin_the_message(update, context):
    msg = update.message.reply_to_message 
    chatid = msg.chat_id
    msg_id = msg.message_id 
    context.bot.pin_chat_message(chatid, msg_id)

@restricted
def promote_member(update, context):
    msg = update.message.reply_to_message 
    f_name = msg.from_user.first_name
    chatid = msg.chat_id
    userid = msg.from_user.id
    try:
        context.bot.promote_chat_member(chatid, userid,
                can_delete_messages=True, 
                can_invite_users=True,
                can_restrict_members=True,
                can_pin_messages=True)
        update.message.reply_text('{} به لیست مدیران گروه اضافه شد'.format(f_name))
    except Exception:
        update.message.reply_text('شما مجوزهای لازم جهت ارتفای کاربران به مدیریت را به ربات نداده اید \nلطفا از بخش تنطیمات گروه دسترسی های  لازم را برای ربات صادر کنید ')
    
@restricted 
def unpromote_member(update, context):
    msg = update.message.reply_to_message 
    f_name = msg.from_user.first_name
    chatid = msg.chat_id
    userid = msg.from_user.id
    try:
        context.bot.promote_chat_member(chatid, userid,
                can_delete_messages=False, 
                can_invite_users=False,
                can_restrict_members=False,
                can_pin_messages=False)
        update.message.reply_text('{} از مدیریت عزل شد'.format(f_name))
    except Exception:
        update.message.reply_text('شما مجوزهای لازم جهت ارتفای کاربران به مدیریت را به ربات نداده اید \nلطفا از بخش تنطیمات گروه دسترسی های  لازم را برای ربات صادر کنید ')


def main():
    updater = Updater(token, use_context=True)
    #j = updater.job_queue
    #j.run_daily(update_admins, time=datetime.time(22, 57, 1), days=(0,1,2,3,4,5,6))
    db = updater.dispatcher
    db.add_handler(CommandHandler('start', start, Filters.private))

    db.add_handler(CommandHandler('info', get_user_info, Filters.group, pass_args=True))

    db.add_handler(CallbackQueryHandler(button_callback))

    db.add_handler(MessageHandler(Filters.group and Filters.status_update.new_chat_members, button))
    db.add_handler(MessageHandler(Filters.group and Filters.regex('^[/!]\s?admins$'), get_admins))

    db.add_handler(MessageHandler(Filters.group and Filters.regex('^[/!].?gp_link$'), get_gp_link))

    db.add_handler(MessageHandler(Filters.group and Filters.regex('^[/!].?kick$'), kick_member))

    db.add_handler(MessageHandler(Filters.group and Filters.regex('^[/!].?unban$'), unban_chat_member))

    db.add_handler(MessageHandler(Filters.group and Filters.regex('^[/!]\s?mute$'), restrict_member))

    db.add_handler(MessageHandler(Filters.group and Filters.regex('^[/!]\s?unmute$'), unrestrict_member))

    #db.add_handler(MessageHandler(Filters.group and Filters.regex('^[/!]\s?info$'), get_user_info),pass_args=True)


    db.add_handler(MessageHandler(Filters.group and Filters.regex('^[/!]\s?pin$'), pin_the_message))


    db.add_handler(MessageHandler(Filters.group and Filters.regex('^[/!]\s?promote$'), promote_member))

    db.add_handler(MessageHandler(Filters.group and Filters.regex('^[/!]\s?unpromote$'), unpromote_member))

    db.add_handler(MessageHandler(Filters.group and Filters.regex('^[/!]\s?عزل$'), unpromote_member))

    db.add_handler(MessageHandler(Filters.group and Filters.regex('^[/!]\s?ارتقا$'), promote_member))


    updater.start_polling()
    updater.idle()

if __name__=="__main__":
    main()
