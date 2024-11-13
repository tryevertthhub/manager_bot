import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch tokens and keys from environment variables
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Predefined questions and answers
PREDEFINED_QA = {
    "What is Commune AI?": "ACommune AI (COMAI) is a decentralized, permissionless, and composable protocol that aims to connect all developer tools into one network, fostering a more shareable, reusable, and open economy. It follows an inclusive design philosophy, allowing developers to integrate tools seamlessly and leverage the collective knowledge and resources of the community to enhance their projects.",
    "How does Commune AI work?": "AI works by using algorithms and large data sets to identify patterns and make decisions based on learned information.",
    "What is Subnet?": "Machine Learning is a subset of AI that involves training algorithms to learn from and make predictions on data.",
}

class AIChatBot(commands.Bot):
    """
    A Discord bot that allows users to select from predefined questions and receive answers.
    """

    def __init__(self):
        """
        Initializes the bot with required intents, command prefix, and event listeners.
        Sets up bot commands and defines intents for message content.
        """
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="/", intents=intents)

        # Initialize commands and interactions
        self.setup_commands()

    async def on_ready(self):
        """Event that runs when the bot is ready and connected to Discord."""
        print(f"Logged in as {self.user}!")
        await self.tree.sync()

    def setup_commands(self):
        """Registers all bot commands in the command tree."""
        
        # Register the /ask command
        @self.tree.command(name="ask")
        async def ask(interaction: discord.Interaction):
            """Displays a list of questions for the user to select from."""
            await self.ask_command(interaction)

    async def ask_command(self, interaction: discord.Interaction):
        """
        Displays a dropdown list of predefined questions for the user to select.
        """
        options = [discord.SelectOption(label=question) for question in PREDEFINED_QA.keys()]
        select = discord.ui.Select(placeholder="Choose a question...", options=options)
        
        async def select_callback(interaction):
            question = select.values[0]
            answer = PREDEFINED_QA.get(question, "Sorry, I don't have an answer for that question.")
            await interaction.response.send_message(answer, ephemeral=True)

        select.callback = select_callback
        view = discord.ui.View()
        view.add_item(select)
        
        await interaction.response.send_message("Select a question to get an answer:", view=view, ephemeral=True)

# Instantiate and run the bot
def run_discord_bot():
    bot = AIChatBot()
    bot.run(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    run_discord_bot()
