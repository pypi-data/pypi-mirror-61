
import argparse 
  
def main(): 
  
    parser = argparse.ArgumentParser(prog ='hitsquad', 
                                     description ='sshpass based stuff') 
    parser.add_argument('--ipfile', help='file with <ip,pass> pairs on different rows',required=True)
    parser.add_argument('--command', help='command to run',required=True)
    args = parser.parse_args() 
    
    print(args.ipfile,args.command)

