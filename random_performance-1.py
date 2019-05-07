from random import *
import time
from playsound import playsound

# Number of nodes
chorus_size = 4

# Possible objects. All have equal probability to be picked
objects = ["PDF", "your favorite writing tool", "plastic fork", "fidget spinner", "the last dream that you can remember"]

# Possible commands. Movement and monologue have a greater probability of being picked
commands = ["monologue", "monologue", "scan", "verbose", "literal", "copy", "louder", "softer", "unison", "return to backstage", "movement", "movement", "movement", "movement"]

# Commands that can be done in unison
unison_commands = ["monologue", "scan", "verbose", "literal", "movement", "movement", "movement"]

# Possible monologues. All have equal probability to be picked
# Thought: Some monologues might be too long. Gertrude Stein is over 2 minutes of a performance with 4 active minutes
monologues_texts = ["Philosophers can never hope finally to formulate these metaphysical first principles. Weakness of insight and deficiencies of language stand in the way inexorably. Words and phrases must be stretched towards a generality foreign to their ordinary usage; and however such elements of language be stabilized as technicalities, they remain metaphors mutely appealing for an imaginative leap.",
"Both linear and dialectical causality no longer function, therefore everything is in determination. The center of meaning is empty, therefore we are satellites in lost orbit. We can no longer act like legislator-subjects or be passive like slaves, therefore we are sponges. Images are no longer anchored by representation, therefore they float weightless in hyperspace. Words are no longer univocal, therefore signifiers slip chaotically over each other. A circuit has been created between the real and the imaginary, therefore reality has imploded into the undecidable proximity of hyperreality",
"Case was twenty-four. At twenty-two, he’d been a cowboy a rustler, one of the best in the Sprawl. He’d been trained by the best, by McCoy Pauley and Bobby Quine, legends in the biz. He’d operated on an almost permanent adrenaline high, a byproduct of youth and proficiency, jacked into a custom cyberspace deck that projected his disembodied consciousness into the con sensual hallucination that was the matrix. A thief he’d worked for other, wealthier thieves, employers who provided the exotic software required to penetrate the bright walls of corporate systems, opening windows into rich fields of data. He’d made the classic mistake, the one he’d sworn he’d never make. He stole from his employers.",
"One. In the ample checked fur in the back and in the house, in the by next cloth and inner, in the chest, in mean wind. One. In the best most silk and water much, in the best most silk. One. In the best might last and wind that. In the best might last and wind in the best might last. Ages, ages, all what sat. One. In the gold presently, in the gold presently unsuddenly and decapsized and dewalking. In the gold coming in. Two. A touching white shining sash and a touching white green undercoat and a touching white colored orange and a touching piece of elastic. A touching piece of elastic suddenly. A touching white inlined ruddy hurry, a touching research in all may day. A touching research is an over show. A touching expartition is in an example of work, a touching beat is in the best way. A touching box is in a coach seat so that a touching box is on a coach seat so a touching box is on a coach seat, a touching box is on a coat seat, a touching box is on a coach seat. A touching box is on the touching so helping held. Two. Any left in the touch is a scene, a scene. Any left in is left somehow. Four. Four between, four between and hacking. Four between and hacking. Five. Four between and a saddle, a kind of dim judge and a great big so colored dog."]
monologues = []

# Possible emotions. All have equal probability to be picked
emotions = ["realize you are angry," "you have been betrayed", "this is the best news you've ever gotten", "sing the song of your heartbreak", "you are disconsolate", "resigned", "hopeless", "radiate kindness", "you are a doctor. break the bad news gently", "convince me", "squish the audience with your words" ]

# Possible movements. All have equal probability to be picked, except for "Dab."
movements = [
"Dab.",
"Escape your skin.",
"Get stuck in the net.",
"Do anything that makes it hard to breathe.",
"Find your breath. Breathe.",
"Lay down and look at your phone.",
"Explore the most uncomfortable way to look at your phone. Maintain eye contact with phone at all costs.",
"Oscillate between \"phone posture\" and \"good posture.\"",
"awkward turtle",
"laughing while crying emoji",
"me gusta meme",
"become furniture"
]

# Prepares the monologues to be read one word at a time
for monologue_text in monologues_texts:
    monologue = monologue_text.split(" ")
    monologues.append(monologue)

# Array of what nodes are currently doing
chorus_states = ["Empty"]
for i in range(1, chorus_size+1):
    chorus_states.append("phone")

# Times in seconds
initial_delay_min = 30
initial_delay_max = 90
unison_time = 15
loop_delay_min = 5
loop_delay_max = 15

# Maximum amount of time the program will run
max_time = 480

# Set's start time to when the for loop begins
start_time = time.time()

# Initial delay
wait = randint(initial_delay_min, initial_delay_max)
time.sleep(wait)

# Integer used to exit the main while loop
exit = 0

while(exit == 0 and (time.time() - start_time) < max_time):
    # Picks a random command and node
    shuffle(commands)
    node_number = randint(1, chorus_size)
    issued_command = 0
    
    # If unison picked, all nodes complete a unison action together
    # Then, all return to phones once finished.
    # Thoughts: I'm not sure how well this works with literal, verbose, and scan.
    # Also, there is currently a fixed time of 15 secs for unison actions other than monologue, but this could be random changed
    if(commands[0] == "unison"):
        shuffle(unison_commands)
        playsound('beep-07.mp3')
        if(unison_commands[0] == "monologue"):
            shuffle(monologues)
            shuffle(emotions)
            print("All nodes in unison -- " + unison_commands[0] + ". Emotion -- " + emotions[0])
            time.sleep(2)
            for i in range(0, len(monologues[0])):
                print(monologues[0][i])
                time.sleep(0.5)
            time.sleep(1)
        else:
            if(unison_commands[0] == "literal" or unison_commands[0] == "verbose"):
                shuffle(objects)
                print("All nodes in unison -- " + unison_commands[0] + " " + objects[0])
            if(unison_commands[0] == "scan"):
                print("All nodes in unison -- " + unison_commands[0])
            if(unison_commands[0] == "movement"):
                shuffle(movements)
                while(movements[0] == "Dab."):
                    if(randint(0,5) == 3):
                        break
                    shuffle(movements)
                print("All nodes in unison -- " + movements[0])
            time.sleep(unison_time)
        playsound('beep-07.mp3')
        print("All nodes in unison -- Return to backstage")
        for i in range(1, chorus_size+1):
            chorus_states[i] = "phone"
        time.sleep(1)
        issued_command = 1

    # If monologue picked, one node recites monologue one word at a time
    if(commands[0] == "monologue"):
        shuffle(monologues)
        shuffle(emotions)
        playsound('beep-07.mp3')
        print("Node #" + str(node_number) + " –- " + commands[0] + ". Emotion -- " + emotions[0])
        time.sleep(2)
        for i in range(0, len(monologues[0])):
            print(monologues[0][i])
            time.sleep(0.5)
        for i in range(1, chorus_size+1):
            chorus_states[i] = "phone"
        time.sleep(1)
        issued_command = 1
    
    # Tells the selected node to scan and sets them to active
    # Thoughts: This setup will probably lead to lengthier scans than we've been doing
    if(commands[0] == "scan"):
        playsound('beep-07.mp3')
        print("Node #" + str(node_number) + " –- " + commands[0])
        chorus_states[node_number] = "active"
        issued_command = 1
        
    # If a node is active and "return to backstage", "softer", or "louder"
    # selected, issues command to random active node
    if((commands[0] == "return to backstage" or commands[0] == "louder" or commands[0] == "softer") and "active" in chorus_states):
        while(chorus_states[node_number] != "active"):
            node_number = randint(1, chorus_size)
        playsound('beep-07.mp3')
        print("Node #" + str(node_number) + " –- " + commands[0])
        # If returning to backstage, sets state to "phone"
        if(commands[0] == "return to backstage"):
            chorus_states[node_number] = "phone"
        issued_command = 1
            
    # Tells selected node to literal or verbose a random object
    # Thoughts: Can have two nodes working on same object at once
    if(commands[0] == "verbose" or commands[0] == "literal"):
        shuffle(objects)
        playsound('beep-07.mp3')
        print("Node #" + str(node_number) + " –- " + commands[0] + " " + objects[0])
        chorus_states[node_number] = "active"
        issued_command = 1
        
    # Picks random active node and tells a different node to copy it
    # Thoughts: Can now copy scan, just for simplicity
    if(commands[0] == "copy" and "active" in chorus_states):
        target_number = randint(1, chorus_size)
        while(chorus_states[target_number] != "active"):
            target_number = randint(1, chorus_size)
        while node_number == target_number:
            node_number = randint(1, chorus_size)
        playsound('beep-07.mp3')
        print("Node #" + str(node_number) + " –- " + commands[0] + " Node #" + str(target_number))
        chorus_states[node_number] = "copying"
        issued_command = 1

    if(commands[0] == "movement"):
        shuffle(movements)
        while(movements[0] == "Dab."):
            if(randint(0,5) == 3):
                break
            shuffle(movements)
        playsound('beep-07.mp3')
        print("Node #" + str(node_number) + " –- " + movements[0])
        chorus_states[node_number] = "moving"
        issued_command = 1
    
    if issued_command:
        # Wait time before issuing another command
        wait = randint(loop_delay_min, loop_delay_max)
        time.sleep(wait)
        
        # 2% chance of quiting
        if(randint(0,50) == 25):
            exit = 1
