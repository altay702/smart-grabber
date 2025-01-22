import os
import ast
import astor
import random
import string
import pyperclip
from base64 import b64encode
from colorama import init, Fore, Style
import ctypes

# Initialize colorama
init(autoreset=True)

def generate_random_string(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class CodeObfuscator(ast.NodeTransformer):
    def __init__(self):
        self.variable_map = {}
        self.function_map = {}

    def obfuscate_name(self, name):
        if name not in self.variable_map:
            self.variable_map[name] = generate_random_string()
        return self.variable_map[name]

    def visit_FunctionDef(self, node):
        if node.name not in self.function_map:
            self.function_map[node.name] = generate_random_string()
        node.name = self.function_map[node.name]
        node.args.args = [
            ast.arg(arg=self.obfuscate_name(arg.arg), annotation=arg.annotation)
            for arg in node.args.args
        ]
        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Load, ast.Store, ast.Del)):
            if node.id in self.variable_map:
                node.id = self.variable_map[node.id]
        return node

    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name):
            node.targets[0].id = self.obfuscate_name(node.targets[0].id)
        self.generic_visit(node)
        return node

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in self.function_map:
                node.func.id = self.function_map[node.func.id]
        self.generic_visit(node)
        return node

def obfuscate_code(source_code):
    try:
        tree = ast.parse(source_code)
        obfuscator = CodeObfuscator()
        obfuscated_tree = obfuscator.visit(tree)
        obfuscated_code = astor.to_source(obfuscated_tree)
        encoded_code = b64encode(obfuscated_code.encode('utf-8')).decode('utf-8')
        final_code = f"import base64\nexec(base64.b64decode('{encoded_code}').decode('utf-8'))"
        return final_code
    except Exception as e:
        return f"Error obfuscating code: {e}"

def main():
    ctypes.windll.kernel32.SetConsoleTitleW("Python Code Obfuscator")

    print(Fore.CYAN + Style.BRIGHT + "=" * 50)
    print(Fore.MAGENTA + Style.BRIGHT + "   Python Code Obfuscator - Terminal Edition")
    print(Fore.CYAN + Style.BRIGHT + "=" * 50 + "\n")

    print(Fore.YELLOW + Style.BRIGHT + "Paste your Python code below. Press Enter twice to finish:")
    source_code_lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        source_code_lines.append(line)
    source_code = "\n".join(source_code_lines)

    if not source_code.strip():
        print(Fore.RED + "No code provided. Exiting...")
        return

    print(Fore.CYAN + "\nObfuscating code...")
    obfuscated_code = obfuscate_code(source_code)

    print(Fore.GREEN + "\nObfuscated Code:")
    print(Fore.BLUE + Style.BRIGHT + obfuscated_code + "\n")

    # Auto-copy to clipboard
    pyperclip.copy(obfuscated_code)
    print(Fore.YELLOW + Style.BRIGHT + "The obfuscated code has been copied to the clipboard automatically.\n")

    # Offer manual copy
    print(Fore.CYAN + "If you want to manually copy the output again, type 'y' and press Enter.")
    manual_copy = input(Fore.MAGENTA + "Copy manually? (y/n): ").strip().lower()
    if manual_copy == 'y':
        pyperclip.copy(obfuscated_code)
        print(Fore.GREEN + "Output copied to clipboard manually!")

    print(Fore.CYAN + Style.BRIGHT + "\nThank you for using the Python Code Obfuscator!")
    print(Fore.CYAN + "=" * 50)

if __name__ == "__main__":
    main()
