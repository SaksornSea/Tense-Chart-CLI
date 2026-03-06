import requests
import sys
import json
import argparse

logo_part1 = r'''
 ______                               ____     __                       __      
/\__  _\                             /\  _`\  /\ \                     /\ \__   
\/_/\ \/    __    ___     ____     __\ \ \/\_\\ \ \___      __     _ __\ \ ,_\  
   \ \ \  /'__`\/' _ `\  /',__\  /'__`\ \ \/_/_\ \  _ `\  /'__`\  /\`'__\ \ \/  
    \ \ \/\  __//\ \/\ \/\__, `\/\  __/\ \ \L\ \\ \ \ \ \/\ \L\.\_\ \ \/ \ \ \_ 
     \ \_\ \____\ \_\ \_\/\____/\ \____\\ \____/ \ \_\ \_\ \__/.\_\\ \_\  \ \__\
      \/_/\/____/\/_/\/_/\/___/  \/____/ \/___/   \/_/\/_/\/__/\/_/ \/_/   \/__/
'''

# rainbow!
colors = [
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

def print_colored_logo(text):
    lines = text.strip('\n').split('\n')
    for line in lines:
        colored_line = ""
        for i, (start, end) in enumerate(slices):
            chunk = line[start:end]
            colored_line += f"{colors[i]}{chunk}{reset}"
        print(colored_line)

logo_part2 = r'''
 ____     __     ______                                                         
/\  _`\  /\ \   /\__  _\                                                        
\ \ \/\_\\ \ \  \/_/\ \/                                                        
 \ \ \/_/_\ \ \  __\ \ \                                                        
  \ \ \L\ \\ \ \L\ \\_\ \__                                                     
   \ \____/ \ \____//\_____\                                                    
    \/___/   \/___/ \/_____/                                                                                                      
'''

def getTenseData(args):
    params = {}
    if args.random:
        params['random'] = 'true'
    elif args.subject and args.verb:
        params['subject'] = args.subject
        params['verb'] = args.verb
    else:
        # Default to daily
        params['daily'] = 'true'

    response = requests.get("https://sea.navynui.cc/tensechart/api/index.php", params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract metadata [subject, verb]
        subject_verb = [data['metadata']['subject'], data['metadata']['verb']]
    
        # Extract all tenses in row-major order (Aspect then Time)
        tenses = []
        for voice in ["active", "passive"]:
            for aspect in ["simple", "perfect", "continuous", "perfect_continuous"]:
                for time in ["past", "present", "future"]:
                    tenses.append(data[voice][time][aspect])

        return subject_verb, tenses
    
    else:
        print(f"Server-side Error: http code {response.status_code}")
        sys.exit(0)

def generateCharts(subject_verb, tenses):
    # Subject-verb box
    boxLenght = len(subject_verb[0]) + len(subject_verb[1]) + 6
    print("╭" + "─" * boxLenght + "╮")
    print("│  " + subject_verb[0] + "  " + subject_verb[1] + "  │")
    print("╰" + "─" * boxLenght + "╯")

    # Use the longest tense for padding
    pastLenght = len(tenses[21]) + 2
    presentLenght = len(tenses[22]) + 2
    futureLenght = len(tenses[23]) + 2 

    topPastlenght = pastLenght - 7
    topPresentlenght = presentLenght - 10
    topFuturelenght = futureLenght - 9

    # Active chart
    print("╭" + "─" * 20 + "┬" + "─" * pastLenght + "┬" + "─" * presentLenght + "┬" + "─" * futureLenght + "╮")
    print("│ Active             │ Past " + " " * topPastlenght + " │ Present " + " " * topPresentlenght + " │ Future " + " " * topFuturelenght + " │")
    print("├" + "─" * 20 + "┼" + "─" * pastLenght + "┼" + "─" * presentLenght + "┼" + "─" * futureLenght + "┤")
    print("│ Simple             │ " + tenses[0] + " " * (len(tenses[21]) - len(tenses[0])) + " │ " + tenses[1] + " " * (len(tenses[22]) - len(tenses[1])) + " │ " + tenses[2] + " " * (len(tenses[23]) - len(tenses[2])) + " │")
    print("├" + "─" * 20 + "┼" + "─" * pastLenght + "┼" + "─" * presentLenght + "┼" + "─" * futureLenght + "┤")
    print("│ Perfect            │ " + tenses[3] + " " * (len(tenses[21]) - len(tenses[3])) + " │ " + tenses[4] + " " * (len(tenses[22]) - len(tenses[4])) + " │ " + tenses[5] + " " * (len(tenses[23]) - len(tenses[5])) + " │")
    print("├" + "─" * 20 + "┼" + "─" * pastLenght + "┼" + "─" * presentLenght + "┼" + "─" * futureLenght + "┤")
    print("│ Continuous         │ " + tenses[6] + " " * (len(tenses[21]) - len(tenses[6])) + " │ " + tenses[7] + " " * (len(tenses[22]) - len(tenses[7])) + " │ " + tenses[8] + " " * (len(tenses[23]) - len(tenses[8])) + " │")
    print("├" + "─" * 20 + "┼" + "─" * pastLenght + "┼" + "─" * presentLenght + "┼" + "─" * futureLenght + "┤")
    print("│ Perfect Continuous │ " + tenses[9] + " " * (len(tenses[21]) - len(tenses[9])) + " │ " + tenses[10] + " " * (len(tenses[22]) - len(tenses[10])) + " │ " + tenses[11] + " " * (len(tenses[23]) - len(tenses[11])) + " │")
    print("╰" + "─" * 20 + "┴" + "─" * pastLenght + "┴" + "─" * presentLenght + "┴" + "─" * futureLenght + "╯")

    # Passive chart
    print("╭" + "─" * 20 + "┬" + "─" * pastLenght + "┬" + "─" * presentLenght + "┬" + "─" * futureLenght + "╮")
    print("│ Passive            │ Past " + " " * topPastlenght + " │ Present " + " " * topPresentlenght + " │ Future " + " " * topFuturelenght + " │")
    print("├" + "─" * 20 + "┼" + "─" * pastLenght + "┼" + "─" * presentLenght + "┼" + "─" * futureLenght + "┤")
    print("│ Simple             │ " + tenses[12] + " " * (len(tenses[21]) - len(tenses[12])) + " │ " + tenses[13] + " " * (len(tenses[22]) - len(tenses[13])) + " │ " + tenses[14] + " " * (len(tenses[23]) - len(tenses[14])) + " │")
    print("├" + "─" * 20 + "┼" + "─" * pastLenght + "┼" + "─" * presentLenght + "┼" + "─" * futureLenght + "┤")
    print("│ Perfect            │ " + tenses[15] + " " * (len(tenses[21]) - len(tenses[15])) + " │ " + tenses[16] + " " * (len(tenses[22]) - len(tenses[16])) + " │ " + tenses[17] + " " * (len(tenses[23]) - len(tenses[17])) + " │")
    print("├" + "─" * 20 + "┼" + "─" * pastLenght + "┼" + "─" * presentLenght + "┼" + "─" * futureLenght + "┤")
    print("│ Continuous         │ " + tenses[18] + " " * (len(tenses[21]) - len(tenses[18])) + " │ " + tenses[19] + " " * (len(tenses[22]) - len(tenses[19])) + " │ " + tenses[20] + " " * (len(tenses[23]) - len(tenses[20])) + " │")
    print("├" + "─" * 20 + "┼" + "─" * pastLenght + "┼" + "─" * presentLenght + "┼" + "─" * futureLenght + "┤")
    print("│ Perfect Continuous │ " + tenses[21] + " │ " + tenses[22] + " │ " + tenses[23] + " │")
    print("╰" + "─" * 20 + "┴" + "─" * pastLenght + "┴" + "─" * presentLenght + "┴" + "─" * futureLenght + "╯")



def main():
    parser = argparse.ArgumentParser(description="The Daily Tense Charts, now in your terminal!")
    parser.add_argument("-d", "--daily", action="store_true", help="Get today's tense chart")
    parser.add_argument("-r", "--random", action="store_true", help="Get a random tense chart")
    parser.add_argument("-s", "--subject", type=str, help="Subject for custom chart")
    parser.add_argument("-v", "--verb", type=str, help="Verb for custom chart")
    
    args = parser.parse_args()
    
    if (args.subject and not args.verb) or (args.verb and not args.subject):
        parser.error("-s/--subject and -v/--verb must be used together for custom charts.")

    print_colored_logo(logo_part1)
    print_colored_logo(logo_part2)
    
    subject_verb, tenses = getTenseData(args)
    generateCharts(subject_verb, tenses)

if __name__ == "__main__":
    main()