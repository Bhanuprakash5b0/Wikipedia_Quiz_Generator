import requests
from bs4 import BeautifulSoup

def scrape_wikipedia(url):
    #url="https://en.wikipedia.org/wiki/Varanasi_(film)" 
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=10)
        print(response.status_code)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1").text

        paragraphs = soup.find_all("p")
        content = " ".join(p.text for p in paragraphs[:15])

        #print(title+"\n"+content+"\n"+paragraphs[0].text.strip())
        return {
            "title": title,
            "content": content,
            "summary": paragraphs[0].text.strip()
        }

    except Exception as e:
        print(e)
        return None
#scrape_wikipedia("https://en.wikipedia.org/wiki/Varanasi_(film)")