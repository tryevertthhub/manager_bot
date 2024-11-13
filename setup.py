from setuptools import setup, find_packages

setup(
    name="my_discord_bot",
    version="0.1",
    description="A Discord bot for interacting with predefined questions and answers",
    author="Your Name",
    author_email="tryevertth@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "discord.py",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "my_discord_bot=manager_bot.bot:run_discord_bot"
        ]
    },
)
