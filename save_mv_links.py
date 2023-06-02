from bs4 import BeautifulSoup

try:
    with open("27milletvekili.html") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
except FileNotFoundError:
    print("Error: HTML file not found.")
    exit()

base_url = 'https://www.tbmm.gov.tr'

div_elements = soup.find_all('div', class_='row profile-list')

links = []
for div in div_elements:
    span = div.find('span')
    href = span.find('a')['href']
    full_url = base_url + href.replace('&amp;', '&')
    links.append(full_url)

output = '\n'.join(links)
with open('27.Donem_Milletvekili_Link.txt', 'w') as f:
    f.write(output)