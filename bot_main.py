import discord
from discord.ext import commands
from bot_class import MyView,read_token,read_color,read_welcome_channel_id
from ticket_system import *

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

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    channel_name = message.channel.name

    # ตรวจว่าเป็น ticket หรือไม่
    is_ticket_channel = channel_name.startswith("ticket-")

    # เลือกโฟลเดอร์
    log_folder_path = "ticket_logs" if is_ticket_channel else "chat_logs"

    # สร้างโฟลเดอร์ถ้ายังไม่มี
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)

    # ตั้งชื่อไฟล์ log
    log_file_name = f"{channel_name}.txt"
    log_path = os.path.join(log_folder_path, log_file_name)

    # เขียน log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if message.attachments:
        files = ", ".join(att.filename for att in message.attachments)
        log_msg = f"[{timestamp}] {message.author} ({message.author.id}): [ไฟล์แนบ] {files}\n"
    else:
        log_msg = f"[{timestamp}] {message.author} ({message.author.id}): {message.content}\n"

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(log_msg)

    await bot.process_commands(message)


@bot.command()
async def sendticket(ctx):
    view = TicketButton()
    await ctx.send("🎫 กดปุ่มด้านล่างเพื่อเปิด Ticket", view=view)



bot.run(read_token())
