import pandas as pd
import numpy as np
import re


pattern_for_comma = r'(,.*$)'
pattern_for_parenthesis = r'\s*\([^)]*\)'
pattern_for_parenthesis_number = r'[(]\d\d[)]'

sequences = []

station_counter = {}


def load_data(path):
    cph_data = pd.read_csv(path)
    return cph_data

def get_sequence(row) -> None:
    initial_start   = row['SearchStart']
    initial_end     = row['SearchEnd']
    if pd.notna(initial_start):
        start   = re.sub(pattern_for_comma, "", initial_start)
        end     = re.sub(pattern_for_comma, "", initial_end)



        if "Metro" not in start:
            start   = re.sub(pattern_for_parenthesis, "", start)
        else: 
            start   = re.sub(pattern_for_parenthesis_number, "", start)
                
        if "Metro" not in end:
            end   = re.sub(pattern_for_parenthesis, "", end)
        else:
            end   = re.sub(pattern_for_parenthesis_number, "", end)
        
        if start.strip() != "":
            sequences.append([start.strip(), end.strip()])
            
            start = start.strip()
            end = end.strip()
            
            if start not in station_counter:
                station_counter[start] = 1
            else:
                station_counter[start] = station_counter[start] + 1
            
            if end not in station_counter:
                station_counter[end] = 1
            else:
                station_counter[end] = station_counter[end] + 1
            
def save_sequence_file(seq):
    df = pd.DataFrame(seq, columns=['start', 'end'])
    df.to_csv('Data/sequence_list.csv', index=False)
    



def main():
    PATH = 'Data/cph_file.csv'
    cph_data = load_data(PATH)
    cph_data.apply(get_sequence, axis=1)
    save_sequence_file(sequences)
    
main()