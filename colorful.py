from colorama import Fore, Back, Style

print(Fore.RED + "This text is red!")
print(Fore.GREEN + "This text is green!")
print(Back.YELLOW + "This has a yellow background!")
print(Fore.BLUE + "This text is blue!")
print(Fore.WHITE + Back.BLUE + "This is white text on blue background!")
print(Style.RESET_ALL + "Back to normal")