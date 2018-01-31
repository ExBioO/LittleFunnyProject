import pandas as pd
from urllib import urlopen
from bs4 import BeautifulSoup
from googlesearch import search
from tqdm import tqdm

namePath = "names.csv"
outPath = "date.csv"

def searchDateOnGoogle(query):
    result = search(query, num=10, stop=1, pause=2)
    for url in result:
        if "https://ark.intel.com/products/" in url:
            return extractDateFromIntel(url)
        elif ("http://www.amd.com/" in url) or ("https://www.amd.com/" in url):
            return extractDateFromAMD(url)
        elif "https://en.wikipedia.org/wiki/" in url:
            pass
        #print(url)
    raise Exception("Unspecified query:"+query)

def extractDateFromWikipedia(url):
    pass


def extractDateFromIntel(url):
    html = urlopen(url).read()
    parsed_html = BeautifulSoup(html,  "html.parser")
    dateText = parsed_html.body.find('li', attrs={'class':'BornOnDate'}).text
    dateTextParesed = dateText.split('\n')
    for token in dateTextParesed:
        if 'Q' in token:
            dateParesed = token.split('\'')
            date = "20"+dateParesed[1]+'.'+dateParesed[0][1]
            return date
    raise Exception("Can find date in: "+dateText)

def extractDateFromAMD(url):
    html = urlopen(url).read()
    index = html.find("Launch Date")
    if index==-1:raise Exception("Can't find date in: "+url)
    s = html[index:index+100]
    index1 = s.find("field__item\">")+len("field__item\">")
    index2 = s.find("</div>", index1)
    #print(s[index1:index2])
    dateParesed = s[index1:index2].split("/")
    date = dateParesed[2]+'.'+str(1+int((int(dateParesed[0])-1)/3))
    return date

def mergeByName(singleCore, multiCore, date):
    merge = pd.merge(singleCore, multiCore, on="cpu")
    return pd.merge(merge, date, on='cpu')


def main():
    #print(searchDateOnGoogle("Intel Core i7-8700K 3.7 GHz (6 cores)"))
    names = pd.read_csv(namePath)
    nameSample = names["cpu"]
    dateSample = []
    print("start searching...")
    for name in tqdm(nameSample):
        try:
            dateSample.append(searchDateOnGoogle(name))
        except:
            print("Fail to search: "+name)
            dateSample.append("")
    data = pd.DataFrame({"cpu":nameSample, "date": dateSample})
    data.to_csv(outPath, sep=",", encoding='utf-8')


if __name__ == '__main__':
    main()