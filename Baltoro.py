import random as r
from collections import Counter
import time
import math 
import string 
import pprint
import os

# VARIABLES:
testRun = True # True / False
doLoadingScreen = True # True / False
ante = 0
money = 0
handSize = 8
hands = [4, 4]
discards = [3, 3]
chips = 0
mult = 0
roundScore = 0
printMethod = 2 # 1 = Normal, 2 = Scroll
cardStyle = 2 # 1 = Default, 2 = Recommended
textColour = 0
gameSpeed = 3
tutorial = True # True / False

tutorialText = r"""
[Welcome to the game!]

Your goal is to create the highest scoring poker hand possible and reach the blind score to continue.
    •    You are dealt 8 cards from your deck.

Choose up to 5 cards to play by entering their positions (indexes), separated by spaces. Example input: 1 5 7 4 8
    •    After playing a hand, the used cards return to your deck for future draws.
    •    Hands and discards represent your remaining chances.

Running out Hands is game over, whereas you will be unable to use discards.
    •    Different hand types (like pairs, flushes, etc.) award chips and multipliers based on their strength and rarity.
    •    The chips you earn from the cards played and hand bonuses are multiplied by the mult to calculate your score for that hand.

These two values are multiplied together to calculate your total score for that hand.
    •    Jokers are special cards that give unique effects to boost your score in creative ways."""

logo = r"""
         ____        _ _ 
        |  _ \      | | |
        | |_) | __ _| | |_ ___  _ __ ___ 
        |  _ < / _` | | __/ _ \| '__/ _ \ 
        | |_) | (_| | | || (_) | | | (_) |
        |____/ \__,_|_|\__\___/|_|  \___/ 
     𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵𓏵
"""

# LISTS:
suits = ["S", "H", "D", "C"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

# List of modifiers and their corresponding functions
modifiers = {
    "+": lambda chips, mult: (chips + 30, mult),  # add 30 chips
    "-": lambda chips, mult: (chips - 30, mult),  # subtract 30 chips
    "*": lambda chips, mult: (chips, mult + 4),  # add 4 multiplier
    "^": lambda chips, mult: (chips, mult * 1.5),  # times multiplier by 1.5
    "++": lambda chips, mult: (chips + 50, mult),  # add 50 to the card
    "--": lambda chips, mult: (chips - 50, mult),  # subtract 50 from the card
    "**": lambda chips, mult: (chips, mult + 20),  # add 20 multiplier to the card
    "^^": lambda chips, mult: (chips, mult * 2),  # times multiplier by 2
    None: lambda chips, mult: (chips, mult)  # no modifier
}

# List of suits and their corresponding symbols (for mapping)
suitMap = {
    "S": "♠", # Spades
    "H": "♥", # Hearts
    "D": "♦", # Diamonds
    "C": "♣", # Clubs
}

def nameMap(ante): 
    blindNames = ["Small", "Big", "Boss"]
    if ante % 3 == 0:
        return blindNames[2]
    elif ante % 3 == 2:
        return blindNames[1]
    else:
        return blindNames[0]
    
jokers = {
    ("Joker", 2, "+4 Multi"),
    ("Greedy Joker", 5, "Played cards with ♦ Diamond suit give +3 Mult when scored"),
    ("Lusty Joker", 5, "Played cards with ♥ Heart suit give +3 Mult when scored"),
    ("Wrathful Joker", 5, "Played cards with ♠ Spade suit give +3 Mult when scored"),
    ("Gluttonous Joker", 5, "Played cards with ♣ Club suit give +3 Mult when scored"),
    ("Jolly Joker", 3, "+8 Mult if played hand contains a Pair"),
    ("Zany Joker", 4, "+12 Mult if played hand contains a Three of a Kind"),
    ("Mad Joker", 4, "+10 Mult if played hand contains a Two Pair"),
    ("Crazy Joker", 4, "+12 Mult if played hand contains a Straight"),
    ("Droll Joker", 4, "+10 Mult if played hand contains a Flush"),
    ("Sly Joker", 3, "+50 Chips if played hand contains a Pair"),
    ("Wily Joker", 4, "+100 Chips if played hand contains a Three of a Kind"),
    ("Clever Joker", 4, "+80 Chips if played hand contains a Two Pair"),
    ("Devious Joker", 4, "+80 Chips if played hand contains a Flush"),
    ("Half Joker", 5, "+20 Mult if played hand contains 3 or fewer cards"),
    ("Joker Stencil", 8, "x1 Mult for each empty Joker slot"),
    ("Banner", 5, "+30 Chips for each remaining discard"),
    ("Mystic Summit", 5, "+15 Mult when 0 discards remaining"),
    ("Misprint", 4, "+0-23 Mult"),
    ("Fibonacci", 8, "Each played Ace, 2, 3, 5, or 8 gives +8 Mult when scored"),
    ("Scary Face", 4, "Played face cards give +30 Chips when scored"),
    ("Abstract Joker", 4, "+3 Mult for each Joker card"),
    ("Delayed Gratification", 4, "Earn $2 per discard if no discards are used by end of the round"),
    ("Even Steven", 4, "Played cards with even rank give +4 Mult when scored"), 
    ("Odd Todd", 4, "Played cards with odd rank give +31 Chips when scored")
}

jokerDeck = []

# Template of cards to be copied
templateCards = [
    ["A",  "S", 11, None], ["A",  "C", 11, None], ["A",  "H", 11, None], ["A",  "D", 11, None],  # Aces
    ["K",  "S", 10, None], ["K",  "C", 10, None], ["K",  "H", 10, None], ["K",  "D", 10, None],  # Kings
    ["Q",  "S", 10, None], ["Q",  "C", 10, None], ["Q",  "H", 10, None], ["Q",  "D", 10, None],  # Queens
    ["J",  "S", 10, None], ["J",  "C", 10, None], ["J",  "H", 10, None], ["J",  "D", 10, None],  # Jacks
    ["10", "S", 10, None], ["10", "C", 10, None], ["10", "H", 10, None], ["10", "D", 10, None],  # 10s
    ["9",  "S",  9, None], ["9",  "C",  9, None], ["9",  "H",  9, None], ["9",  "D",  9, None],  # 9s
    ["8",  "S",  8, None], ["8",  "C",  8, None], ["8",  "H",  8, None], ["8",  "D",  8, None],  # 8s
    ["7",  "S",  7, None], ["7",  "C",  7, None], ["7",  "H",  7, None], ["7",  "D",  7, None],  # 7s
    ["6",  "S",  6, None], ["6",  "C",  6, None], ["6",  "H",  6, None], ["6",  "D",  6, None],  # 6s
    ["5",  "S",  5, None], ["5",  "C",  5, None], ["5",  "H",  5, None], ["5",  "D",  5, None],  # 5s
    ["4",  "S",  4, None], ["4",  "C",  4, None], ["4",  "H",  4, None], ["4",  "D",  4, None],  # 4s
    ["3",  "S",  3, None], ["3",  "C",  3, None], ["3",  "H",  3, None], ["3",  "D",  3, None],  # 3s
    ["2",  "S",  2, None], ["2",  "C",  2, None], ["2",  "H",  2, None], ["2",  "D",  2, None],  # 2s
]

cards = templateCards

colours = {
    "0": '\033[0m', # White
    "1": '\033[95m', # Purple
    "2": '\033[96m', # Cyan
    "3": '\033[94m', # Blue
    "4": '\033[92m', # Green
    "5": '\033[93m', # Yellow
    "6": '\033[91m' # Red
} # List of Text Colours

def clear(): # Clear Screen Function
    os.system('cls' if os.name == 'nt' else 'clear')

def encoder():
    global cardStyle, textColour, printMethod, gameSpeed
    return f"Your Settings Configuration Code is: D{cardStyle}.C{textColour}.F{printMethod}.S{gameSpeed}"

def decoder(code):
    global cardStyle, textColour, printMethod, gameSpeed
    clear()
    if len(code) != 11:
        clear()
        text_scroll("Invalid code length. Please enter a valid code.")
        time.sleep(0.5)
        return False
    if code[0] != "D" or code[3] != "C" or code[6] != "F" or code[9] != "S":
        clear()
        text_scroll("Invalid code format. Please enter a valid code.")
        time.sleep(0.5)
        clear()
        return False
    cardStyle = int(code.split(".")[0][1:])
    textColour = int(code.split(".")[1][1:])
    printMethod = int(code.split(".")[2][1:])
    gameSpeed = int(code.split(".")[3][1:])
    return True 

def text_scroll(text, delay=gameSpeed, isLogo=False): # Text Scroll Function
    global textColour, colours, printMethod
    if delay == 1:
        delay = 0.25
    elif delay == 2:
        delay = 0.1
    elif delay == 3:
        delay = 0.01
    if printMethod == 2: # Scroll Print

        if textColour: # Coloured text
            display_text = ""
            for character in text:
                clear()
                if isLogo: # If logo is part of the text
                    print(logo) # Print the logo each time
                display_text += character
                print(colours[str(textColour)] + display_text + "\033[0m") # Prints the text with its corrisponding colour
                time.sleep(delay)
        else: # Non-coloured text
            display_text = ""
            for character in text:
                clear()
                if isLogo:
                    print(logo)
                display_text += character
                print(display_text)
                time.sleep(delay)
    
    elif printMethod == 1: # Normal Print
        if textColour: # Coloured text
            if isLogo:
                print(logo)
            print(colours[str(textColour)] + text + "\033[0m") # Prints the text with its corrisponding colour at once
        else: # Non-coloured text
            if isLogo:
                print(logo)
            print(text) # Prints the text at once without any colour


def loading_screen(): # Loading Screen Function
    clear()
    display_text = ""
    for char in "Loading Pr": # First half at 0.15/cps (characters per second)
        clear()
        display_text += char
        print(display_text)
        time.sleep(0.15)
    for char in "ogram: Baltoro": # Second half at 0.05/cps
        clear()
        display_text += char
        print(display_text)
        time.sleep(0.05)
    clear()
    print(display_text + "\n [■□□□□□□□□□] 10%")
    time.sleep(r.uniform(0.2, 1))
    clear()
    print(display_text + "\n [■■□□□□□□□□] 20%")
    time.sleep(r.uniform(0.2, 1))
    clear()
    print(display_text + "\n [■■■□□□□□□□] 30%")
    time.sleep(r.uniform(0.2, 1))
    clear()
    print(display_text + "\n [■■■■□□□□□□] 40%")
    time.sleep(r.uniform(0.2, 1))
    clear()
    print(display_text + "\n [■■■■■□□□□□] 50%")
    time.sleep(r.uniform(0.2, 1))
    clear()
    print(display_text + "\n [■■■■■■□□□□] 60%")
    time.sleep(r.uniform(0.2, 1))
    clear()
    print(display_text + "\n [■■■■■■■□□□] 70%")
    time.sleep(r.uniform(0.2, 1))
    clear()
    print(display_text + "\n [■■■■■■■■□□] 80%")
    time.sleep(r.uniform(0.2, 1))
    clear()
    print(display_text + "\n [■■■■■■■■■□] 90%")
    time.sleep(r.uniform(0.2, 1))
    clear()
    print(display_text + "\n [■■■■■■■■■■] 100%")
    time.sleep(r.uniform(2, 3))
    clear()
        
def menu():
    global printMethod, cardStyle, textColour, gameSpeed
    while True:

        clear()
        text_scroll(r"""
[Menu]

1) Credits
2) Customise Deck
3) Settings
4) Configuration Code
                
5) Back""") # Menu Options
        choice = input().lower()

        if choice in ["1", "credits", "credit", "c"]: # Credits
            while True:
                clear()
                text_scroll(r"""
[Credits]

Directed by Me.
Curated by Me.
Developed by Me in association with OpenAI and Balatro.

1) Back""") # Credits
                choice = input().lower()

                if choice in ["1", "back", "b"]: # Back to Main Menu
                    clear()
                    text_scroll("Returning to Menu...")
                    time.sleep(0.5)
                    clear()
                    break
                else: # Invalid Input
                    clear()
                    text_scroll("(INVALID SELECTION!)")
                    time.sleep(2)
                    clear()

        elif choice in ["2", "customise deck", "customise", "deck", "c", "d"]: # Customise Deck Options
            while True:
                clear()
                text_scroll(r"""
[Customise Deck]
- How the cards are displayed.

1) AS KH QD JC 10S 9H 8D 7S (Default)
2) A♠ K♥ Q♣ J♦ 10♤ 9♡ 8♧ 7♢ (Recommended)

3) Back""") # Customise Deck Options
                choice = input().lower()

                if choice in ["1", "default", "d"]: # Card Style = 1 (Default)
                    clear()
                    cardStyle = 1
                    text_scroll("Card Style set to: AS KH QD JC 10S 9H 8D 7S (Default)")
                    time.sleep(0.5)
                    clear()
                    break
                elif choice in ["2", "recommended", "recommened", "r"]: # Card Style = 2 (Recommended)
                    clear()
                    cardStyle = 2
                    text_scroll("Card Style set to: A♠ K♥ Q♣ J♦ 10♤ 9♡ 8♧ 7♢ (Recommended)")
                    time.sleep(0.5)
                    clear()
                    break
                elif choice in ["3", "back", "b"]: # Back to Main Menu
                    clear()
                    text_scroll("Returning to Menu...")
                    time.sleep(0.5)
                    clear()
                    break
                else: # Invalid Input
                    clear()
                    text_scroll("(INVALID SELECTION!)")
                    time.sleep(2)
                    clear()

        elif choice in ["3", "settings", "setting", "s"]: # Settings
            while True:
                clear()
                text_scroll(r"""
[Settings]
- Game settings and options.

1) Graphics
2) Game

3) Back""") # Settings
                choice = input().lower()
                if choice in ["1", "graphics", "graphic"]: # Graphics Options
                    while True:
                        clear()
                        text_scroll(f"""
\033[0m[Graphics Options]\033[0m
- Colour of the text shown.

\033[0m1) Normal\033[0m
{colours["1"]}2) Purple\033[0m
{colours["2"]}3) Cyan\033[0m
{colours["3"]}4) Blue\033[0m
{colours["4"]}5) Green\033[0m
{colours["5"]}6) Yellow\033[0m
{colours["6"]}7) Red\033[0m\n
8) Back""") # Text Colour Options

                        choice = input().lower()

                        if choice in ["1", "default", "d"]: # Text Colour = Default
                            textColour = 0
                            clear()
                            text_scroll("Text Colour set to Default")
                            time.sleep(0.5)
                            clear()
                            break
                        elif choice in ["2", "purple", "p"]: # Text Colour = Purple
                            textColour = 1
                            clear()
                            text_scroll("Text Colour set to Purple")
                            time.sleep(0.5)
                            clear()
                            break
                        elif choice in ["3", "cyan", "c"]: # Text Colour = Cyan
                            textColour = 2
                            clear()
                            text_scroll("Text Colour set to Cyan")
                            time.sleep(0.5)
                            clear()
                            break
                        elif choice in ["4", "blue", "bl"]: # Text Colour = Blue
                            textColour = 3
                            clear()
                            text_scroll("Text Colour set to Blue")
                            time.sleep(0.5)
                            clear()
                            break
                        elif choice in ["5", "green", "g"]: # Text Colour = Green
                            textColour = 4
                            clear()
                            text_scroll("Text Colour set to Green")
                            time.sleep(0.5)
                            clear()
                            break
                        elif choice in ["6", "yellow", "y"]: # Text Colour = Yellow
                            textColour = 5
                            clear()
                            text_scroll("Text Colour set to Yellow")
                            time.sleep(0.5)
                            clear()
                            break
                        elif choice in ["7", "red", "r"]: # Text Colour = Red
                            textColour = 6
                            clear()
                            text_scroll("Text Colour set to Red")
                            time.sleep(0.5)
                            clear()
                            break
                        elif choice in ["8", "back", "b"]: # Back to Main Menu
                            clear()
                            text_scroll("Returning to Menu...")
                            time.sleep(0.5)
                            clear()
                            break
                        else: # Invalid Input
                            clear()
                            text_scroll("(INVALID SELECTION!)")
                            time.sleep(2)
                            clear()

                elif choice in ["2", "game", "games"]: # Game Options
                    while True:
                            clear()
                            text_scroll(r"""
[Game Options]

1) Print Methods
2) Game Speed
            
3) Back""") # Game Options
                            choice = input().lower()

                            if choice in ["1", "print", "print methods", "i", "method"]: # Print Method Options
                                while True:
                                    clear()
                                    text_scroll(r"""
[Print Methods]
- The way text is shown.

1) Normal: prints anything at once.
2) Scroll: prints each letter at a time, like a typewriter.

3) Back""") # Print Method Options
                                    choice = input().lower()

                                    if choice in ["1", "normal", "n"]: # Print Method = 1 (Normal)
                                        printMethod = 1
                                        clear()
                                        text_scroll("Print Method set to Normal")
                                        time.sleep(0.5)
                                        clear()
                                        break
                                    elif choice in ["2", "scroll", "s"]: # Print Method = 2 (Scroll)
                                        printMethod = 2
                                        clear()
                                        text_scroll("Print Method set to Scroll")
                                        time.sleep(0.5)
                                        clear()
                                        break
                                    elif choice in ["3", "back", "b"]: # Back to Main Menu
                                        clear()
                                        text_scroll("Returning to Menu...")
                                        time.sleep(0.5)
                                        clear()
                                        break
                                    else: # Invalid Input
                                        clear()
                                        text_scroll("(INVALID SELECTION!)")
                                        time.sleep(2)
                                        clear()

                            elif choice in ["2", "game speed", "speed", "s"]: # Game Speed Options
                                while True:
                                    clear()
                                    text_scroll(r"""
[Game Speed]
- How fast the text is shown.

1) Slow (0.5)
2) Normal (0.1)
3) Fast (0.01)

4) Back""") # Game Speed Options
                                    choice = input().lower()

                                    if choice in ["1", "slow", "s"]: # Speed = Slow (0.25/cps)
                                        gameSpeed = 1
                                        clear()
                                        text_scroll("Game Speed set to Slow")
                                        time.sleep(0.5)
                                        break
                                    elif choice in ["2", "normal", "n"]: # Speed = Normal (0.1/cps)
                                        gameSpeed = 2
                                        clear()
                                        text_scroll("Game Speed set to Normal")
                                        time.sleep(0.5)
                                        break
                                    elif choice in ["3", "fast", "f"]: # Speed = Fast (0.01/cps)
                                        gameSpeed = 3
                                        clear()
                                        text_scroll("Game Speed set to Fast")
                                        time.sleep(0.5)
                                        break
                                    elif choice in ["4", "back", "b"]: # Back to Main Menu
                                        clear()
                                        text_scroll("Returning to Menu...")
                                        time.sleep(0.5)
                                        break
                                    else: # Invalid Input
                                        clear()
                                        text_scroll("(INVALID SELECTION!)")
                                        time.sleep(2)
                                        
                            elif choice in ["3", "back", "b"]: # Back to Main Menu
                                clear()
                                text_scroll("Returning to Menu...")
                                time.sleep(0.5)
                                break
                            else: # Invalid Input
                                clear()
                                text_scroll("(INVALID SELECTION!)")
                                time.sleep(2)

                elif choice in ["3", "back", "b"]: # Back to Main Menu
                    clear()
                    text_scroll("Returning to Menu...")
                    time.sleep(0.5)
                    break
                else: # Invalid Input
                    clear()
                    text_scroll("(INVALID SELECTION!)")
                    time.sleep(2)
        elif choice in ["4", "configuration code", "code", "c"]: # Configuration Code
            clear()
            text_scroll(r"""
[Configuration Code]
- Setting's Configuration Code.

1) Enter your Code
2) Receive your Code

3) Back""") # Game Speed Options
            choice = input().lower()
            clear()
            if choice in ["1", "enter", "e"]: # Enter Code
                clear()
                text_scroll("Input your Configuration Code:\n")
                code = input()
                while decoder(code) != True:
                    clear()
                    text_scroll("Invalid code. Please enter a valid code.")
                    code = input()
                clear()
                text_scroll(f"""Configuration set to:
cardStyle: {"default" if cardStyle == 1 else "advanced"}  
textColour: {"white" if textColour == 0 else "purple" if textColour == 1 else "cyan" if textColour == 2 else "blue" if textColour == 3 else "green" if textColour == 4 else "yellow" if textColour == 5 else "red" if textColour == 6 else "unknown"} 
printMethod: {"normal" if printMethod == 1 else "scroll"} 
gameSpeed: {"slow" if gameSpeed == 1 else "normal" if gameSpeed == 2 else "fast" if gameSpeed == 3 else "unknown"} 
""")

                print("\nPress Enter to continue...")
            elif choice in ["2", "receive", "r"]: # Receive Code
                clear()
                text_scroll(encoder())
                choice = input("\nPress Enter to continue...")
                clear()
            else: # Invalid Input
                clear()
                text_scroll("(INVALID SELECTION!)")
                time.sleep(2)
                clear()
        elif choice in ["5", "back", "b"]: # Back to Main Menu
            clear()
            text_scroll("Returning to Menu...")
            time.sleep(0.5)
            break
        else: # Invalid Input
            clear()
            text_scroll("(INVALID SELECTION!)")
            time.sleep(2)

def addCardToDeck(name=None, suit=None, modifier=None):
    if [name, suit, modifier] == None: # automatic mode
        nameLuck = r.randint(0, len(ranks) - 1)
        suitLuck = r.randint(0, len(suits) - 1)
        modifierLuck = r.randint(0, len(modifiers) - 1)
        name = ranks[nameLuck]
        suit = suits[suitLuck]
        if r.randint(0, 10) == 0:
            modifier = list(modifiers.keys())[modifierLuck]
        if name == "A":
            chips = 11
        elif name in ["K", "Q", "J"]:
            chips = 10
        elif name in ranks:
            chips = int(name)

        card = (name, suit, chips, modifier)
    return card

def printCard(card):
    global cardStyle
    rank = card[0]
    modifier = card[3] if card[3] else ""
    
    if cardStyle == 2:
        suit = suitMap[card[1]]
        return rank + suit + modifier
    elif cardStyle == 1:
        suit = card[1]
        return rank + suit + modifier
    else:
        return f"{rank} {card[1]}{modifier}"  # default fallback

def checkHand(chips, mult, selectedHand):
    selectedHand = sorted(selectedHand, key=lambda card: ranks.index(card[0]))
    rank_counts = Counter(card[0] for card in selectedHand)
    suit_counts = Counter(card[1] for card in selectedHand)
    values = [card[2] for card in selectedHand]

    def apply_modifiers():
        nonlocal chips, mult
        for card in selectedHand:
            if card[3] in modifiers:
                chips, mult = modifiers[card[3]](chips, mult)

    # Check for specific 5-card combinations inside the hand
    if len(selectedHand) >= 5:
        # Royal Flush
        if any(
            all((rank in [card[0] for card in selectedHand if card[1] == suit])
                for rank in ["10", "J", "Q", "K", "A"])
            for suit in suit_counts
        ):
            chips += 100 + sum(values)
            mult += 8
            apply_modifiers()

        # Straight Flush
        for suit in suit_counts:
            suited = [card for card in selectedHand if card[1] == suit]
            if len(suited) >= 5:
                suited = sorted(suited, key=lambda card: ranks.index(card[0]))
                if all(
                    ranks.index(suited[i][0]) + 1 == ranks.index(suited[i + 1][0])
                    for i in range(len(suited) - 1)
                ):
                    chips += 80 + sum(card[2] for card in suited)
                    mult += 8
                    apply_modifiers()

        # Flush
        if any(count >= 5 for count in suit_counts.values()):
            chips += 50 + sum(values)
            mult += 5
            apply_modifiers()

        # Straight
        rank_idxs = sorted(set(ranks.index(card[0]) for card in selectedHand))
        for i in range(len(rank_idxs) - 4):
            if rank_idxs[i + 4] - rank_idxs[i] == 4:
                chips += 30 + sum(values)
                mult += 3
                apply_modifiers()
                break

        # Full House
        if 3 in rank_counts.values() and 2 in rank_counts.values():
            chips += 40 + sum(values)
            mult += 4
            apply_modifiers()

    # Other combos that can appear within any hand size
    if 5 in rank_counts.values():
        chips += 120 + sum(values)
        mult += 12
        apply_modifiers()
    elif 4 in rank_counts.values():
        chips += 60 + sum(values)
        mult += 7
        apply_modifiers()
    elif sorted(rank_counts.values()) == [2, 3]:  # Flush House
        if len(suit_counts) == 1:
            chips += 140 + sum(values)
            mult += 14
            apply_modifiers()
    elif list(rank_counts.values()).count(2) == 2:
        chips += 20 + sum(values)
        mult += 2
        apply_modifiers()
    elif 3 in rank_counts.values():
        chips += 30 + sum(values)
        mult += 3
        apply_modifiers()
    elif 2 in rank_counts.values():
        chips += 10 + sum(values)
        mult += 1
        apply_modifiers()
    else:
        selectedCard = max(selectedHand, key=lambda card: card[2])
        chips += selectedCard[2] + 5
        mult += 1
        if selectedCard[3] in modifiers:
            chips, mult = modifiers[selectedCard[3]](chips, mult)

    return chips, mult

        
#addCardToDeck(
#    input("name (2-9/J-A): ").upper(),
#    input("suit (S/H/D/C): ").upper(),
#    input("modifier (++/--/**/^^): ")
#)

def play():
    global chips, mult, hands, discards, roundScore, money, ante, handSize, cards, tutorial, goalScore
    if tutorial:
        clear()
        text_scroll(tutorialText)
        choice = input("\nPress Enter to continue...")
        clear()
        tutorial = False
    if not testRun:
        money = 0
    else:
        money = 1000
    cards = templateCards
    goalScore = 300
    ante = 0

    while True: # Main Game Loop
        ante += 1
        roundScore = 0
        hands[1] = hands[0]
        discards[1] = discards[0]
        chips = 0
        mult = 0
        hand = []

        while not testRun: # Ante loop (skips whne testing)
            clear()

            while len(hand) < handSize: # Fill hand with cards
                hand.append(cards.pop(r.randint(0, len(cards) - 1)))
                hand = sorted(hand, key=lambda card: ranks.index(card[0]), reverse=True)

            text_scroll(f"{len(cards)} cards left in deck")
            time.sleep(0.5)
            text_scroll(f"{len(hand)} cards in hand")

            if hands[1] == 0: # No hands left and you lose
                clear()
                text_scroll("You Lose!")
                time.sleep(2)
                clear()
                return
            
            clear()
            text_scroll(printBoard(hand, chips, mult, hands, discards, roundScore, cards, money, ante, goalScore), delay=0.005) # Print the board
            selected = input().split() # Select the cards to play
            if "menu" in selected:
                clear()
                text_scroll("Returning to Menu...")
                time.sleep(0.5)
                menu()
                clear()
                continue

            try: # Convert the input to integers
                selected = list(map(int, selected))
            except ValueError:
                clear()
                text_scroll("Invalid input! Please enter numbers only.")
                time.sleep(2)
                clear()
                continue

            if len(selected) != len(set(selected)): # Check for duplicate cards selected
                clear()
                text_scroll("Duplicate selections are not allowed!")
                time.sleep(2)
                clear()
                continue

            selectedHand = []

            if len(selected) > 5: # Check if too many cards are selected
                clear()
                text_scroll("Invalid Amount Selected!")
                time.sleep(2)
                clear()
                continue

            for i in selected: # Append the selected cards to the selectedHand
                selectedHand.append(hand[i-1])

            choice = input("(1) Play / (2) Discard\n").lower() # Choose what to do with the selected cards
            clear()

            if choice in ["1", "play"]:
                chips = 0
                mult = 0

                chips, mult = checkHand(chips, mult, selectedHand) # Convert the selected cards to chips and multipliers
                hands[1] -= 1
                roundScore += chips * mult # Add the chips and multipliers to the round score

                for card in selectedHand: # Remove the selected cards from the hand and add it back to the deck
                    if card in hand:
                        hand.remove(card)
                        cards.append(card)

                if roundScore >= goalScore: # Check if the round score is greater than or equal to the goal score
                    clear()
                    text_scroll(f"You Win!\nMoney: +{ante*3}$") # Add three times the ante to the money
                    money += ante * 3
                    chips = 0
                    mult = 0
                    roundScore = 0
                    time.sleep(2)
                    goalScore = int(1.5 * goalScore) # Increase the score required by 50%
                    clear()
                    break

            elif choice in ["2", "discard"]:
                if discards[1] == 0: # If no discards are left
                    text_scroll("No discards left!")
                    continue

                else: # Ff discards remain
                    for card in selectedHand: # Remove the selected cards from the hand and add it back to the deck
                        hand.remove(card)
                        cards.append(card)
                    discards[1] -= 1

        clear()
        text_scroll(printShop())
        choice = input().lower()

def printShop():
    global cards, money, jokers, vouchers
    jokerCards = []
    shopCards = []
    amountOfCards = r.randint(1, 4)
    amountOfJokers = r.randint(1, 3)

    for i in range(amountOfCards):
        modifierChance = r.randint(1, 5)
        if modifierChance == 1:
            card = r.choice(cards)  # Select a random card
            modifier = r.choice(list(modifiers.keys()))  # Select a random modifier
            modified_card = [card[0], card[1], card[2], modifier]  # Add the modifier to the card
            shopCards.append(modified_card)  # Append the modified card to the shop
        else:
            card = r.choice(cards)  # Select a random card
            card.append(r.randint(1, 20), -1)
            shopCards.append(card)

    for i in range(amountOfJokers):
        joker = r.choice(list(jokers))
        jokerCards.append(joker)  # Append the joker to the shop

    while True: 
        text_scroll(f"""\n
୧‿̩͙ ˖︵ ꕀ⠀SHOP ꕀ ︵˖ ‿̩͙୨

[Money: {money}$]

- Playing Cards:
{'\n'.join(f"{i + 1}) {printCard(card)}: {card[-1]}$" for i, card in enumerate(shopCards))}

- Jokers:
{'\n'.join(f"{i + 1 + amountOfCards}) {joker[0]}: {joker[1]}$ - {joker[2]}" for i, joker in enumerate(jokerCards))}

"leave" to exit the shop
    """)
        choice = input("Select a card to buy: ")

        if choice == "leave":
            clear()
            text_scroll("Leaving the shop...")
            time.sleep(0.5)
            clear()
            break

        elif choice.isdigit() and 1 <= choice <= amountOfCards:
            if money >= cardPrice:
                clear()
                text_scroll(f"You bought {shopCards[choice-1]} for {cardPrice}$")
                time.sleep(0.5)
                clear()
                money -= cardPrice
                shopCards[choice - 1].remove(shopCards[choice - 1][-1])
                cards.append(shopCards[choice - 1])
                shopCards.pop(choice - 1)
                continue
            elif money < cardPrice:
                clear()
                text_scroll("Not enough money!")
                time.sleep(2)
                clear()
                continue
            else:
                clear()
                text_scroll("Invalid selection!")
                time.sleep(2)
                clear()
                continue
        elif choice.isdigit() and len(shopCards) + 1 < int(choice) <= len(shopCards) + amountOfJokers:
            choice = int(choice)
            cardPrice = r.randint(1, 20)
            if money >= shopCards[choice-1][1]:
                clear()
                text_scroll(f"You bought {shopCards[choice-1]} for {shopCards[choice-1][1]}$")
                time.sleep(0.5)
                clear()
                money -= cardPrice
                jokerDeck.append(shopCards[choice - 1])
                shopCards.pop(choice - 1)
                continue
            elif money < cardPrice:
                clear()
                text_scroll("Not enough money!")
                time.sleep(2)
                clear()
                continue
            else:
                clear()
                text_scroll("Invalid selection!")
                time.sleep(2)
                clear()
                continue
        else:
            clear()
            text_scroll("Invalid selection!")
            time.sleep(2)
            clear()
            continue

def printBoard(hand, chips, mult, hands, discards, roundScore, cards, money, ante, goalScore):
    return f"""\n[{nameMap(ante)} Blind]
[Score at least: {goalScore}]
[Reward: 3$]
[Round Score: {roundScore}]
[Previous Score: {chips} x {mult}]
[Money: {money}$]
[Ante: {ante}]

- Jokers:
{None}

- Hand:
{'\n'.join(f"{i + 1}) {printCard(card)}" for i, card in enumerate(hand))}

[Hands: {hands[1]}/{hands[0]}]
[Discards: {discards[1]}/{discards[0]}]
           

[Play: "1"]
[Discard: "2"]

["menu" to exit]
"""


# START OF PROGRAM
if not testRun:
    loading_screen() # Loading Sequence

while True:
    clear()
    if printMethod == 1:
        pass
    elif printMethod == 2:
        clear()
        time.sleep(0.5)
        for line in logo.splitlines(): # Print the Logo
            print(line)
            time.sleep(0.15)

    print("\n")

    text_scroll(r"""
1) Play
2) Options

3) Exit""", isLogo=True) # Prints the Options
    
    choice = input().lower()
    if choice in ["1", "play", "p"]: # Option 1: Play
        text_scroll("Do you want the Tutorial? (y/n)")
        while True:
            choice = input().lower()
            if choice in ["y", "yes", "t", "true"]:
                tutorial = True
                break
            elif choice in ["n", "no", "f", "false"]:
                tutorial = False
                break
            else:
                clear()
                text_scroll("(INVALID SELECTION!)")
                time.sleep(2)
                clear()
        play()
    elif choice in ["2", "options", "o"]: # Option 2: Menu
        menu()
    elif choice in ["3", "exit", "e"]: # Option 3: Exit
        clear()
        text_scroll("Goodbye!")
        time.sleep(1)
        clear()
        exit()
    else: # Invalid Input
        clear()
        text_scroll("(INVALID SELECTION!)")
        time.sleep(2)
