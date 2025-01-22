import requests, sys, time
from colorama import init, Fore

init()

def get_webhook_info(webhook_url):
    try:
        r = requests.get(webhook_url)
        return r.json()
    except:
        return None

def send_webhook_messages(webhook_url, message, amount):
    for i in range(amount):
        requests.post(webhook_url, json={"content": message})
        time.sleep(1)

def decode_snowflake(snowflake):
    timestamp = (int(snowflake) >> 22) + 1420070400000
    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp/1000))

def get_server_info(server_id, bot_token):
    url = f"https://discord.com/api/v9/guilds/{server_id}"
    headers = {"Authorization": f"Bot {bot_token}"}
    r = requests.get(url, headers=headers)
    return r.json()

def main_menu():
    print(Fore.MAGENTA + "Discord Utility")
    print(Fore.MAGENTA + "1) Webhook Tools")
    print(Fore.MAGENTA + "2) Server Info")
    print(Fore.MAGENTA + "3) Exit")
    choice = input(Fore.MAGENTA + "Choose an option: ")
    return choice

def webhook_menu():
    print(Fore.MAGENTA + "1) Get Webhook Info")
    print(Fore.MAGENTA + "2) Send Messages via Webhook")
    print(Fore.MAGENTA + "3) Back")
    choice = input(Fore.MAGENTA + "Choose an option: ")
    return choice

def server_menu():
    print(Fore.MAGENTA + "Enter the server ID, and a bot token with 'guilds' permission.")
    server_id = input(Fore.MAGENTA + "Server ID: ")
    bot_token = input(Fore.MAGENTA + "Bot Token: ")
    info = get_server_info(server_id, bot_token)
    print(Fore.MAGENTA + f"Server Info: {info}")

def run_webhook_tools():
    while True:
        choice = webhook_menu()
        if choice == "1":
            webhook_url = input(Fore.MAGENTA + "Enter the webhook URL: ")
            info = get_webhook_info(webhook_url)
            if info and "id" in info:
                print(Fore.MAGENTA + f"Webhook ID: {info['id']}")
                print(Fore.MAGENTA + f"Channel ID: {info.get('channel_id','Unknown')}")
                print(Fore.MAGENTA + f"Guild ID: {info.get('guild_id','Unknown')}")
                print(Fore.MAGENTA + f"Created At: {decode_snowflake(info['id'])}")
            else:
                print(Fore.MAGENTA + "Invalid or inaccessible webhook.")
        elif choice == "2":
            webhook_url = input(Fore.MAGENTA + "Enter the webhook URL: ")
            msg = input(Fore.MAGENTA + "Enter the message to send: ")
            amt = int(input(Fore.MAGENTA + "How many times to send the message?: "))
            send_webhook_messages(webhook_url, msg, amt)
            print(Fore.MAGENTA + "Messages sent.")
        elif choice == "3":
            break
        else:
            print(Fore.MAGENTA + "Invalid choice.")

def main():
    while True:
        choice = main_menu()
        if choice == "1":
            run_webhook_tools()
        elif choice == "2":
            server_menu()
        elif choice == "3":
            sys.exit(0)
        else:
            print(Fore.MAGENTA + "Invalid choice.")

if __name__ == "__main__":
    main()
