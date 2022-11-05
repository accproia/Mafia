import logging
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from game import Game
from game_print import GamePrint
from game_play import GamePlay, ButtonPressed, InlineButton, State
from game_config import GameConfig

game_config = GameConfig()

class GameContext:
    def __init__(self):
        self.game = Game()
        self.game_print = GamePrint(self.game)
        self.game_play = GamePlay(self.game, self.game_print)
        self.state = self.game_play.get_first_state()


games = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    
    user = update.effective_user
    game_context = GameContext()
    games[user] = game_context
    state = game_context.state

    (text, reply_markup) = game_process(state)
    await update.message.reply_text(text=text, reply_markup=reply_markup)
    

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query


    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    user = update.effective_user
    if user not in games:
        await query.answer(text="Error")
        return

    game_context = games[user]
    erasable = game_context.state.erasable()
    game_context.state = game_context.state.get_next(ButtonPressed(query.data))
    (text, reply_markup) = game_process(game_context.state)

    if erasable:
        await query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await query.edit_message_text(text=query.message.text, reply_markup=None)
        await query.message.reply_text(text=text, reply_markup=reply_markup)

def convert_buttons(buttons:list) -> list:
    return [InlineKeyboardButton(button.text, callback_data=button.name) for button in buttons]

def convert_buttonlists(buttonlists:list) -> list:
    return [convert_buttons(buttons_list) for buttons_list in buttonlists]

def game_process(state: State) -> tuple[str, any]:
    state.do()
    (text, buttons) = state.print()

    keyboard = []

    if state.is_end():
        pass
    elif buttons is None:
        keyboard = []
    else:
        keyboard = convert_buttonlists(buttons)

    keyboard.append([InlineKeyboardButton("Continue", callback_data="Continue")])

    reply_markup = None if state.is_end() else InlineKeyboardMarkup(keyboard)
    return (text, reply_markup)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Create the Application and pass it your bot's token.
application = Application.builder().token(game_config.bot_token).build()

# on different commands - answer in Telegram
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button))

# Run the bot until the user presses Ctrl-C
application.run_polling()


