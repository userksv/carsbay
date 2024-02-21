from django.shortcuts import render
import requests, bs4

# Create your views here.
def news(request):
    context = {}
    source, news = rss_news_feed()
    context = {'news': news, 'source': source}

    return render(request, 'news/news.html', context)


def rss_news_feed():
    url = 'https://www.caranddriver.com/rss/all.xml/'
    r = requests.get(url)
    r.raise_for_status()

    soup = bs4.BeautifulSoup(r.text, features="xml")
    items = soup.find_all('item')
    source = soup.link.string[12:-1]
    return source , [
        {
            'news_title': item.title.string,
            'news_url': item.link.string,
            'news_img_src': item.find('media:content')['url'],
        }
        for item in items if item.category.string == 'News'
    ]

s, l = rss_news_feed()
print(s)