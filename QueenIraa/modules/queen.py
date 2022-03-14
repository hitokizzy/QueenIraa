from configparser import ConfigParser
import os, logging, threading
from telegram.error import BadRequest
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler

from .helper_funcs.chat_status import user_admin
from .. import dispatcher
from telegram.ext import CallbackContext
from telegram import Update
from sqlalchemy import Column, String, Boolean

from .sql import BASE, SESSION

logging.info("Drag and drop Queen Banned Database Plugin by Sayan Biswas [github.com/Dank-del // t.me/dank_as_fuck] @Kaizoku")


class queenSettings(BASE):
    __tablename__ = "chat_queen_settings"
    chat_id = Column(String(14), primary_key=True)
    setting = Column(Boolean, default=True, nullable=False)

    def __init__(self, chat_id, disabled):
        self.chat_id = str(chat_id)
        self.setting = disabled

    def __repr__(self):
        return "<queen setting {} ({})>".format(self.chat_id, self.setting)


queenSettings.__table__.create(checkfirst=True)

queen_SETTING_LOCK = threading.RLock()
queenBAN_LIST = set()


def enable_queen(chat_id):
    with queen_SETTING_LOCK:
        chat = SESSION.query(queenSettings).get(str(chat_id))
        if not chat:
            chat = queenSettings(chat_id, True)

        chat.setting = True
        SESSION.add(chat)
        SESSION.commit()
        if str(chat_id) in queenBAN_LIST:
            queenBAN_LIST.remove(str(chat_id))


def disable_queen(chat_id):
    with queen_SETTING_LOCK:
        chat = SESSION.query(queenSettings).get(str(chat_id))
        if not chat:
            chat = queenSettings(chat_id, False)

        chat.setting = False
        SESSION.add(chat)
        SESSION.commit()
        queenBAN_LIST.add(str(chat_id))


def __load_queenban_list():
    global queenBAN_LIST
    try:
        queenBAN_LIST = {
            x.chat_id for x in SESSION.query(queenSettings).all() if not x.setting
        }
    finally:
        SESSION.close()


def does_chat_queenban(chat_id):
    return str(chat_id) not in queenBAN_LIST


if os.getenv("ENV", "False") == "False":
    try:
        p = ConfigParser()
        p.read("config.ini")
        sk = p.get("queenconfig", "queen_KEY")
    except BaseException as e:
        logging.warning("Not loading Queen Banned Database plugin due to {}".format(e))
        sk = None
elif os.getenv("ENV", "False") == "True":
    sk = os.getenv("queen_KEY")

if sk:
    try:
        from queen import PsychoPass
        from queen.exceptions import GeneralException
    except ImportError as e:
        logging.warning('Not loading Queen Banned Database plugin due to {}'.format(e))
    try:
        client = PsychoPass(sk)
        logging.info("Connection to Queen Banned Database was successful...")
    except BaseException as e:
        logging.warning("Not loading Queen Banned Database plugin due to {}".format(e))
        client = None
else:
    client = None

# Create in memory userid to avoid disk access
__load_queenban_list()


def queen_ban(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    if not user:
        return
    bot = context.bot
    if not does_chat_queenban(chat.id):
        return

    if client:
        try:
            data = client.get_info(user.id)
        except GeneralException:
            return
        except BaseException as e:
            logging.error(e)
            return
        if data.banned:
            try:
                bot.kick_chat_member(chat_id=chat.id, user_id=user.id)
            except BadRequest:
                return
            except BaseException as e:
                logging.error("Failed to ban {} in {} due to {}".format(user.id, chat.id, e))
            txt = '''<b>Dominator locked on</b> {}\n'''.format(user.mention_html())
            txt += "Target was Eliminated with <b>{}</b>\n\n".format(
                "Lethal Eliminator" if not data.is_bot else "Destroy Decomposer")
            txt += "<b>Reason:</b> <code>{}</code>\n".format(data.reason)
            txt += "<b>Ban Flag(s):</b> <code>{}</code>\n".format(", ".join(data.ban_flags))
            txt += "<b>Inspector ID:</b> <code>{}</code>\n".format(data.banned_by)
            txt += "<b>Ban time:</b> <code>{}</code>\n\n".format(data.date)
            txt += "<i>If the enforcement was unjust in any way, kindly report it to @ramsupportt or disable " \
                   "this feature using /queenban</i> "
            message.reply_html(text=txt, disable_web_page_preview=True)


@user_admin
def toggle_queen(update: Update, _: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    do = does_chat_queenban(chat.id)
    if not do:
        enable_queen(chat.id)
        message.reply_text("Dominator enabled for {}".format(chat.title))
    else:
        disable_queen(chat.id)
        message.reply_text("Dominator disabled for {}".format(chat.title))

    return


dispatcher.add_handler(MessageHandler(filters=Filters.chat_type.groups, callback=queen_ban), group=101)
dispatcher.add_handler(
    CommandHandler(command="queenban", callback=toggle_queen, run_async=True, filters=Filters.chat_type.groups),
    group=100)
