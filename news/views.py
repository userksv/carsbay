from django.shortcuts import render
import requests, bs4


def news(request):
    context = {}
    source, news = rss_news_feed()
    context = {'news': news, 'source': source}
    return render(request, 'news/news.html', context)


def rss_news_feed():
    url = 'https://www.caranddriver.com/rss/all.xml/'
    r = requests.get(url)
    r.raise_for_status()

    soup = bs4.BeautifulSoup(r.text, 'xml')
    items = soup.find_all('item')
    source = soup.link.string[12:-1]
    content = []
    for item in items:
        media_tag = item.find('media:content')
        if media_tag:
            url = media_tag.get('url')
        content.append({
            'news_title': item.title.string,
            'news_url': item.link.string,
            'news_img_src': url,
        })
       
    return source, content
