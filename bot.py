import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Slash commands synced.")

@bot.tree.command(name="training", description="Send a LAFD & EMS training ping embed")
@app_commands.describe(
    time="Time of the training (e.g. 7:00 PM EST)",
    date="Date of the training (e.g. 05/28/25)",
    location="Location (e.g. Pillbox)",
    requirements="Requirements (e.g. radio, uniform, etc.)"
)
async def training(
    interaction: discord.Interaction,
    time: str,
    date: str,
    location: str,
    requirements: str
):
    # ✅ Only these users can run the command (e.g. FTOs)
    allowed_role_id =  # FTO role ID
    # ✅ This role will be pinged in the message (e.g. Needs Training)
    pinged_role_id =    # Needs Training role ID

    # Check if the user has permission
    if allowed_role_id not in [role.id for role in interaction.user.roles]:
        await interaction.response.send_message(
            "❌ You do not have permission to use this command.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="📣 Department Training",
        description="A mandatory training session is being held. Please ensure your attendance if you're able.",
        color=discord.Color.red()
    )
    embed.add_field(name="🕒 Time", value=time, inline=False)
    embed.add_field(name="📅 Date", value=date, inline=False)
    embed.add_field(name="📍 Location", value=location, inline=False)
    embed.add_field(name="📘 Requirements", value=requirements, inline=False)
    embed.add_field(
        name="🔗 Notes",
        value="Failure to attend may result in disciplinary action unless excused. Contact a supervisor for exemptions.",
        inline=False
    )
    embed.set_footer(text="Los Angeles Fire Department & EMS")
    embed.timestamp = discord.utils.utcnow()

    # Pinged role
    role_mention = f"<@&{pinged_role_id}>"

    await interaction.response.send_message(
        content=f"🚨 {role_mention} — Training Notice 🚨",
        embed=embed,
        allowed_mentions=discord.AllowedMentions(roles=True)  # <-- This allows the role to be pinged
    )

    message = await interaction.original_response()
    await message.add_reaction("✅")
    await message.add_reaction("❌")

bot.run("YOUR BOT TOKEN HERE") # The bot will not work if you do not place your bot token!!!

# To get the bot running place this into the terminal python bot.py
