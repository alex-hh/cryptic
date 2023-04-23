import argparse
import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import json


url = 'https://www.theguardian.com/crosswords/accessible/quiptic/{}'


def main(puzzle_id):
    response = requests.get(url.format(puzzle_id))
    soup = BeautifulSoup(response.content, 'html.parser')


    def parse_clue(clue):
        clue_num = clue['value']
        clue_text = unicodedata.normalize('NFKD', clue.text.strip())
        code = re.findall(r'\(([\d,A-Z]+)\)', clue_text)[0]
        clue_text = clue_text.replace(f"({code}) ","")
        letters = re.findall(r'\(([\d,-]+)\)', clue_text)[0].replace("-", ",").split(",")
        num_letters = [int(d) for d in letters]
        return {'clue': clue_text, 'id': clue_num, 'num_letters': num_letters, 'code': code}


    # Extracting grid data
    grid_data = []
    blank_data = soup.select('ul.crossword__accessible-blank-data li.crossword__accessible-row-data')
    for blank in blank_data:
        line_num = re.findall(r'Line (\d+)', blank.span.text)[0]
        blanks = re.findall(r'\b([A-Z]{1,2})\b', blank.text)
        grid_data.append({'line': int(line_num), 'blanks': blanks})

    # Extracting across clues data
    across_data = []
    across_clues = soup.select('div.crossword__clues--across ol.crossword__clues-list li.crossword__clue')
    for clue in across_clues:
        across_data.append(parse_clue(clue))
        
    # Extracting down clues data
    down_data = []
    down_clues = soup.select('div.crossword__clues--down ol.crossword__clues-list li.crossword__clue')
    for clue in down_clues:
        down_data.append(parse_clue(clue))

    # Creating JSON output
    output = {
        'grid': grid_data,
        'across': across_data,
        'down': down_data,
        'id': puzzle_id,
        'url': url.format(puzzle_id),
        'type': 'quiptic',
        'source': 'Guardian',
    }
    json_output = json.dumps(output, indent=4)
    print(json_output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("puzzle_id")
    args = parser.parse_args()
    main(args.puzzle_id)

