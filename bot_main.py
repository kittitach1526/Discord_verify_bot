import discord
from discord.ext import commands
from bot_class import MyView,read_token,read_color,read_welcome_channel_id

intents = discord.Intents.all()
# intents.message_content = True

bot = commands.Bot(command_prefix=">", intents=intents)

@bot.event
async def on_ready():
    print(f'Version 1.1(welcome update) Logged in as {bot.user}')


@bot.event
async def on_member_join(member):
    # หาแชนแนลที่ต้องการส่งข้อความต้อนรับ
    # channel = interaction.client.get_channel(read_confirmation_channel_id())
    # channel = discord.utils.get(member.guild.channels, name='general')  # เปลี่ยน 'general' เป็นชื่อแชนแนลที่ต้องการ
    channel = bot.get_channel(read_welcome_channel_id)    
    if channel:
        embed = discord.Embed(title = "WELCOME !!!!", 
                        description = f"ยินดีต้อนรับ {member.mention} เข้าสู่เซิร์ฟเวอร์!.\nรบกวนไปยืนยันตัวตนด้วยน้าา ><",
                        colour=discord.colour.parse_hex_number(read_color())
                        )
        await channel.send(embed=embed)

@bot.command()
async def button(ctx):
    # user_mention = ctx.author.mention #ดึงข้อมูลของคนกด
    view = MyView()
    embed = discord.Embed(title = "Verification", 
                        description = "Click below to verify.",
                        colour=discord.colour.parse_hex_number(read_color())
                        )
    await ctx.send(embed = embed,view=view)
    # await ctx.send("Here is a button:", view=view)

bot.run(read_token())
