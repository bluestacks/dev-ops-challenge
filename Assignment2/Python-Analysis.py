#!/usr/bin/env python3
##### AUTHOR - TANUJ ARORA
##### DATE - 19 July 2024

from collections import Counter

def log_analysis():
    log_file = "/Users/tanujarora/Desktop/Projects/dev-ops-challenge/Assignment2/logfile"  
    output_file = "output.txt"  

    log_dict = Counter()

    try:
        with open(log_file, 'r') as file:
            lines = file.readlines()
            for line in lines:

                ip_address = line.split()[0]
                log_dict[ip_address] += 1


        top_8_ip = log_dict.most_common(8)


        with open(output_file, 'w') as file:
            for ip, count in top_8_ip:
                file.write(f"{ip} - {count}\n")

    except FileNotFoundError:
        print("Log file not found")

if __name__ == "__main__":
    log_analysis()