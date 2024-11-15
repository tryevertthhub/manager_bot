import discord
from discord.ext import commands
import aiohttp
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
AI_BASE_URL = "https://openrouter.ai/api/v1"

class AIChatBot(commands.Bot):
    """
    A Discord bot that uses OpenRouter AI to generate answers to user questions.
    """

    def __init__(self):
        """
        Initializes the bot with required intents and commands.
        """
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="/", intents=intents)
        self.setup_commands()

    async def on_ready(self):
        """Runs when the bot is ready."""
        print(f"Logged in as {self.user}!")
        await self.tree.sync()

    def setup_commands(self):
        """Registers the /ask command."""
        @self.tree.command(name="ask")
        async def ask(interaction: discord.Interaction, question: str):
            """
            Handles the /ask command by sending the question to OpenRouter AI.
            
            Args:
                interaction (discord.Interaction): The interaction object.
                question (str): The question asked by the user.
            """
            await interaction.response.defer(ephemeral=False)
            ai_response = await self.fetch_ai_response(question)
            await interaction.followup.send(ai_response)

    async def fetch_ai_response(self, question: str) -> str:
        """
        Sends the question to OpenRouter AI and retrieves the response.

        Args:
            question (str): The user's question.

        Returns:
            str: The response from OpenRouter AI, or an error message.
        """
        headers = {
            "Authorization": f"Bearer {OPEN_ROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "openai/gpt-4",
            "prompt": question,
            "max_tokens": 1000,
            "temperature": 1.0,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(f"{AI_BASE_URL}/completions", headers=headers, json=data) as response:
                if response.status == 200:
                    response_data = await response.json()
                    return response_data["choices"][0]["text"].strip()
                else:
                    error_message = await response.text()
                    print(f"HTTP error {response.status}: {error_message}")
                    return "Failed to fetch AI response. Please try again later."

# Instantiate and run the bot
def run_discord_bot():
    bot = AIChatBot()
    bot.run(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    run_discord_bot()
