import psutil as ps 
import time
from run_templates import templates
from gtts import gTTS
import pygame 

def all_proc():
  for proc in ps.process_iter(['pid', 'name', 'username']):
    try:
      print(f'PID: {proc.info['pid']}, Name: {proc.info['name']}, User: {proc.info['username']}')
    except (ps.NoSuchProcess, ps.AccessDenied, ps.ZombieProcess):
      print('Oops..')
      
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
            processed_names.add(proc_name)
            callback(proc_name)
              
        except (ps.NoSuchProcess, ps.AccessDenied, ps.ZombieProcess) as e:
          print(f'Error {element}: {e}')      
          
      if time.time() % 1 < 1:
        clear_callback(processed_names)
              
              
        prev_proc = curr_proc
        
        
    except Exception as e:
      print(f"Error: {e}")
      
def new_process_handler(name):
  print(f'New Process: {name}')
  task_templates(name, text_to_speech)
  
    
def task_templates(proc_name, callback):   
  if proc_name in templates:
    for message in templates[proc_name]:
      callback(message)
  
def text_to_speech(message):
  language = 'en'
  my_obj = gTTS(text=message, lang=language, slow=False)
  my_obj.save('voice.mp3')
  
  # change someday
  pygame.mixer.init()
  pygame.mixer.music.load('voice.mp3')
  pygame.mixer.music.play()
  
  while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
    
  pygame.mixer.music.stop()
  pygame.mixer.quit()
  # os.remove(voice.mp3)

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
        
    


all_proc()
monitor_new_process(new_process_handler, proc_names_clear_handler)
