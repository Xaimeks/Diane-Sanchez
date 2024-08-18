import psutil as ps 
import time
from run_templates import templates

def all_proc():
  for proc in ps.process_iter(['pid', 'name', 'username']):
    try:
      print(f'PID: {proc.info['pid']}, Name: {proc.info['name']}, User: {proc.info['username']}')
    except (ps.NoSuchProcess, ps.AccessDenied, ps.ZombieProcess):
      print('Oops..')
      
# new process monitoring
def monitor_new_process(callback):
  prev_proc = set(p.info['pid'] for p in ps.process_iter(['pid']))
  processed_names = set()
    
  while True:
    
    time.sleep(1)
    curr_proc = set(p.info['pid'] for p in ps.process_iter(['pid']))
    new_proc = curr_proc - prev_proc
      
    for element in new_proc:
      process = ps.Process(element)
      proc_name = process.name()
      
      if proc_name not in processed_names:
        processed_names.add(proc_name)
        callback(proc_name)
        
    prev_proc = curr_proc
    
def new_process_handler(name):
  print(f'New Process: {name}')
  task_templates(name)
    
def task_templates(proc_name):   
  if proc_name in templates:
    for message in templates[proc_name]:
      print(message)
  


all_proc()
monitor_new_process(new_process_handler)