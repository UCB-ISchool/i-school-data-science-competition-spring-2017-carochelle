import urllib.request as req
import json
import urllib.parse as up
import csv
from pprint import pprint
import re

WIKI_URL = "https://en.wikipedia.org/w/api.php?action=query&titles=<name>&prop=revisions&rvprop=content&format=json"


def read_celebrity_list():
    '''
    Function to read celebrity names and
    return list of famous celebrities
    '''

    celebrity_list = []
    with open('celebrities_100.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            celebrity_list.append(row['Name'].strip())
    return celebrity_list

def query_wikipedia(name):
    url_name = name.replace(" ", "%20")
    response = req.urlopen(WIKI_URL.replace(
        "<name>", url_name)).read().decode('utf-8')
    return response


def process_celebrity_marriage_data(celebrity_list):
    '''
    Function which accepts list of celebrities and queries wikipedia to
    retreive number of marriages and divorces for each celebrity
    '''

    results = []
    for name in celebrity_list:
        count_marriage = 0
        list_of_spouses = []

        response = query_wikipedia(name)
        # Check if the page is redirected to another
        redirect_loc = response.find('#REDIRECT')
        if redirect_loc != -1:
            redirect_name = response[redirect_loc+12:]
            redirect_name = redirect_name[:redirect_name.find("]]")]
            response = query_wikipedia(redirect_name)

        #Fetch spouses / divorces
        spouse_word = response.find('spouse')
        text = response[spouse_word:]
        marriage_start = text.lower().find('{marriage')

        if marriage_start == - 1:
            if spouse_word >= 0:
                count_marriage = 1
                name_start = re.search('[A-Z]', text[6:])
                letter = name_start.group(0)
                name_start = text.find(letter)
                name_end = re.search("[^a-zA-Z\d\s:]", text[name_start:])
                end_symbol = name_end.group(0)
                end = text.find(end_symbol, name_start)
                spouse_name = text[name_start: end]
                list_of_spouses.append(spouse_name)

        count_divorces = text.count('end=div')
        count_divorces2 = text.count('reason=divorced')
        count_divorces = count_divorces + count_divorces2
        while marriage_start > 0:  # entered three times
            count_marriage += 1
            text = text[marriage_start + 6:]
            name_start = re.search('[A-Z]', text)
            letter = name_start.group(0)
            name_start = text.find(letter)  # 36
            name_end = re.search("[^\w\s]", text[name_start:])
            end_symbol = name_end.group(0)
            end = text.find(end_symbol, name_start)
            spouse_name = text[name_start: end]
            list_of_spouses.append(spouse_name)
            text = text[marriage_start:]
            marriage_start = text.lower().find('{marriage')

        celebrity_data = {"Name": name, 'Marriages': count_marriage, 'Divorces': count_divorces, 'List of Spouses': list_of_spouses}
        results.append(celebrity_data)
    return results


def write_celebrity_divorces_to_csv(results):
    '''
    Functin which writes celebrity divorces data to csv
    '''
    print(results)
    with open('celebrity_divorces.csv', 'w') as csvfile:
        fieldnames = ['Name', 'Marriages', 'Divorces', 'List of Spouses']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def main():
    '''
    Main method
    '''

    celebrity_list = read_celebrity_list()
    results = process_celebrity_marriage_data(celebrity_list)
    write_celebrity_divorces_to_csv(results)


if __name__ == "__main__":
    main()
