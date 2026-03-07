import requests
import sys
import json
import argparse
import os

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

def load_settings():
    defaults = {
        "logo": True,
        "colors": True,
        "formatting": True,
        "unicode": True
    }
    if not os.path.exists(SETTINGS_FILE):
        return defaults
    try:
        with open(SETTINGS_FILE, "r") as f:
            return {**defaults, **json.load(f)}
    except:
        return defaults

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        print(f"Error saving settings: {e}")

logo_part1 = r'''
 ______                               ____     __                       __      
/\__  _\                             /\  _`\  /\ \                     /\ \__   
\/_/\ \/    __    ___     ____     __\ \ \/\_\\ \ \___      __     _ __\ \ ,_\  
   \ \ \  /'__`\/' _ `\  /',__\  /'__`\ \ \/_/_\ \  _ `\  /'__`\  /\`'__\ \ \/  
    \ \ \/\  __//\ \/\ \/\__, `\/\  __/\ \ \L\ \\ \ \ \ \/\ \L\.\_\ \ \/ \ \ \_ 
     \ \_\ \____\ \_\ \_\/\____/\ \____\\ \____/ \ \_\ \_\ \__/.\_\\ \_\  \ \__\
      \/_/\/____/\/_/\/_/\/___/  \/____/ \/___/   \/_/\/_/\/__/\/_/ \/_/   \/__/
'''

logo_part2 = r'''
 ____     __     ______                                                         
/\  _`\  /\ \   /\__  _\                                                        
\ \ \/\_\\ \ \  \/_/\ \/                                                        
 \ \ \/_/_\ \ \  __\ \ \                                                        
  \ \ \L\ \\ \ \L\ \\_\ \__                                                     
   \ \____/ \ \____//\_____\                                                    
    \/___/   \/___/ \/_____/                                                                                                      
'''

# rainbow!
colors_list = [
    "\033[91m",       # Red (T)
    "\033[38;5;208m", # Orange (e)
    "\033[38;5;214m", # Gold (n)
    "\033[93m",       # Yellow (s)
    "\033[92m",       # Green (e)
    "\033[96m",       # Cyan (C)
    "\033[94m",       # Blue (h)
    "\033[38;5;63m",  # Indigo (a)
    "\033[95m",       # Magenta (r)
    "\033[38;5;201m"  # Violet (t)
]
reset = "\033[0m"

# character boundaries for "T e n s e C h a r t"
slices = [
    (0, 8), (8, 18), (18, 26), (26, 35), (35, 43), 
    (43, 52), (52, 60), (60, 68), (68, 75), (75, 81)
]

def print_logo(text, settings):
    if not settings.get("logo", True):
        return
    
    use_colors = settings.get("colors", True)
    lines = text.strip('\n').split('\n')
    
    for line in lines:
        if use_colors:
            colored_line = ""
            for i, (start, end) in enumerate(slices):
                chunk = line[start:end]
                colored_line += f"{colors_list[i % len(colors_list)]}{chunk}{reset}"
            print(colored_line)
        else:
            print(line)

def getTenseData(args):
    params = {}
    if args.random:
        params['random'] = 'true'
    elif args.subject and args.verb:
        params['subject'] = args.subject
        params['verb'] = args.verb
    else:
        params['daily'] = 'true'

    try:
        response = requests.get("https://sea.navynui.cc/tensechart/api/index.php", params=params)
        if response.status_code == 200:
            data = response.json()
            subject_verb = [data['metadata']['subject'], data['metadata']['verb']]
            tenses = []
            for voice in ["active", "passive"]:
                for aspect in ["simple", "perfect", "continuous", "perfect_continuous"]:
                    for time in ["past", "present", "future"]:
                        tenses.append(data[voice][time][aspect])
            return subject_verb, tenses
        else:
            print(f"Server-side Error: http code {response.status_code}")
            sys.exit(0)
    except Exception as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)

def generateCharts(subject_verb, tenses, settings):
    use_colors = settings.get("colors", True)
    use_format = settings.get("formatting", True)
    use_unicode = settings.get("unicode", True)
    
    bold = "\033[1m" if use_format else ""
    italic = "\033[3m" if use_format else ""
    clr_reset = "\033[0m" if (use_colors or use_format) else ""

    # Box drawing characters
    H = "─" if use_unicode else "-"
    V = "│" if use_unicode else "|"
    TL = "╭" if use_unicode else "+"
    TR = "╮" if use_unicode else "+"
    BL = "╰" if use_unicode else "+"
    BR = "╯" if use_unicode else "+"
    TM = "┬" if use_unicode else "+"
    BM = "┴" if use_unicode else "+"
    ML = "├" if use_unicode else "+"
    MR = "┤" if use_unicode else "+"
    MM = "┼" if use_unicode else "+"
    
    # Subject-verb box
    boxLenght = len(subject_verb[0]) + len(subject_verb[1]) + 6
    print(TL + H * boxLenght + TR)
    print(f"{V}  {italic}{subject_verb[0]}  {subject_verb[1]}{clr_reset}  {V}")
    print(BL + H * boxLenght + BR)

    pastLenght = len(tenses[21]) + 2
    presentLenght = len(tenses[22]) + 2
    futureLenght = len(tenses[23]) + 2 

    topPastlenght = pastLenght - 7
    topPresentlenght = presentLenght - 10
    topFuturelenght = futureLenght - 9

    # Active chart
    print(TL + H * 20 + TM + H * pastLenght + TM + H * presentLenght + TM + H * futureLenght + TR)
    print(f"{V} {bold}{italic}Active{clr_reset}             {V} {bold}Past{clr_reset} " + " " * topPastlenght + f" {V} {bold}Present{clr_reset} " + " " * topPresentlenght + f" {V} {bold}Future{clr_reset} " + " " * topFuturelenght + f" {V}")
    print(ML + H * 20 + MM + H * pastLenght + MM + H * presentLenght + MM + H * futureLenght + MR)
    print(f"{V} {bold}Simple{clr_reset}             {V} " + tenses[0] + " " * (len(tenses[21]) - len(tenses[0])) + f" {V} " + tenses[1] + " " * (len(tenses[22]) - len(tenses[1])) + f" {V} " + tenses[2] + " " * (len(tenses[23]) - len(tenses[2])) + f" {V}")
    print(ML + H * 20 + MM + H * pastLenght + MM + H * presentLenght + MM + H * futureLenght + MR)
    print(f"{V} {bold}Perfect{clr_reset}            {V} " + tenses[3] + " " * (len(tenses[21]) - len(tenses[3])) + f" {V} " + tenses[4] + " " * (len(tenses[22]) - len(tenses[4])) + f" {V} " + tenses[5] + " " * (len(tenses[23]) - len(tenses[5])) + f" {V}")
    print(ML + H * 20 + MM + H * pastLenght + MM + H * presentLenght + MM + H * futureLenght + MR)
    print(f"{V} {bold}Continuous{clr_reset}         {V} " + tenses[6] + " " * (len(tenses[21]) - len(tenses[6])) + f" {V} " + tenses[7] + " " * (len(tenses[22]) - len(tenses[7])) + f" {V} " + tenses[8] + " " * (len(tenses[23]) - len(tenses[8])) + f" {V}")
    print(ML + H * 20 + MM + H * pastLenght + MM + H * presentLenght + MM + H * futureLenght + MR)
    print(f"{V} {bold}Perfect Continuous{clr_reset} {V} " + tenses[9] + " " * (len(tenses[21]) - len(tenses[9])) + f" {V} " + tenses[10] + " " * (len(tenses[22]) - len(tenses[10])) + f" {V} " + tenses[11] + " " * (len(tenses[23]) - len(tenses[11])) + f" {V}")
    print(BL + H * 20 + BM + H * pastLenght + BM + H * presentLenght + BM + H * futureLenght + BR)

    # Passive chart
    print(TL + H * 20 + TM + H * pastLenght + TM + H * presentLenght + TM + H * futureLenght + TR)
    print(f"{V} {bold}{italic}Passive{clr_reset}            {V} {bold}Past{clr_reset} " + " " * topPastlenght + f" {V} {bold}Present{clr_reset} " + " " * topPresentlenght + f" {V} {bold}Future{clr_reset} " + " " * topFuturelenght + f" {V}")
    print(ML + H * 20 + MM + H * pastLenght + MM + H * presentLenght + MM + H * futureLenght + MR)
    print(f"{V} {bold}Simple{clr_reset}             {V} " + tenses[12] + " " * (len(tenses[21]) - len(tenses[12])) + f" {V} " + tenses[13] + " " * (len(tenses[22]) - len(tenses[13])) + f" {V} " + tenses[14] + " " * (len(tenses[23]) - len(tenses[14])) + f" {V}")
    print(ML + H * 20 + MM + H * pastLenght + MM + H * presentLenght + MM + H * futureLenght + MR)
    print(f"{V} {bold}Perfect{clr_reset}            {V} " + tenses[15] + " " * (len(tenses[21]) - len(tenses[15])) + f" {V} " + tenses[16] + " " * (len(tenses[22]) - len(tenses[16])) + f" {V} " + tenses[17] + " " * (len(tenses[23]) - len(tenses[17])) + f" {V}")
    print(ML + H * 20 + MM + H * pastLenght + MM + H * presentLenght + MM + H * futureLenght + MR)
    print(f"{V} {bold}Continuous{clr_reset}         {V} " + tenses[18] + " " * (len(tenses[21]) - len(tenses[18])) + f" {V} " + tenses[19] + " " * (len(tenses[22]) - len(tenses[19])) + f" {V} " + tenses[20] + " " * (len(tenses[23]) - len(tenses[20])) + f" {V}")
    print(ML + H * 20 + MM + H * pastLenght + MM + H * presentLenght + MM + H * futureLenght + MR)
    print(f"{V} {bold}Perfect Continuous{clr_reset} {V} " + tenses[21] + f" {V} " + tenses[22] + f" {V} " + tenses[23] + f" {V}")
    print(BL + H * 20 + BM + H * pastLenght + BM + H * presentLenght + BM + H * futureLenght + BR)

def handle_settings(settings):
    print_logo(logo_part1, settings)
    print_logo(logo_part2, settings)
    
    use_unicode = settings.get("unicode", True)
    H = "─" if use_unicode else "-"
    V = "│" if use_unicode else "|"
    TL = "╭" if use_unicode else "+"
    TR = "╮" if use_unicode else "+"
    BL = "╰" if use_unicode else "+"
    BR = "╯" if use_unicode else "+"
    ML = "├" if use_unicode else "+"
    MR = "┤" if use_unicode else "+"
    TM = "┬" if use_unicode else "+"
    BM = "┴" if use_unicode else "+"

    def fmt_status(val):
        return "ON " if val else "OFF"

    print("\n")
    print(TL + H * 39 + TR)
    print(f"{V}{'Tense Chart Settings'.center(39)}{V}")
    print(ML + H * 6 + TM + H * 32 + MR)
    print(f"{V} 1.   {V} {('Logo: ' + fmt_status(settings['logo'])).ljust(30)} {V}")
    print(f"{V} 2.   {V} {('Colors: ' + fmt_status(settings['colors'])).ljust(30)} {V}")
    print(f"{V} 3.   {V} {('Formatting (Bold/Italic): ' + fmt_status(settings['formatting'])).ljust(30)} {V}")
    print(f"{V} 4.   {V} {('Unicode Outlines: ' + fmt_status(settings['unicode'])).ljust(30)} {V}")
    print(f"{V} 5.   {V} {'Exit'.ljust(30)} {V}")
    print(BL + H * 6 + BM + H * 32 + BR)
    
    choice = input("\nSelect a setting to toggle (1-4) or 5 to exit: ")
    if choice == '1':
        settings['logo'] = not settings['logo']
    elif choice == '2':
        settings['colors'] = not settings['colors']
    elif choice == '3':
        settings['formatting'] = not settings['formatting']
    elif choice == '4':
        settings['unicode'] = not settings['unicode']
    elif choice == '5':
        return False
    else:
        print("Invalid choice.")
        return True
    
    save_settings(settings)
    print("Settings updated!")
    return True

def main():
    settings = load_settings()
    
    parser = argparse.ArgumentParser(description="The Daily Tense Charts, now in your terminal!")
    parser.add_argument("-d", "--daily", action="store_true", help="Get today's tense chart")
    parser.add_argument("-r", "--random", action="store_true", help="Get a random tense chart")
    parser.add_argument("-s", "--subject", type=str, help="Subject for custom chart")
    parser.add_argument("-v", "--verb", type=str, help="Verb for custom chart")
    parser.add_argument("-set", "--settings", action="store_true", help="Toggle settings interactively")
    
    # Override flags
    parser.add_argument("--no-logo", action="store_true", help="Disable logo for this run")
    parser.add_argument("--no-color", action="store_true", help="Disable colors for this run")
    parser.add_argument("--no-format", action="store_true", help="Disable formatting for this run")
    parser.add_argument("--no-unicode", action="store_true", help="Disable unicode outlines for this run")

    args = parser.parse_args()
    
    if args.settings:
        while handle_settings(settings):
            pass
        sys.exit(0)

    # Apply temporary CLI overrides
    if args.no_logo: settings["logo"] = False
    if args.no_color: settings["colors"] = False
    if args.no_format: settings["formatting"] = False
    if args.no_unicode: settings["unicode"] = False

    if (args.subject and not args.verb) or (args.verb and not args.subject):
        parser.error("-s/--subject and -v/--verb must be used together for custom charts.")

    print_logo(logo_part1, settings)
    print_logo(logo_part2, settings)
    
    subject_verb, tenses = getTenseData(args)
    generateCharts(subject_verb, tenses, settings)

if __name__ == "__main__":
    main()