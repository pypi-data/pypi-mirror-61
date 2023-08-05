import subprocess
import argparse 

def main(): 
  
    parser = argparse.ArgumentParser(prog ='hitsquad', 
                                     description ='sshpass based stuff') 
    parser.add_argument('--ipfile', help='file with <ip,pass> pairs on different rows',required=True)
    parser.add_argument('--command', help='command to run',required=True)
    args = parser.parse_args()
    sshpass = "/".join(__file__.split("/")[:-1])+"/sshpass"
    f = open(args.ipfile,"r")
    for row in f.readlines():
        if not row:
            continue
        print(row)
        (ip,password) = row.strip().split(",")
        print(ip,password)
        print("----- {} -----".format(ip))
        subprocess.call("{} -p {} ssh {} {}".format(sshpass,password,ip,args.command),shell=True)