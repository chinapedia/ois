# wget http://onlineinternship.com/static/data/theVerge.html

import bs4

with open("theVerge.html") as ifile:
    html = ifile.read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    spans = soup.find_all("span")
    print (spans[4].text)
    h2s = soup.find_all("h2")
    print (len(h2s))
    numbers = [len(x.find_all("a", recursive=False)) for x in h2s]
    print (sum(numbers))
    