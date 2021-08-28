import requests
from bs4 import BeautifulSoup


def check_backlink(url, backlink):
    request = requests.get(url)
    if request.ok:
        raw = request.text
        soup = BeautifulSoup(raw, "html.parser")
        anchors = soup.find_all('a')  # find all anchor tag
        flag = False
        for anchor in anchors:
            if anchor.attrs.get('href') == backlink:  # extract herf link and compare
                flag = True
        return flag
    else:
        return False


def check(data):
    data['Brand URLs Present'] = data.progress_apply(lambda x: check_backlink(x['AWU'], x['BU'].strip()), axis=1)
    data['Brand URLs Present'] = data['Brand URLs Present'].apply(lambda x: 'Yes' if x  else 'No')
    return data
