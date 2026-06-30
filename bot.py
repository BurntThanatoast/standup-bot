import os
import discord
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load your secure tokens from the .env file
load_dotenv()

# 2. Initialize the OpenAI client
# Old: openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
# New:
openai_client = OpenAI(
    api_key=os.getenv('GROQ_API_KEY'),
    base_url="https://api.groq.com/openai/v1"
)

# 3. Set up Discord permissions (Intents) so the bot can read messages
intents = discord.Intents.default()
intents.message_content = True
discord_client = discord.Client(intents=intents)

# 4. Event: What to do when the bot turns on
@discord_client.event
async def on_ready():
    print(f'Success! We have logged in as {discord_client.user}')

# 5. Event: What to do when a message is sent in the server
@discord_client.event
async def on_message(message):
    # Ignore messages sent by the bot itself to prevent infinite loops
    if message.author == discord_client.user:
        return

    # Listen for our specific trigger command: "!standup"
    if message.content.startswith('!standup'):
        # Grab the messy text the user typed after the command
        raw_notes = message.content.replace('!standup', '').strip()
        
        # If they just typed "!standup" with no notes, prompt them
        if not raw_notes:
            await message.channel.send("Please provide some notes! Example: `!standup fixed the login bug, going to work on the database today, no blockers.`")
            return

        # Let the user know the bot received the command
        await message.channel.send("Formatting your standup...")

        try:
            # Send the messy notes to OpenAI with strict formatting instructions
            response = openai_client.chat.completions.create(
                # Old: model="gpt-4o-mini",
                # New:
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are an engineering assistant. The user will give you a messy brain dump of their day. Format it into a professional daily standup report using exactly three bulleted categories: **What I did yesterday**, **What I am doing today**, and **Blockers**. Keep it concise, professional, and fix any grammar mistakes."},
                    {"role": "user", "content": raw_notes}
                ]
            )
            
            clean_standup = response.choices[0].message.content
            
            # Send the final formatted text back to Discord
            await message.channel.send(clean_standup)

        except Exception as e:
            # Good engineering practice: handle errors gracefully so the bot doesn't crash
            await message.channel.send("Oops, something went wrong connecting to OpenAI.")
            print(f"Error: {e}")

# Start the bot
discord_client.run(os.getenv('DISCORD_TOKEN'))