from Crypto.Util.number import bytes_to_long
from secret import LotteryCenter, FLAG
import signal

def handler1(signum, frame):
    raise TimeoutError("You took too long to make a decision. The boss is not patient.")
def handler2(signum, frame):
    e = '''
Before I can react, a heavy hand clamps onto my shoulder. The boss's face is dark with rage. "What the hell did you do?!"
I stammer, "I just thought the numbers could be luckier..."
"OUT!" he roars, dragging me toward the door. "And don't come back unless you've got the money to replace this thing!"
'''
    raise TimeoutError(e)

x = bytes_to_long(FLAG)
assert x.bit_length() <= 512

descrption = """
You step into the Lottery Center, the bell above the door rings softly as you enter. The air is stale, with an old fan humming above. The walls are lined with lottery posters and flashing numbers. At the counter, a middle-aged man in a dark suit is busy sorting through some papers, unaware of your presence.

The atmosphere is quiet and slightly unsettling. You glance around the room — a corner has an old lottery machine, still occasionally making a "clicking" noise. There's a poster on the wall showing today's lucky numbers, but they seem somewhat blurry.
"""

print(descrption)

lotteryCenter = LotteryCenter()

menu = """
You're left with a few choices:
1. Talk to the Boss.
2. Pick Your Lucky Number.
3. Choose Your Bet Size.
4. Look Around.
"""

signal.signal(signal.SIGALRM, handler1)
signal.alarm(600)

while 1:
    print(menu)
    choice = input("What do you do? ")
    if choice == "1":
        # Choose my favourite number.
        print(f"You approach the counter. The boss looks up briefly, then says in a low voice, \"Today's lucky number is {lotteryCenter.P}. Trust it, it will bring good luck.\"")
    elif choice == "2":
        g = int(input("You decide to pick your own lucky number: "))
        if lotteryCenter.defineG(g):
            print("You successfully pick your lucky number.")
        else:
            print("You can't pick that number.")
    elif choice == "3":
        if lotteryCenter.g==None:
            print("You should pick your lucky number first.")
        else:
            times = int(input("You decide to pick your bet size: "))
            assert times>0
            ticket = lotteryCenter.tetration(times, x)
            # Calculate the tetration g^g^...^g(times)^x.
            # For example, P=23, g=3, tetration(3, 2) = 3^(3^(3^2)) % 23 = 12.
            print(f"You take the ticket with the number {ticket} from the machine, feeling a slight chill in the air. The boss looks at you for a moment longer, his expression unreadable. Then, with a slow smile, he finally speaks, his voice low but clear:")
            print("\"Good luck... I hope today is your lucky day.\"")
            break
    elif choice == "4":
        print("The boss seems distracted — perhaps counting cash or sorting through stacks of old receipts, his back turned just enough. Seizing the moment, I slip around to the back of the lottery machine, my fingers hovering over the controls. A quiet smirk tugs at my lips as I mutter under my breath ...")
        lotteryCenter.P = int(input("I don't think the boss's lucky number is lucky enough: "))
        assert lotteryCenter.P>1
        x = int(input("\"Yes!\" I whisper, overriding the preset algorithm with my own: "))
        g = int(input("You decide to pick your own lucky number: "))
        times = int(input("You decide to pick your bet size: "))
        assert times>0
        signal.signal(signal.SIGALRM, handler2)
        signal.alarm(10)
        try:
            if lotteryCenter.defineG(g):
                ticket = lotteryCenter.tetration(times, x)
                print(f"You take the ticket with the number {ticket} from the machine secretly.")
            else:
                print("Oops! The lottery machine whirs weakly as I finish tampering with its settings — then suddenly, the screen flickers violently before dying with a pathetic click. A thin wisp of smoke curls from the vents.")
        except TimeoutError as e:
            print(e)
        finally:
            signal.alarm(0)
        break
    else:
        print("Nothing here.")

print("\nYou exit the Lottery Center, the door closing softly behind you. The bell rings once more, leaving you standing outside, holding the ticket — unsure if you've just stepped into a stroke of luck... or something else entirely.")