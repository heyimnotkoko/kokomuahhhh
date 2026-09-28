import asyncio
import importlib

from pyrogram import idle

import KroMusic as fm
from KroMusic.Modules import ALL_MODULES


async def run():
    await fm.fallen_startup()

    fm.LOGGER.info("Loading modules...")
    for module in ALL_MODULES:
        importlib.import_module("KroMusic.Modules." + module)
    fm.LOGGER.info("Loaded %s modules.", len(ALL_MODULES))

    await idle()


if __name__ == "__main__":
    asyncio.run(run())
