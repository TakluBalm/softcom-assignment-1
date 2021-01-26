import bs4
import requests
import os
import textwrap

wrapper = textwrap.TextWrapper(width = 178)

urls=["https://timesofindia.indiatimes.com/india","https://timesofindia.indiatimes.com/world","https://timesofindia.indiatimes.com/business","https://timesofindia.indiatimes.com/"]

for url in urls:
    source=requests.get(url)
    all_content=bs4.BeautifulSoup(source.text,"lxml")
    content = all_content.find("div", class_="main-content")
    a_tags=content.find_all("a", href=True, target=False, class_=False, title=True)
    links=[]
    for var in a_tags:
        if 'http' in var['href']:
            continue
        elif 'video' in var['href']:
            continue
        elif '/' in var['href']:
            temp='https://timesofindia.indiatimes.com' + var['href']
            links.append(temp)
    cwd = os.getcwd() #fetching current working directory from the system
    #generating a folder in cwd
    if '/india' in url:
        path = os.path.join(cwd, "India")
        os.mkdir(path)
    elif '/world' in url:
        path = os.path.join(cwd, "World")
        os.mkdir(path)
    elif '/business' in url:
        path = os.path.join(cwd, "Business")
        os.mkdir(path)
    else:
        path = os.path.join(cwd, "Home")
        os.mkdir(path)
    
    i = 1
    #writing links to the file
    for link in links:
        source = requests.get(link)
        content = bs4.BeautifulSoup(source.text, "lxml")
        fd = open(f"{path}/file{i}.txt", "w")
        try:
            title = content.find("h1", class_='_23498' ).text
            article = wrapper.fill(text = content.find("div", class_='ga-headlines').text)
            date = content.find("div", class_="_3Mkg- byline").text
        except Exception as e:
            title = "Premium Content"
            article = "Premium Content"
            date = "Premium Content"
        date = date[-21:]
        fd.write(f"Link:\n{link}\n\nTitle:\n{title}\n\nDate:\n{date}\n\nContents:\n{article}")
        i += 1
        fd.close()
        