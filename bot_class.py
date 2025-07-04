import discord
from discord.ui import Button, View, Modal, TextInput
import configparser

def read_token():
    config = configparser.ConfigParser()
    # Read the .ini file
    config.read('config.ini')
    token = config.get('TOKEN', 'token')
    return token

def read_role():
    config = configparser.ConfigParser()
    # Read the .ini file
    config.read('config.ini')
    role = config.get('ROLE', 'role_id')
    return int(role)

def read_confirmation_channel_id():
    config = configparser.ConfigParser()
    # Read the .ini file
    config.read('config.ini')
    #token = config.get('TOKEN', 'token')
    confirmation_channel_id = int(config.get('CHANNEL', 'confirmation_channel_id'))  # New channel ID for confirmation
    return confirmation_channel_id

def read_color():
    config = configparser.ConfigParser()
    # Read the .ini file
    config.read('config.ini')
    color = config.get('COLOR', 'color')
    return color

def read_welcome_channel_id():
    config = configparser.ConfigParser()
    # Read the .ini file
    config.read('config.ini')
    #token = config.get('TOKEN', 'token')
    welcome_channel_id = int(config.get('CHANNEL', 'welcome_ch_id'))  # New channel ID for confirmation
    return welcome_channel_id



class MyView(View):
    def __init__(self):#edit this
        super().__init__(timeout=None)
        

    @discord.ui.button(label="Member", style=discord.ButtonStyle.primary, custom_id="click_me_button")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        # role = read_role()
        user = interaction.user
        # print(user)
        modal = MyModal(user)
        # await interaction.response.send_message("ส่งข้อมูลให้ผู้ดูแลแล้ว !", ephemeral=True)
        await interaction.response.send_modal(modal)

    # @discord.ui.button(label="PrivateSphx", style=discord.ButtonStyle.primary, custom_id="another_button")
    # async def another_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     user = interaction.user
    #     print(user)
    #     user = interaction.user
    #     # print(user)
    #     modal = MyModal(user)
    #     await interaction.response.send_message("ส่งข้อมูลให้ผู้ดูแลแล้ว !", ephemeral=True)
    #     await interaction.response.send_modal(modal)

        

class confirm(discord.ui.View):

    def __init__(self,user):#edit this
        super().__init__(timeout=None)
        self.user = user#edit this

    @discord.ui.button(label="Add role!", style=discord.ButtonStyle.success, custom_id="click_me_button")
    async def button_callback_add_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = read_role()
        #user = interaction.user
        print(self.user)
        channel = interaction.client.get_channel(read_confirmation_channel_id())
        if channel is None:
            await interaction.response.send_message("Channel not found.")
            return
        
        # await channel.send(
        #     f"Grenda Secret: {self.user.mention} Get Role!"
        # )

        if role not in self.user.roles:
            await self.user.add_roles(self.user.guild.get_role(role))
            # await self.user.send("You have been verified!")
            # await channel.send(f"Grenda Secret: {self.user.mention} got the role!")
            embed = discord.Embed(title = "Bot Notify", 
                        description = f"Role added to {self.user.mention}! ✅",
                        colour=discord.colour.parse_hex_number(read_color())
                        )
            await interaction.response.defer()
            await channel.send(embed=embed)
            #await interaction.response.send_message(f"Role added to {self.user.mention}!", ephemeral=True)
            
        else:
            # embed = discord.Embed(title = "Bot Notify", 
            #             description = f"Admin has decided! ",
            #             colour=discord.colour.parse_hex_number(read_color())
            #             )
            await interaction.response.defer()
            # await channel.send(embed=embed)
            #await interaction.response.send_message(f"{self.user.mention} already has the role.", ephemeral=True)
        
        # await interaction.message.edit(content="Admin has decided", view=None)

        # await interaction.response.send_message(f"Add role to {self.user.mention} complete ! ", ephemeral=True)
        button.disabled = True
        # await interaction.message.edit(view=None)
        await interaction.message.edit(content=f"Admin has decided", view=None)
        

    @discord.ui.button(label="Cancel!", style=discord.ButtonStyle.danger, custom_id="click_me_button2")
    async def button_callback_cencel(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.client.get_channel(read_confirmation_channel_id())
        if channel is None:
            await interaction.response.send_message("Channel not found.")
            return
        
        # await channel.send(
        #     f"Grenda Secret: {self.user.mention} Cancel!"
        # )
        embed = discord.Embed(title = "Bot Notify", 
                        description = f"Add role to {self.user.mention} reject ! ❌",
                        colour=discord.colour.parse_hex_number(read_color())
                        )
        await interaction.response.defer()
        await channel.send(embed=embed)
        # await interaction.response.send_message(f"Add role to {self.user.mention} reject ! ❌", ephemeral=True,)
        button.disabled = True
        # await interaction.message.edit(view=None)
        await interaction.message.edit(content="Admin has decided", view=None)



class MyModal(Modal):
    def __init__(self,user):#edit this

        super().__init__(title="กรอกข้อมูล")
        self.user = user#edit this

        self.name = TextInput(label="ชื่อ", placeholder="Enter your name", required=True)
        self.age = TextInput(label="อายุ", placeholder="Enter your age", required=True)
        self.gender = TextInput(label="เพศ", placeholder="Enter your gender", required=True)
        self.contact = TextInput(label="Link : Facebook/IG", placeholder="Enter your contact", required=True)
        self.who_invite = TextInput(label="ใครเชิญมา", placeholder="Enter who invited you", required=True)

        self.add_item(self.name)
        self.add_item(self.age)
        self.add_item(self.gender)
        self.add_item(self.contact)
        self.add_item(self.who_invite)

    async def on_submit(self, interaction: discord.Interaction):
        channel = interaction.client.get_channel(read_confirmation_channel_id())
        if channel is None:
            await interaction.response.send_message("Channel not found.")
            return
        
        # confirmation_button = Button(label="Confirm Submission", style=discord.ButtonStyle.success, custom_id="confirm_submission")
        # view = View()
        # view.add_item(confirmation_button)
        embed_respone = discord.Embed(title = "User Data", 
                        description = f"Discord: {self.user.mention}\nName: {self.name.value}\nAge: {self.age.value}\nGender: {self.gender.value}\nContact: {self.contact.value}\nWho invited: {self.who_invite.value}",
                        colour=discord.colour.parse_hex_number(read_color())
                        )
        await channel.send(embed=embed_respone
            # f"Discord: {self.user.mention}\nName: {self.name.value}\nAge: {self.age.value}\nGender: {self.gender.value}\nContact: {self.contact.value}\nWho invited: {self.who_invite.value}",
            # # view=view
        )
        await channel.send(view=confirm(self.user))
        # await channel.send(view=Verification(self.user))
        await interaction.response.defer() # hide result
        # await interaction.response.send_message("Your information has been submitted successfully! Please wait for confirmation.") #show result

