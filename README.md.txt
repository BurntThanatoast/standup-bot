# Discord Standup Automator

A lightweight, AI-powered Discord bot that transforms messy "braindump" notes into professional daily standup reports. Built to help developers maintain communication, identify blockers early, and keep standups concise.

## How it Works
1. Users type `!standup` followed by their daily notes into Discord.
2. The bot sends the notes to a Large Language Model (Llama 3.1 via Groq API).
3. The AI formats the input into three professional categories: **What I did yesterday**, **What I am doing today**, and **Blockers**.

## Tech Stack
- **Language:** Python
- **API Integration:** Groq (Meta Llama 3.1) & Discord.py
- **Environment Management:** Python venv
- **Deployment Strategy:** Local host (ready for containerization)

## How to run it
1. Clone this repository.
2. Create a `.env` file and add your `DISCORD_TOKEN` and `GROQ_API_KEY`.
3. Install requirements: `pip install -r requirements.txt` (Note: run `pip freeze > requirements.txt` in your terminal to generate this file first!)
4. Run the bot: `python bot.py`