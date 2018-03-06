import os
import pdfkit
import requests
import requests_html

def Download_image(img_name, img_url):
    print('Download image:', img_name, img_url)
    filename = img_name + 'jpg'
    with open(filename, 'wb') as f:
        r = requests.get(img_url)
        f.write(r.content)

def Download_poster(path, poster_url):
    print('Download poster:', path, poster_url)
    poster_name = poster_url.split('/')[-1]
    filename = os.path.join(path, poster_name)
    with open(filename, 'wb') as f:
        r = requests.get(poster_url)
        f.write(r.content)


URL = 'http://maoyan.com/board/4'
for i in range(10):
    session = requests_html.HTMLSession()
    params = {'offset': str(10 * i)}
    soup = session.get(URL, params=params)
    #pdfkit.from_url(soup.url, str(i)+'.pdf')

    aList = soup.html.xpath("//div[@class='wrapper']//a[@class='image-link']")
    for a in aList:
        img = a.find("img[@class='board-img']")[0]
        img_url = img.attrs['data-src']
        img_name = img.attrs['alt']
        img_url = img_url.split('@')[0]
        Download_image(img_name, img_url)

        path = img_name
        if not os.path.exists(path):
            os.mkdir(path)
        
        poster_url = 'http://maoyan.com' + a.attrs['href']
        r = session.get(poster_url)
        urls = r.html.xpath("/html/body/div[4]/div/div[1]/div/div[2]/div[4]//img/@data-src")
        for poster_url in urls:
            poster_url = poster_url.split('@')[0]
            Download_poster(path, poster_url)
