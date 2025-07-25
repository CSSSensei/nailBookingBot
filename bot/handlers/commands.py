from aiogram.types import Message

from bot.keyboards import user_keyboards
from bot.routers import UserRouter, BaseRouter
from config import Config, load_config
from phrases import PHRASES_RU

router = UserRouter()
config: Config = load_config()


@router.command('start')                                                               # /start
async def process_start_command(message: Message):
    await message.answer(PHRASES_RU.commands.start, reply_markup=user_keyboards.keyboard)


@router.command('help', 'как пользоваться ботом')                   # /help
async def process_help_command(message: Message):
    await message.answer(PHRASES_RU.commands.help, reply_markup=user_keyboards.keyboard)


@router.command('about', 'о разработчиках')                         # /about
async def process_about_command(message: Message):
    await message.answer(PHRASES_RU.commands.about, reply_markup=user_keyboards.keyboard)


@router.command('commands', 'список всех команд (это сообщение)')   # /commands
async def process_commands_command(message: Message):
    commands_text = '\n'.join(str(command) for command in BaseRouter.available_commands if not command.is_admin)
    await message.answer(PHRASES_RU.title.commands + commands_text, reply_markup=user_keyboards.keyboard)
