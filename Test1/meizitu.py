from bs4 import BeautifulSoup
import requests
import os

url = 'http://www.mzitu.com/'
head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36\
 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36','Referer':url}
res1 = requests.get(url,headers = head)
content = res1.text
soup1 = BeautifulSoup(content, 'html.parser')
fin_num = soup1.find_all('a', class_ = 'page-numbers')
max_page = fin_num[-2].text
for i in range(6,11):
    if not os.path.exists('E:/Python_Project/Test1/pic' + '/' + str(i)):
        os.mkdir('E:/Python_Project/Test1/pic' + '/' + str(i))
    path = 'E:/Python_Project/Test1/pic' + '/' + str(i)
    if i == 1:
        url = 'http://www.mzitu.com/'
    else:
        url = 'http://www.mzitu.com/page' + '/' + str(i) + '/'
    res2 = requests.get(url, headers=head)
    content2 = res2.text
    soup2 = BeautifulSoup(content2, 'html.parser')
    fid_a = soup2.find(id='pins').find_all(target='_blank')

    for a in fid_a:
        print(a['href'])
        url3 = a['href']
        res3 = requests.get(url3, headers=head)
        content3 = res3.text
        soup3 = BeautifulSoup(content3, 'html.parser')
        pic_max = soup3.find_all('span')[10].text
        title = soup3.find('h2').text

        for j in range(1, int(pic_max) + 1):
            href = url3 + '/' + str(j)
            html = requests.get(href, headers=head)
            mess = BeautifulSoup(html.text, 'html.parser')
            pic_url = mess.find('img', alt=title)
            try:
                html = requests.get(pic_url['src'], headers=head)
                filename = pic_url['src'].split(r'/')[-1]
            except:
                continue
            if os.path.exists(path + '/' + filename):
                continue
            f = open(path + '/' + filename, 'wb')
            f.write(html.content)
            f.close()
