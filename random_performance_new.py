from random import *
import time
import markovify
import re
import nltk
import json
from playsound import playsound

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

# ---------------------------------------------------------------

# # This is for making a new Markov chain
# # Get raw text as string.
# with open("corpus.txt", "r") as f:
#     text = f.read()
# 
# # Build the model.
# speech_model = markovify.Text(text)
# 
# model_json = speech_model.to_json()
# 
# with open("exxon_model.json", "w") as f:
#     f.write(model_json)

# ---------------------------------------------------------------

# This is for loading an old Markov chain
with open("tcp_model.json", "r") as f:
    model_json = f.read()

unison_model = markovify.Text.from_json(model_json)

# ---------------------------------------------------------------

speech_models = []
model_names = ["shelley_model.json", "austen_model.json", "zuboff_model.json", "marx_model.json", "heidegger_model.json", "foucault_model.json", "exxon_model.json", "hamlet_model.json", "google_model.json"]

for name in model_names:
    with open(name, "r") as f:
        model_json = f.read()
    speech_model = markovify.Text.from_json(model_json)
    speech_models.append(speech_model);


# Interesting functions
# text_model.make_sentence()
# make_short_sentence(self, max_chars, min_chars=0, **kwargs):
# make_sentence_with_start(self, beginning, strict=True, **kwargs):

# Number of nodes
chorus_size = 6

shuffle(speech_models)

# Possible commands. Movement and monologue have a greater probability of being picked
commands = ["dialogue", "dialogue", "monologue", "scan", "scan", "verbose", "verbose", "literal", "copy", "louder", "softer", "unison", "return to backstage", "movement", "movement", "movement", "movement", "movement"]

# Commands that can be done in unison
unison_commands = ["monologue", "scan", "verbose", "literal", "movement", "movement", "movement"]

# Possible movements. All have equal probability to be picked, except for "Dab."

movements_object = [
"Become a %s", # Object
"Struggle with a %s" # Object
]

movements_escape = [
"Escape the %s", # Escape object
"Get stuck in the %s" # Escape object
]

movements_two_objects = [
"Oscillate between %s and %s", # Object and object
]

movements_emotion = [
"Realize you are %s", # Emotion
"lay down and maintain eye contact with phone despite %s" # Emotion
]

movements_two_emotions = [
"Oscillate between %s and %s", # Emotion and emotion
"Show both %s and %s"
]

movements_all = [
"Dab.",
"Do anything that makes it hard to breathe.",
"Find your breath. Breathe.",
"awkward turtle",
"laughing while crying emoji",
"me gusta meme",
"become furniture",
"you are a mime stuck in a box"
] + movements_emotion + movements_two_emotions + movements_two_objects + movements_escape + movements_object

emotions = [
"anger",
"joy",
"paranoia",
"sadness",
"love",
"jealousy",
"sloth",
"illness",
"amusement",
"kindness"
]

# Possible emotions. All have equal probability to be picked
emotions_all = [
"you have been betrayed",
"this is the best news you've ever gotten",
"sing the song of your heartbreak",
"you are a doctor. break the bad news gently",
"convince me",
"squish the audience with your words",
"you're a stand-up comedian",
"you're giving safety instructions",
"question your convictions"] + emotions

objects_escape = ["net", "skin", "mud", "last dream that you can remember"]

# Possible objects. All have equal probability to be picked
objects_all = ["PDF", "favorite writing tool", "plastic fork", "fidget spinner", "computer mouse", "bacteria"] + objects_escape

noises = [
"Wind blowing",
"Coughing",
"A clock ticking",
"Waves",
"Slow humming",
"Cheerful humming",
"Bird chirps",
"Cars passing by"
]

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
            shuffle(emotions_all)
            print("All nodes in unison -- " + unison_commands[0] + ". Emotion -- " + emotions_all[0])
            time.sleep(4.5)
            new_monologue = ""
            for i in range(randint(2, 5)):
                new_monologue += unison_model.make_short_sentence(140)
                new_monologue += " "
            new_monologue = new_monologue.split(" ")
            for i in range(0, len(new_monologue)):
                print(new_monologue[i])
                time.sleep(0.5)
            time.sleep(1)
        else:
            if(unison_commands[0] == "literal" or unison_commands[0] == "verbose"):
                shuffle(objects_all)
                shuffle(emotions_all)
                print("All nodes in unison -- " + unison_commands[0] + " " + objects_all[0] + ". Emotion -- " + emotions_all[0])
            if(unison_commands[0] == "scan"):
                shuffle(emotions_all)
                print("All nodes in unison -- " + unison_commands[0] + ". Emotion -- " + emotions_all[0])
            if(unison_commands[0] == "movement"):
                shuffle(movements_all)
                while(movements_all[0] == "Dab."):
                    if(randint(0,5) == 3):
                        break
                    shuffle(movements_all)
                if(movements_all[0] in movements_object):
                    shuffle(objects_all)
                    print("All nodes in unison –- " + (movements_all[0] % objects_all[0]))
                elif(movements_all[0] in movements_escape):
                    shuffle(objects_escape)
                    print("All nodes in unison –- " + (movements_all[0] % objects_escape[0]))
                elif(movements_all[0] in movements_emotion):
                    shuffle(emotions)
                    print("All nodes in unison –- " + (movements_all[0] % emotions[0]))
                elif(movements_all[0] in movements_two_emotions):
                    shuffle(emotions)
                    print("All nodes in unison –- " + (movements_all[0] % (emotions[0], emotions[1])))
                elif(movements_all[0] in movements_two_objects):
                    shuffle(objects_all)
                    print("All nodes in unison –- " + (movements_all[0] % (objects_all[0], objects_all[1])))
                else:
                    print("All nodes in unison –- " + movements_all[0])
            time.sleep(unison_time)
        playsound('beep-07.mp3')
        print("All nodes in unison -- Return to backstage")
        for i in range(1, chorus_size+1):
            chorus_states[i] = "phone"
        time.sleep(1)
        issued_command = 1

    # If monologue picked, one node recites monologue one word at a time
    if(commands[0] == "monologue"):
        shuffle(emotions_all)
        playsound('beep-07.mp3')
        print("Node #" + str(node_number) + " –- " + commands[0] + ". Emotion -- " + emotions_all[0])
        if(randint(1,2) == 1):
            node_number2 = randint(1, chorus_size)
            while node_number2 == node_number:
                node_number2 = randint(1, chorus_size)
            shuffle(noises)
            time.sleep(3)
            playsound('beep-07.mp3')
            print("Node #" + str(node_number2) + " –- Give the monologue background sound -- " + noises[0])
        # Thought: More time to get ready before monologue?
        time.sleep(4.5)
        new_monologue = ""
        for i in range(randint(2, 5)):
            new_monologue += speech_models[node_number % len(speech_models)].make_short_sentence(140)
            new_monologue += " "
        new_monologue = new_monologue.split(" ")
        for i in range(0, len(new_monologue)):
            print(new_monologue[i])
            time.sleep(0.5)
        for i in range(1, chorus_size+1):
            chorus_states[i] = "phone"
        # Thought: Remove wait for action to resume after monologue?
        # Or have action resume after monologue
        time.sleep(1)
        issued_command = 1

    if(commands[0] == "dialogue"):
        node_number2 = randint(1, chorus_size)
        while node_number2 == node_number:
            node_number2 = randint(1, chorus_size)
        playsound('beep-07.mp3')
        print("Node #" + str(node_number) + " and Node #" + str(node_number2) + " –- " + commands[0])
        time.sleep(3)
        shuffle(emotions_all)
        print("Node #" + str(node_number) + " -- Emotion -- " + emotions_all[0])
        time.sleep(3)
        shuffle(emotions_all)
        print("Node #" + str(node_number2) + " -- Emotion -- " + emotions_all[0])
        if(randint(1,2) == 1):
            node_number3 = randint(1, chorus_size)
            while node_number3 == node_number or node_number3 == node_number2:
                node_number3 = randint(1, chorus_size)
            shuffle(noises)
            time.sleep(3.5)
            playsound('beep-07.mp3')
            print("Node #" + str(node_number3) + " –- Give the dialogue background sound -- " + noises[0])
        # Thought: More time to get ready before dialogue?
        time.sleep(4.5)
        for i in range(randint(3, 5)):
            new_line = ""
            if(i % 2 == 0):
                for i in range(randint(1, 2)):
                    new_line += speech_models[node_number % len(speech_models)].make_short_sentence(115)
                    new_line += " "
                new_line = new_line.split(" ")
                print("-------- Node #" + str(node_number))
                time.sleep(0.5)
                for i in range(0, len(new_line)):
                    print(new_line[i])
                    time.sleep(0.5)
            else:
                for i in range(randint(1, 2)):
                    new_line += speech_models[node_number2  % len(speech_models)].make_short_sentence(115)
                    new_line += " "
                new_line = new_line.split(" ")
                print("-------- Node #" + str(node_number2))
                time.sleep(0.5)
                for i in range(0, len(new_line)):
                    print(new_line[i])
                    time.sleep(0.5)
        for i in range(1, chorus_size+1):
            chorus_states[i] = "phone"
        time.sleep(1)
        issued_command = 1

    # Tells the selected node to scan and sets them to active
    if(commands[0] == "scan"):
        shuffle(emotions_all)
        playsound('beep-07.mp3')
        print("Node #" + str(node_number) + " –- " + commands[0] + ". Emotion -- " + emotions_all[0])
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
        shuffle(objects_all)
        shuffle(emotions_all)
        playsound('beep-07.mp3')
        print("Node #" + str(node_number) + " –- " + commands[0] + " " + objects_all[0] + ". Emotion -- " + emotions_all[0])
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
        shuffle(movements_all)
        while(movements_all[0] == "Dab."):
            if(randint(0,5) == 3):
                break
            shuffle(movements_all)
        playsound('beep-07.mp3')
        if(movements_all[0] in movements_object):
            shuffle(objects_all)
            print("Node #" + str(node_number) + " –- " + (movements_all[0] % objects_all[0]))
        elif(movements_all[0] in movements_escape):
            shuffle(objects_escape)
            print("Node #" + str(node_number) + " –- " + (movements_all[0] % objects_escape[0]))
        elif(movements_all[0] in movements_emotion):
            shuffle(emotions)
            print("Node #" + str(node_number) + " –- " + (movements_all[0] % emotions[0]))
        elif(movements_all[0] in movements_two_emotions):
            shuffle(emotions)
            print("Node #" + str(node_number) + " –- " + (movements_all[0] % (emotions[0], emotions[1])))
        elif(movements_all[0] in movements_two_objects):
            shuffle(objects_all)
            print("Node #" + str(node_number) + " –- " + (movements_all[0] % (objects_all[0], objects_all[1])))
        else:
            print("Node #" + str(node_number) + " –- " + movements_all[0])
        chorus_states[node_number] = "moving"
        issued_command = 1

    if issued_command:
        # Wait time before issuing another command
        wait = randint(loop_delay_min, loop_delay_max)
        time.sleep(wait)
        # Thought increase chance of unison near end of performance
        # if (time.time() - start_time) > ((max_time / 3) * 2):
        #     commands.append("unison")
        # Thought: Can safely remove this?
        # 2% chance of quiting
        # if(randint(0,50) == 25):
        #     exit = 1
