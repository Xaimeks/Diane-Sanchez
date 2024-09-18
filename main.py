import psutil as ps 
import time
from run_templates import templates
import pygame
from eleven_labs import eleven_labs_tts
from dotenv import load_dotenv
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import random

load_dotenv()
api_key = os.getenv('ELEVEN_LABS_API_KEY')

# new process monitoring
def monitor_new_process(callback, clear_callback):
  prev_proc = set(p.info['pid'] for p in ps.process_iter(['pid']))
  processed_names = set()
    
  while True:
    try:
      time.sleep(1)
      curr_proc = set(p.info['pid'] for p in ps.process_iter(['pid']))
      new_proc = curr_proc - prev_proc
        
      for element in new_proc:
        try:
          process = ps.Process(element)
          proc_name = process.name()
            
          if proc_name not in processed_names:
            time.sleep(3)
            processed_names.add(proc_name)
            callback(proc_name)

        except (ps.NoSuchProcess, ps.AccessDenied, ps.ZombieProcess) as e:
          print(f'Error {element}: {e}')      
          
      if time.time() % 1 < 5:
        clear_callback(processed_names)
              
      prev_proc = curr_proc
        
    except Exception as e:
      print(f"Error: {e}")
      
def new_process_handler(name):
  print(f'New Process: {name}')
  task_templates(name)
  
def task_templates(proc_name):   
  if proc_name in templates:
    message = random.choice(templates[proc_name])
    eleven_labs_tts(message)
  
    # change someday
    pygame.mixer.init()
    pygame.mixer.music.load('voice.mp3')
    pygame.mixer.music.play()
      
    while pygame.mixer.music.get_busy():
      pygame.time.Clock().tick(10)
        
    pygame.mixer.music.stop()
    pygame.mixer.quit()

def proc_names_clear_handler(names):
    print(f'Names before check: {names}')
    if len(names) == 0:
      print('Nothing clear now.')
    elif len(names) > 0:
      print(f'Names before clear. {names}')
      names.clear()
      print('Names cleared.')
    else:
      print('No names to clear')
        
        
monitor_new_process(new_process_handler, proc_names_clear_handler)
