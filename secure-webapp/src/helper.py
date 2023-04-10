from bs4 import BeautifulSoup
from hashlib import sha512


def clean_content(content):
    concatenated =  ""
    for line in content.split('\n'):
        concatenated+=line.strip()+'\n'
    return concatenated;


def calc_integrity(dom_content):
    soup = BeautifulSoup(dom_content, 'html.parser')
    vaults = soup.find_all('vault')
    if vaults:
        concatenated = "" 
        for vault in vaults:
            concatenated+=clean_content(str(vault))
        print(concatenated)
        print(sha512(concatenated.encode()).hexdigest())
    else:
        return 'NA'
