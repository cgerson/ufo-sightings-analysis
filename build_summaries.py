from bs4 import BeautifulSoup
import glob
import os
from pymongo import MongoClient

client = MongoClient(host="54.69.198.239",port=27017)
db = client.UFO
col = db.Summaries

dirs = os.listdir("./www.nuforc.org/webreports/")
num_dirs = [directory for directory in dirs if str(directory).isdigit()] 
for item in num_dirs:
    path = './www.nuforc.org/webreports/{}/*.html'.format(item)
    print path
    files = glob.glob(path)
    for name in files:
        summary = {}
        summary["link"]=str(name[-15:-5]) #change, links from dir 100 on are longer (should try to capture up until / only)
        try:
            with open(name) as f:
                soup = BeautifulSoup(f,"html.parser")
                tds = soup.find_all("td")
                summary["text"]=tds[1].text
        except:
            summary["text"] = "None"
        col.save(summary)


