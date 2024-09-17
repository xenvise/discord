import discord
from discord.ext import commands
from discord.ui import Button, View

# Deinen Bot-Token hier einfügen
TOKEN = 'MTI4NTQ0MDMwNDcyMzM5NDcwMQ.G-nodQ.HULdae7TM1VuGqhUgl4WZ3aW6cXT2D21byi87k'

# Bot initialisieren
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Reviews speichern (in-memory, für dauerhaftes Speichern nutze eine Datenbank)
reviews = {}

# Review-Kommando
@bot.command(name="vouch")
async def vouch(ctx, rating: int, *, review_text: str):
    if rating < 1 or rating > 5:
        await ctx.send("Please enter a rating between 1 and 5 stars.")
        return

    # Review speichern
    reviews[ctx.author.id] = {'rating': rating, 'review_text': review_text, 'author': ctx.author.name}

    # Embed-Nachricht erstellen
    embed = discord.Embed(title="Vouch from " + ctx.author.name, description="Xenvise Vouches", color=0xff0000)
    embed.add_field(name="Rating", value="⭐" * rating + "✩" * (5 - rating), inline=False)
    embed.add_field(name="Vouch", value=review_text, inline=False)
    embed.set_thumbnail(url=ctx.author.avatar.url)  # Verwende den Avatar des Benutzers
    embed.set_footer(text=f"ID: {ctx.author.id} • {ctx.message.created_at.strftime('%Y-%m-%d')}")

    # Button zum Review einreichen
    button = Button(label="Submit A Vouch", style=discord.ButtonStyle.primary)
    view = View()
    view.add_item(button)

    await ctx.send(embed=embed, view=view)

   # Lösche die ursprüngliche Nachricht mit dem Befehl
    try:
        await ctx.message.delete()
    except discord.NotFound:
        pass  # Nachricht wurde bereits gelöscht oder konnte nicht gefunden werden

# Nachrichten löschen-Kommando
@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, limit: int):
    if limit <= 0:
        await ctx.send("Please provide a positive number of messages to delete.")
        return
    
    deleted = await ctx.channel.purge(limit=limit)
    await ctx.send(f"Deleted {len(deleted)} messages.", delete_after=5)

# Fehlerbehandlung, wenn der Benutzer nicht die erforderlichen Berechtigungen hat
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to manage messages.")

# Bot starten
bot.run(TOKEN)
