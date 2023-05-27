from aiogram import Bot
from aiogram.types import BotCommand,BotCommandScopeDefault


async def set_default_commands(bot: Bot):
    commands = ([
        BotCommand(command="start",
                   description= "Запустить бота"),
        BotCommand(command="card",
                   description="Карта лояльности")
    ])

    await bot.set_my_commands(commands,
                              BotCommandScopeDefault())