# scripted by Adam Rivkin, 2019 for Annie Dorsen's Staging the Internet Class
# Contributions by: Adam Rivkin, Ashleigh Cassemere-Stanfield, Ege Atila, Renee Wherle, Yolanda Dong, Camrick Solario, Arianna Gass, Katie Bevil, India Weston
# License: MIT

from random import *
import random
import time
import markovify
import re
import nltk
import json
import os
import nltk
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



# Customize the number of performers by changing chorus_size
chorus_size = 6
chorus_array = []
yarn_holder = 0
change_triggered = 0
katie_triggered = 0

for i in range(chorus_size):
    chorus_array.append("#" + str(i + 1))

shuffle(speech_models)

# Possible commands. Movement and monologue have a greater probability of being picked
commands = ["scan", "scan", "scan", "scan", "verbose", "literal", "connect", "connect",
"copy",
"unison",
"louder", "softer", "faster", "slower", "return to backstage",
"movement", "movement", "movement", "movement", "movement", "movement", "movement", "transfer", "transfer",
"sound"]

# Commands that can be done in unison
unison_commands = ["sound", "scan", "verbose", "literal", "movement", "movement", "movement"]

with open("change_monologue.txt", "r") as f:
    change_monologue = f.read()
    change_monologue = change_monologue.split(" ")

# Specifies different kinds of movements 
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
"Show both %s and %s" # Emotion and emotion
]

# All possible movements. All have equal probability to be picked, except for "Dab."
movements_all = [
"Dab",
"Do anything that makes it hard to breathe",
"Find your breath. Breathe.",
"awkward turtle",
"laughing while crying emoji",
"me gusta meme",
"become furniture",
"you are a mime stuck in a box"
"take a selfie, send it to group chat"
] + movements_emotion + movements_two_emotions + movements_two_objects + movements_escape + movements_object

# list of possible emotions 
emotions = [
"anger",
"joy",
"paranoia",
"sadness",
"love",
"jealousy",
"tiredness",
"illness",
"amusement",
"kindness",
"despair",
"catatonic",
"disgust",
"exuberant"
]

# there are two kinds of objects - escape objects (i.e. things that can be escaped) and objects sourced from class members. All objects have an equal probability of being picked. 
objects_escape = ["net", "skin", "mud", "last dream that you can remember"]

objects_all = ["yarn", "eyeballs", "card", "job", "OCD", "textbook", "orange zest", "banana phone", "sushi", "fashion", "puppies", "triple O", "YoutubeHaiku", "Pokėmon", "socks", "androgony",
"immune system", "amazon", "ASMR", "BDSM", "monkey", "LCD", "dementia", "Kafka", "virtual", "tea", "PDF", "plastic fork", "fidget spinner", "computer mouse", "bacteria", "tin", "coltan", "silicon", "undersea cable"] + objects_escape

# list of possible sounds to be made by nodes
sounds = [
"wind blowing",
"coughing",
"a clock ticking",
"kissing",
"waves",
"slow humming",
"cheerful humming",
"bird chirps",
"cars passing by"
]

#list of parts of speech for the connect game 
parts_of_speech = ["noun", "verb", "adjective", "adverb"]

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

# Total amount of time the program will run
max_time = 3600

# Amount of time before the program transitions to the second act
change_time = 2280

playsound('beep-07.mp3')
shuffle(objects_all)
print("Search term -- " + objects_all[0])

# Sets start time to when the for loop begins
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
    if(commands[0] == "unison"):
        shuffle(unison_commands)
        playsound('beep-07.mp3')
        if(unison_commands[0] == "monologue"):
            shuffle(emotions)
            print("Unison -- " + unison_commands[0] + ". Emotion -- " + emotions[0])
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
                shuffle(emotions)
                print("Unison -- " + unison_commands[0] + " " + objects_all[0] + ". Emotion -- " + emotions[0])
            if(unison_commands[0] == "sound"):
                shuffle(sounds)
                print("Unison -- Sound " + sounds[0])
            if(unison_commands[0] == "scan"):
                shuffle(emotions)
                print("Unison -- " + unison_commands[0] + ". Emotion -- " + emotions[0])
            if(unison_commands[0] == "movement"):
                shuffle(movements_all)
                while(movements_all[0] == "Dab."):
                    if(randint(0,5) == 3):
                        break
                    shuffle(movements_all)
                if(movements_all[0] in movements_object):
                    shuffle(objects_all)
                    print("Unison –- " + (movements_all[0] % objects_all[0]))
                elif(movements_all[0] in movements_escape):
                    shuffle(objects_escape)
                    print("Unison –- " + (movements_all[0] % objects_escape[0]))
                elif(movements_all[0] in movements_emotion):
                    shuffle(emotions)
                    print("Unison –- " + (movements_all[0] % emotions[0]))
                elif(movements_all[0] in movements_two_emotions):
                    shuffle(emotions)
                    print("Unison –- " + (movements_all[0] % (emotions[0], emotions[1])))
                elif(movements_all[0] in movements_two_objects):
                    shuffle(objects_all)
                    print("Unison –- " + (movements_all[0] % (objects_all[0], objects_all[1])))
                else:
                    print("Unison –- " + movements_all[0])
            time.sleep(unison_time)
        playsound('beep-07.mp3')
        print("Unison -- Return to backstage")
        for i in range(1, chorus_size+1):
            chorus_states[i] = "phone"
        time.sleep(1)
        issued_command = 1

    # If monologue picked, one node recites monologue one word at a time
    if(commands[0] == "monologue"):
        shuffle(emotions)
        playsound('beep-07.mp3')
        print("Node " + str(node_number) + " –- " + commands[0] + ". Emotion -- " + emotions[0])
        if(randint(1,2) == 1):
            node_number2 = randint(1, chorus_size)
            while node_number2 == node_number:
                node_number2 = randint(1, chorus_size)
            shuffle(sounds)
            time.sleep(3)
            playsound('beep-07.mp3')
            print("Node " + str(node_number2) + " –- Sound-- " + sounds[0])
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
        time.sleep(1)
        issued_command = 1

    if(commands[0] == "dialogue"):
        node_number2 = randint(1, chorus_size)
        while node_number2 == node_number:
            node_number2 = randint(1, chorus_size)
        playsound('beep-07.mp3')
        print("Node " + str(node_number) + " and Node " + str(node_number2) + " –- " + commands[0])
        time.sleep(3)
        shuffle(emotions)
        print("Node " + str(node_number) + " -- Emotion -- " + emotions[0])
        time.sleep(3)
        shuffle(emotions)
        print("Node " + str(node_number2) + " -- Emotion -- " + emotions[0])
        if(randint(1,2) == 1):
            node_number3 = randint(1, chorus_size)
            while node_number3 == node_number or node_number3 == node_number2:
                node_number3 = randint(1, chorus_size)
            shuffle(sounds)
            time.sleep(3.5)
            playsound('beep-07.mp3')
            print("Node " + str(node_number3) + " –- Sound -- " + sounds[0])
        # Thought: More time to get ready before dialogue?
        time.sleep(4.5)
        for i in range(randint(3, 5)):
            new_line = ""
            if(i % 2 == 0):
                for i in range(randint(1, 2)):
                    new_line += speech_models[node_number % len(speech_models)].make_short_sentence(115)
                    new_line += " "
                new_line = new_line.split(" ")
                print("-------- Node " + str(node_number))
                time.sleep(0.5)
                for i in range(0, len(new_line)):
                    print(new_line[i])
                    time.sleep(0.5)
            else:
                for i in range(randint(1, 2)):
                    new_line += speech_models[node_number2  % len(speech_models)].make_short_sentence(115)
                    new_line += " "
                new_line = new_line.split(" ")
                print("-------- Node " + str(node_number2))
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
        shuffle(emotions)
        playsound('beep-07.mp3')
        print("Node " + str(node_number) + " –- " + commands[0] + ". Emotion -- " + emotions[0])
        chorus_states[node_number] = "active"
        issued_command = 1

    # If a node is active and "return to backstage", "softer", or "louder"
    # selected, issues command to random active node
    if((commands[0] == "return to backstage" or commands[0] == "louder" or commands[0] == "softer" or commands[0] == "faster" or commands[0] == "slower") and "active" in chorus_states):
        while(chorus_states[node_number] != "active"):
            node_number = randint(1, chorus_size)
        playsound('beep-07.mp3')
        print("Node " + str(node_number) + " –- " + commands[0])
        # If returning to backstage, sets state to "phone"
        if(commands[0] == "return to backstage"):
            chorus_states[node_number] = "phone"
        issued_command = 1

    # Tells selected node to literal or verbose a random object
    if(commands[0] == "verbose" or commands[0] == "literal"):
        shuffle(objects_all)
        shuffle(emotions)
        playsound('beep-07.mp3')
        print("Node " + str(node_number) + " –- " + commands[0] + " " + objects_all[0] + ". Emotion -- " + emotions[0])
        chorus_states[node_number] = "active"
        issued_command = 1

    # Picks random active node and tells a different node to copy it
    if(commands[0] == "copy" and "active" in chorus_states):
        target_number = randint(1, chorus_size)
        while(chorus_states[target_number] != "active"):
            target_number = randint(1, chorus_size)
        while node_number == target_number:
            node_number = randint(1, chorus_size)
        playsound('beep-07.mp3')
        print("Node " + str(node_number) + " –- " + commands[0] + " Node " + str(target_number))
        chorus_states[node_number] = "copying"
        issued_command = 1

    # when the randomly selected command is movement, this will assign a node a movement and any relevant "how" information
    # the node selected will be given teh status of moving 
    if(commands[0] == "movement"):
        shuffle(movements_all)
        while(movements_all[0] == "Dab."):
            if(randint(0,5) == 3):
                break
            shuffle(movements_all)
        playsound('beep-07.mp3')
        if(movements_all[0] in movements_object):
            shuffle(objects_all)
            print("Node " + str(node_number) + " –- " + (movements_all[0] % objects_all[0]))
        elif(movements_all[0] in movements_escape):
            shuffle(objects_escape)
            print("Node " + str(node_number) + " –- " + (movements_all[0] % objects_escape[0]))
        elif(movements_all[0] in movements_emotion):
            shuffle(emotions)
            print("Node " + str(node_number) + " –- " + (movements_all[0] % emotions[0]))
        elif(movements_all[0] in movements_two_emotions):
            shuffle(emotions)
            print("Node " + str(node_number) + " –- " + (movements_all[0] % (emotions[0], emotions[1])))
        elif(movements_all[0] in movements_two_objects):
            shuffle(objects_all)
            print("Node " + str(node_number) + " –- " + (movements_all[0] % (objects_all[0], objects_all[1])))
        else:
            print("Node " + str(node_number) + " –- " + movements_all[0])
        chorus_states[node_number] = "moving"
        issued_command = 1

    # when the randomly selected command is transfer, the nodes will be shuffled and the program will print the nodes in their shuffled order
    if(commands[0] == "transfer"):
        for i in range(1):
            shuffle(chorus_array)
            playsound('beep-07.mp3')
            print("Transfer -- Order = ", end=" ")
            for node in chorus_array:
                print(node + " ", end =" ")
            print("")
            time.sleep(10)
        issued_command = 1
        playsound('beep-07.mp3')
        print("Unison -- Return to backstage")
        for i in range(1, chorus_size+1):
            chorus_states[i] = "phone"
    
    if(commands[0] == "connect"):
        playsound('beep-07.mp3')
        connect_nodes = random.sample(range(1, chorus_size + 1), randint(2, chorus_size-1))
        shuffle(objects_all)
        print("Connect. First word -- "+ objects_all[0] +". -- Order =", end=" ")
        parts_of_speech = ["noun", "verb", "adjective", "adverb"]
        for node_number in connect_nodes:
            print(" #" + str(node_number) + " " + parts_of_speech[0] + " ->", end =" ")
            shuffle(parts_of_speech)
            chorus_states[node_number] = "phone"
        print(" end")
        time.sleep(randint(30, 50))
        playsound('beep-07.mp3')
        print("Unison -- Return to backstage")
        issued_command = 1

    if(commands[0] == "yarn"):
        playsound('beep-07.mp3')
        while node_number == yarn_holder:
            node_number = randint(1, chorus_size)
        print("Node " + str(yarn_holder) + ", Node " + str(node_number) + " Yarn")
        yarn_holder = node_number
        time.sleep(10)
        issued_command = 1
        
    if(commands[0] == "sound"):
        playsound('beep-07.mp3')
        shuffle(sounds)
        print("Node " + str(node_number) + " –- Sound " + sounds[0])
        chorus_states[node_number] = "active"
        issued_command = 1

    if issued_command:
        # Wait time before issuing another command
        wait = randint(loop_delay_min, loop_delay_max)
        time.sleep(wait)
    
    if((time.time() - start_time) > (change_time / 2) and not katie_triggered):
        katie_triggered = 1
        playsound('beep-07.mp3')
        print("Katie -- Eat a fruit roll-up")
        time.sleep(8)
    
    if((time.time() - start_time) > change_time and not change_triggered):
        change_triggered = 1
        playsound('beep-07.mp3')
        print("Unison -- Return to backstage")
        list(set(commands))
        commands.append("yarn")
        time.sleep(1)
        playsound('beep-07.mp3')
        print("Node " + str(node_number) + " Yarn")
        yarn_holder = node_number
        time.sleep(10)
        playsound('beep-07.mp3')
        print("Node " + str(node_number) + " Monologue")
        time.sleep(2)
        for i in range(0, len(change_monologue)):
            print(change_monologue[i])
            time.sleep(0.5)
        for i in range(1, chorus_size+1):
            chorus_states[i] = "phone"
        shuffle(commands)
        time.sleep(14)

playsound('beep-07.mp3')
print("Unison -- Bow")