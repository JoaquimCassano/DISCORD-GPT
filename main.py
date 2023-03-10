import nextcord
from nextcord.ext import commands, menus
from nextcord import Embed
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from bot_chatbot import ChatGPT
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
token = "TOKEN DO BOT"

colorama_init()
intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)
client = nextcord.Client(intents=intents)


@bot.event
async def on_ready():
    print("Bot Online!")
    print(f"Logado usando o token {Fore.GREEN}{token}{Style.RESET_ALL}!")

    

@bot.slash_command()
async def convidar(interaction: nextcord.Interaction):  #Comando que cria um Embed de convite para o servidor
    """Convida o bot para um servidor!"""
    embed=nextcord.Embed(title="Convidar", url="https://link_do_convite_do_bot.com") #Troca isso
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/755769311775162468/1078103302404853860/Apenas_um_nerd_make_a_armadillo_in_this_style_2dbc8642-c046-49c5-9d3d-22201b134b13.png")
    embed.add_field(name="Clique para adicionar o bot ao servidor!", value="", inline=False)
    await interaction.send(embed=embed)


bot.add_cog(ChatGPT(bot))

bot.run(token)