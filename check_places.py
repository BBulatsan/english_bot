import requests
from bs4 import BeautifulSoup
import re
import env


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}
    r = requests.get(url, headers=headers, cookies=env.cookies)
    return r.text


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    carts = soup.find_all('div', class_='item shadow--hover special_course to-subscribe')
    list_all_carts = []
    sum_nums = 0
    for cart in carts:
        name = cart.find('div', class_='title').text.splitlines()[1].strip()
        date = cart.find('div', class_='date pb0').text.splitlines()[1].strip()
        teacher = cart.find('span', class_='credential teacher-name').text.splitlines()[2].strip()
        number_of_seats = cart.find('div', class_='places-left').text.splitlines()[1].strip()
        num = int(re.findall(r'\d+', number_of_seats)[0])
        if num != 0:
            data = name + "\n" + date + "\n" + teacher + "\n" + number_of_seats
            list_all_carts.append(data)
            sum_nums += num
        else:
            continue
    return list_all_carts, sum_nums


def main():
    print(get_data(get_html(env.base_url)))


if __name__ == '__main__':
    main()
