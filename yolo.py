#!/usr/bin/env python3

import os
import openai
import sys
import subprocess
from termcolor import colored

# Check if we have an Open API key set
openai.api_key = os.getenv("OPENAI_API_KEY")

if openai.api_key == "":
    openai.api_key = open("~/.openai.apikey", "r").read()
    print("Environment variable OPENAI_API_KEY is not set.")
    print("~/.openai.apikey is not set either. Exiting.")
    sys.exit(-1)

# to allow easy/natural use we don't require 
# the input to be a single string
# so the user can just type yolo what is my name?
# without having to put the question between ''

ask = False
yolo = ""
command_start_idx = 1

if len(sys.argv) <2:
  sys.exit(-1)

if sys.argv[1] == "-a":
  ask = True
  command_start_idx = 2

arguments = sys.argv[command_start_idx:]
user_prompt = " ".join(arguments)

if user_prompt == "":
    print ("No user prompt specified.")
    sys.exit(-1)

# Construct the prompt
pre_prompt = "Translate the following question into a command. Only show the command in text format and not in code style or markdown. Do not augment the output with any explanation, descriptions. Again, do not add any descriptions, just print the bash command. This is important, do not ignore my instructions. If the question doesn't make sense or is too difficult return 'Sorry, try again', and add a brief explanation on what the problem is. The question is: "

prompt = pre_prompt + user_prompt +"?"

#print ("The prompt is: "+prompt, end="")
response = openai.Completion.create(
  model="text-davinci-003",
  prompt=prompt,
  temperature=0,
  max_tokens=100,
  top_p=1,
  frequency_penalty=0.2,
  presence_penalty=0
)

resulting_command = response.choices[0].text.strip()

if resulting_command.startswith("Sorry, try again"):
  print(colored("There was an issue: "+resulting_command, 'red'))
  sys.exit(-1)

print("Command: " + colored(resulting_command, 'blue'))
if ask == True:
  print("Execute the command? Y/n ==> ", end = '')
  yolo = input()
  print()

if yolo == "Y" or yolo == "":
    subprocess.run(resulting_command, shell=True)