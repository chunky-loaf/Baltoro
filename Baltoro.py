import random as r 
import os
import time
import math 
import string 


logo = r"""
         ____        _ _ 
        |  _ \      | | |
        | |_) | __ _| | |_ ___  _ __ ___ 
        |  _ < / _` | | __/ _ \| '__/ _ \ 
        | |_) | (_| | | || (_) | | | (_) |
        |____/ \__,_|_|\__\___/|_|  \___/ 
     𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵
"""
colours = {
    "default": '\033[0m',
    "purple": '\033[95m',
    "cyan": '\033[96m',
    "blue": '\033[94m',
    "green": '\033[92m',
    "yellow": '\033[93m',
    "red": '\033[91m'
}

inputMethod = 1
cardStyle = 1
textType = None
gameSpeed = 0.1


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def text_scroll(text, delay, isLogo=False):
    global textType, colours
    if textType:
        display_text = ""
        for character in text:
            clear()
            if isLogo:
                print(logo)
            display_text += character
            print(colours[textType] + display_text + "\033[0m")
            time.sleep(delay)
    else:
        display_text = ""
        for character in text:
            clear()
            if isLogo:
                print(logo)
            display_text += character
            print(display_text)
            time.sleep(delay)


def loading_screen():
    display_text = ""
    for char in "Loading Pr":
        clear()
        display_text += char
        print(display_text)
        time.sleep(0.15)
    for char in "ogram: Baltoro":
        clear()
        display_text += char
        print(display_text)
        time.sleep(0.05)
    clear()
    print(display_text + "\n [■□□□□□□□□□] 10%")
    time.sleep(r.uniform(0.2, 0.5))
    clear()
    print(display_text + "\n [■■□□□□□□□□] 20%")
    time.sleep(r.uniform(0.2, 0.5))
    clear()
    print(display_text + "\n [■■■□□□□□□□] 30%")
    time.sleep(r.uniform(0.2, 0.5))
    clear()
    print(display_text + "\n [■■■■□□□□□□] 40%")
    time.sleep(r.uniform(0.2, 0.5))
    clear()
    print(display_text + "\n [■■■■■□□□□□] 50%")
    time.sleep(r.uniform(0.2, 0.5))
    clear()
    print(display_text + "\n [■■■■■■□□□□] 60%")
    time.sleep(r.uniform(0.2, 0.5))
    clear()
    print(display_text + "\n [■■■■■■■□□□] 70%")
    time.sleep(r.uniform(0.2, 0.5))
    clear()
    print(display_text + "\n [■■■■■■■■□□] 80%")
    time.sleep(r.uniform(0.2, 0.5))
    clear()
    print(display_text + "\n [■■■■■■■■■□] 90%")
    time.sleep(r.uniform(0.2, 0.5))
    clear()
    print(display_text + "\n [■■■■■■■■■■] 100%")
    time.sleep(2)
        

def menu():
    global inputMethod, cardStyle, textType, gameSpeed
    while True:

        clear()
        text_scroll(r"""
Menu:

1) Credits
2) Customise Deck
3) Settings
                
4) Back""", gameSpeed)
        choice = input().lower()

        if choice in ["1", "credits", "credit", "c"]:
            while True:
                clear()
                text_scroll(r"""
Credits:

Directed by Me
Curated by Me
Co-Owned by ChatGPT
Developed by Me in association with OpenAI

1) Back""", gameSpeed)
                choice = input().lower()

                if choice in ["1", "back", "b"]:
                    break
                else:
                    text_scroll("(INVALID SELECTION!)", gameSpeed)
                    time.sleep(2)
            continue

        elif choice in ["2", "customise deck", "customise", "deck", "c", "d"]:
            while True:
                clear()
                text_scroll(r"""
Customise Deck:

1) AS KH QD JC 10S 9H 8D 7S (Default)
2) A♠ K♥ Q♣ J♦ 10♤ 9♡ 8♧ 7♢ (Recommended)

3) Back""", gameSpeed)
                choice = input().lower()

                if choice in ["1", "default", "d"]:
                    cardStyle = 1
                    break
                elif choice in ["2", "recommended", "recommened", "r"]:
                    cardStyle = 2
                    break
                elif choice in ["3", "back", "b"]:
                    break
                else:
                    text_scroll("(INVALID SELECTION!)", gameSpeed)
                    time.sleep(2)
            continue

        elif choice in ["3", "settings", "setting", "s"]:
            while True:
                clear()
                text_scroll(r"""
Settings:

1) Graphics
2) Game

3) Back""", gameSpeed)
                choice = input().lower()
                if choice in ["1", "graphics", "graphic"]:
                    while True:
                        clear()
                        text_scroll(f"""
\033[0mGraphics Options:\033[0m
                                    
\033[0m1) Text Appears As Normal\033[0m
{colours["purple"]}2) Text Appears As Purple\033[0m
{colours["cyan"]}3) Text Appears As Cyan\033[0m
{colours["blue"]}4) Text Appears As Blue\033[0m
{colours["green"]}5) Text Appears As Green\033[0m
{colours["yellow"]}6) Text Appears As Yellow\033[0m
{colours["red"]}7) Text Appears As Red\033[0m\n
8) Back""", gameSpeed)

                        choice = input().lower()

                        if choice in ["1", "default", "d"]:
                            textType = "default"
                            clear()
                            text_scroll("Text Type set to Default", gameSpeed)
                            time.sleep(0.5)
                            break
                        elif choice in ["2", "purple", "p"]:
                            textType = "purple"
                            clear()
                            text_scroll("Text Type set to Purple", gameSpeed)
                            time.sleep(0.5)
                            break
                        elif choice in ["3", "cyan", "c"]:
                            textType = "cyan"
                            clear()
                            text_scroll("Text Type set to Cyan", gameSpeed)
                            time.sleep(0.5)
                            break
                        elif choice in ["4", "blue", "bl"]:
                            textType = "blue"
                            clear()
                            text_scroll("Text Type set to Blue", gameSpeed)
                            time.sleep(0.5)
                            break
                        elif choice in ["5", "green", "g"]:
                            textType = "green"
                            clear()
                            text_scroll("Text Type set to Green", gameSpeed)
                            time.sleep(0.5)
                            break
                        elif choice in ["6", "yellow", "y"]:
                            textType = "yellow"
                            clear()
                            text_scroll("Text Type set to Yellow", gameSpeed)
                            time.sleep(0.5)
                            break
                        elif choice in ["7", "red", "r"]:
                            textType = "red"
                            clear()
                            text_scroll("Text Type set to Red", gameSpeed)
                            time.sleep(0.5)
                            break
                        elif choice in ["8", "back", "b"]: 
                            clear()
                            text_scroll("Returning to Menu...", gameSpeed)
                            time.sleep(0.5)
                            break
                        else:
                            text_scroll("(INVALID SELECTION!)", gameSpeed)
                            time.sleep(2)
                    continue

                elif choice in ["2", "game", "games"]:
                    while True:
                            clear()
                            text_scroll(r"""
Game Options:
1) Input Methods
2) Game Speed
            
3) Back""", gameSpeed)
                            choice = input().lower()

                            if choice in ["1", "input", "input methods", "i", "method"]:
                                while True:
                                    clear()
                                    text_scroll(r"""
Input Methods:
1) Full: Back, Option1, Option2.
2) Minimal: 1, 2, 3.
                                            
3) Back""", gameSpeed)
                                    choice = input().lower()

                                    if choice in ["1", "full", "f"]:
                                        inputMethod = 1
                                        clear()
                                        text_scroll("Input Method set to Full", gameSpeed)
                                        time.sleep(0.5)
                                        break
                                    elif choice in ["2", "minimal", "m"]:
                                        inputMethod = 2
                                        clear()
                                        text_scroll("Input Method set to Minimal", gameSpeed)
                                        time.sleep(0.5)
                                        break
                                    elif choice in ["3", "back", "b"]:
                                        clear()
                                        text_scroll("Returning to Menu...", gameSpeed)
                                        time.sleep(0.5)
                                        break
                                    else:
                                        text_scroll("(INVALID SELECTION!)", gameSpeed)
                                        time.sleep(2)

                            elif choice in ["2", "game speed", "speed", "s"]:
                                while True:
                                    clear()
                                    text_scroll(r"""
Game Speed:
1) Slow (0.5)
2) Normal (0.1)
3) Fast (0.01)

4) Back""", gameSpeed)          
                                    choice = input().lower()

                                    if choice in ["1", "slow", "s"]:
                                        gameSpeed = 0.25
                                        clear()
                                        text_scroll("Game Speed set to Slow", gameSpeed)
                                        time.sleep(0.5)
                                        break
                                    elif choice in ["2", "normal", "n"]:
                                        gameSpeed = 0.1
                                        clear()
                                        text_scroll("Game Speed set to Normal", gameSpeed)
                                        time.sleep(0.5)
                                        break
                                    elif choice in ["3", "fast", "f"]:
                                        gameSpeed = 0.01
                                        clear()
                                        text_scroll("Game Speed set to Fast", gameSpeed)
                                        time.sleep(0.5)
                                        break
                                    elif choice in ["4", "back", "b"]:
                                        clear()
                                        text_scroll("Returning to Menu...", gameSpeed)
                                        time.sleep(0.5)
                                        break
                                    else:
                                        text_scroll("(INVALID SELECTION!)", gameSpeed)
                                        time.sleep(2)
                                        
                            elif choice in ["3", "back", "b"]:
                                break
                            else:
                                text_scroll("(INVALID SELECTION!)", gameSpeed)
                                time.sleep(2)

                elif choice in ["3", "back", "b"]:
                    break
                else:
                    text_scroll("(INVALID SELECTION!)", gameSpeed)
                    time.sleep(2)

        elif choice in ["4", "back", "b"]:
            break
        else:
            text_scroll("(INVALID SELECTION!)", gameSpeed)
            time.sleep(2)

loading_screen()

while True: 
    clear()
    time.sleep(0.5)
    for line in logo.splitlines():
        print(line)
        time.sleep(0.15)
    print("\n")
    text_scroll(r"""
1) Play
2) Options

3) Exit""", gameSpeed, True)
    choice = input().lower()
    if choice in ["1", "play", "p"]:
        break
    elif choice in ["2", "options", "o"]:
        menu()
    elif choice in ["3", "exit", "e"]:
        clear()
        text_scroll("Goodbye!", gameSpeed)
        time.sleep(2)
        clear()
        exit()
    else:
        clear()
        text_scroll("(INVALID SELECTION!)", gameSpeed)
        time.sleep(2)
