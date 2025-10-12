from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import requests
import psutil

BOT_TOKEN = "7977196875:AAEQSb_uHW1XJma49sN4CdaMB1YuBJtjqMo"

# ----- Server / Provider Info -----
def detect_provider_env():
    if os.getenv("KOYEB_APP_ID"):
        return "Koyeb"
    elif os.getenv("RAILWAY_PROJECT_ID"):
        return "Railway"
    elif os.getenv("RENDER_SERVICE_ID"):
        return "Render"
    elif os.getenv("HEROKU_APP_NAME"):
        return "Heroku"
    elif os.getenv("VERCEL"):
        return "Vercel"
    return None

def detect_provider_ip():
    try:
        ip = requests.get("https://api.ipify.org").text
        data = requests.get(f"https://ipinfo.io/{ip}/json").json()
        org = data.get("org", "Unknown Provider")
        city = data.get("city", "")
        country = data.get("country", "")
        return f"{org} ({city}, {country})"
    except:
        return "Unknown Provider"

def get_server_info():
    provider = detect_provider_env()
    if provider:
        try:
            ip = requests.get("https://api.ipify.org").text
            data = requests.get(f"https://ipinfo.io/{ip}/json").json()
            city = data.get("city", "")
            country = data.get("country", "")
            return f"{provider} ({city}, {country})"
        except:
            return provider
    else:
        return detect_provider_ip()

# ----- System Stats -----
def get_system_stats():
    cpu_percent = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    ram_total = round(ram.total / (1024*1024*1024), 2)
    ram_used = round(ram.used / (1024*1024*1024), 2)
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    disk_total = round(disk.total / (1024*1024*1024), 2)
    disk_used = round(disk.used / (1024*1024*1024), 2)

    try:
        load_avg = os.getloadavg()
        load_text = f"{load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}"
    except:
        load_text = "N/A"

    return (
        f"💻 CPU Usage: {cpu_percent}%\n"
        f"🧠 RAM Usage: {ram_used}GB / {ram_total}GB ({ram_percent}%)\n"
        f"💾 Disk Usage: {disk_used}GB / {disk_total}GB ({disk_percent}%)\n"
        f"📊 Load Average (1,5,15 min): {load_text}"
    )

# ----- Bot Command -----
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    server_info = get_server_info()
    system_stats = get_system_stats()
    await update.message.reply_text(f"🌐 Current Server: {server_info}\n\n{system_stats}")

# ----- Run Bot -----
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("info", info))
    print("Bot is running...")
    app.run_polling()
