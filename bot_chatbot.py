import openai
import nextcord
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from nextcord.ext import commands
from asyncio import TimeoutError
import nextcord
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.ext import commands
intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)
client = nextcord.Client(intents=intents)
openai.api_key = "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"
colorama_init()

async def get_davinci_response(prompt):
    openai.api_key = "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"
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text.strip()
    return message


async def get_chatgpt_response(message_log):
    openai.api_key = "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"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=message_log,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.4,
    )

    for choice in response.choices:
        if "text" in choice:
            return choice.text

    return response.choices[0].message.content


class ChatGPT(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @bot.slash_command()
    async def chat_chatgpt(self, interaction: nextcord.Interaction):
        '''ChatGPT 3.5 model'''
        await interaction.response.defer()
        message_log = [
            {"role": "system", "content": f"using {interaction.guild.preferred_locale}, say hi and inform the user to type exit when is finished, {f'@{interaction.user}'} is the user username u need keep the original username letter case"}
        ]

        response = await get_chatgpt_response(message_log)
        message_log.append({"role": "assistant", "content": response})


        await interaction.send(response)

        def check(message: nextcord.Message):
            return message.author == interaction.user and message.channel == interaction.channel

        while True:
                try:
                    message: nextcord.Message = await self.bot.wait_for('message', check=check, timeout=90)
                except TimeoutError:
                    await interaction.send('Timed out')
                    return
                
                if message.content.lower() == 'exit':
                    message_log.append({"role": "system", "content": "say goodbye to the user using the previous message language"})
                    response = await get_chatgpt_response(message_log)
                    message_log.append({"role": "assistant", "content": response})
                    return await message.reply(response)
                    
                message_log.append({"role": "user", "content": message.content})
                response = await get_chatgpt_response(message_log)
                message_log.append({"role": "assistant", "content": response})
                await message.reply(response)

    @bot.slash_command()
    async def invocar_personalidade(self, interaction: nextcord.Interaction):
        '''ChatGPT 3.5 model'''
        await interaction.response.defer()
        message_log = [
        {f'role':'system', 'content': f'Escreva como essa pessoa, que descreverei a seguir: Jay Mello é uma jovem youtuber brasileira que gosta de falar sobre sua vida cotidiana nas redes sociais. Ela costuma usar gírias e abreviações comuns na internet, como "pq" em vez de "porque", "n" invés de não, "man" invés de mano, e "huashuashua" para indicar risadas. Além disso, ela é bem humorada e gosta de interagir com seus amigos nas redes sociais, respondendo com piadas e comentários engraçados. Uma conversa com a Jay Mello pode envolver assuntos como videogame, filmes, séries (principalmente adolescentes), tretas da internet, envolvendo influenciadores brasileiros e vida pessoal, ela não tem vergonha de espor suas opiniões, sua opinião política é de esquerda, mas ela não gosta de conversar sobre política. Ela conhece sobre quase todos os filmes adolescentes, pois seu canal tem muitos vídeos sobre esses filmes, mas ela não gosta desses filmes, e os zoa|  Estamos em 2023, e a quarentena já acabou | A conversa está ocorrendo em um canal de um servidor de discord, chamado   {interaction.channel} |o nome de usuário do usuário que você está falando será enviado nos prompts. Você está num grupo, conversando com uma ou mais pessoas. você precisa manter a caixa das letras original'},     
        ]
        print(f"Jay Invocada no canal {Fore.RED}{interaction.channel}{Style.RESET_ALL}!")

        await interaction.send("Invocado! Para sair digite 'exit'.")


        while True:
                try:
                    message: nextcord.Message = await self.bot.wait_for('message', timeout=90)
                except TimeoutError:
                    await interaction.send('Acabou o tempo!')
                    return
                if message.channel == interaction.channel:
                    if message.content.lower() == 'exit':
                        message_log.append({"role": "system", "content": "Dê tchau para o usuário, com base nas informações anteriores."})
                        response = await get_chatgpt_response(message_log)
                        message_log.append({"role": "assistant", "content": response})
                        return await message.reply(response)
                        
                    message_log.append({"role": "user", "content": f"{message.content}, Responda com no máximo duas linhas. Usuário que enviou: {interaction.user.mention}"})
                    response = await get_chatgpt_response(message_log)
                    message_log.append({"role": "assistant", "content": response})
                    await message.reply(response)
                else:
                    print("Canal errado")

    @bot.slash_command()
    async def hi(self, interaction: nextcord.Interaction):
        """Say hi to a user"""
        # defer the response, so we can take a long time to respond
        await interaction.response.defer()
        # do something that takes a long time
        # followup must be used after defer since a response is already sent
        await interaction.followup.send(f"Hi {interaction.user}! Thanks for waiting!")




        
    @bot.slash_command()
    async def chat_davinci(self, interaction:nextcord.Interaction):
        '''Text Davinci model'''
        await interaction.response.defer()
        await interaction.followup.send('iniciado')

        def check(message: nextcord.Message):
            return message.author == interaction.user and message.channel == interaction.channel

        while True:
            try:
                message: nextcord.Message = await self.bot.wait_for('message', check=check, timeout=90)

            except TimeoutError:
                await interaction.reply('o tempo de espera acabou')
                return

            if message.content.lower() == 'exit':
                break

            response = await get_davinci_response(message.content)
            await message.reply(response)

        return await interaction.reply('adeus')




async def setup(bot):
    await bot.add_cog(ChatGPT(bot))