import os, requests
from bs4 import BeautifulSoup as bs

base_url = 'https://gosarchive.gov35.ru/archive1/unit/'
images_url = 'https://gosarchive.gov35.ru/archive1/image/'
headers = {}

arch_id = '410045'

# request the main page of the document:
main_response = requests.get(base_url + arch_id, headers=headers)

# set cookies, parse and save description, make directories
if (main_response.status_code == 200):
    # get coockies from response and set for global headers to use in get_images() function
    for cookie in main_response.cookies:
        if cookie.name == 'PHPSESSID':
            headers['Cookie'] = f'{cookie.name}={cookie.value}'

    path = os.getcwd() + '/' + arch_id
    if (not os.path.isdir(path) ):
        os.mkdir(path)

    soup = bs(main_response.text,'html.parser')

    with open(path + '/desc' + '.html', 'w') as f:
        f.write(str(soup.find(class_='well')))
else:
    print('Ошибка! Возможно неверно указан номер дела')

# Document`s first page number handling
while True:
    pages_range = [input('Начальная страница:\n')]
    if (not pages_range[0].isdigit()):
        print('Введите целое положительное число ')
        continue
    else:
        pages_range[0] = int(pages_range[0])
        if (pages_range[0] > 9999):
            print('Что-то слишком большое число. Попробуйте еще раз.')
            continue
        else:
            break

# Document`s last page number handling
while True:
    pages_range.append(input('Конечная страница:\n'))
    if (not pages_range[1].isdigit() or int(pages_range[0]) >= int(pages_range[1])):
        print('Введите целое положительное чило, большее, чем начальная страница')
        del pages_range[1]
        continue
    else:
        pages_range[1] = int(pages_range[1])
        if (pages_range[0] > 9999):
            print('Что-то слишком большое число. Попробуйте еще раз.')
            continue
        else:
            break

# requests and saves images, checks status code and empty bytes object
def get_images():
    pages_count = 0
    for i in range(pages_range[0], pages_range[1]+1):
        image_response = requests.get(images_url + arch_id + '?n=' + str(i), headers=headers)

        if (image_response.status_code == 200 and bool(image_response.content) != False):
            print(f'Сохранаяем страницу #{i}...', end='\r', flush=True)
            with open(arch_id+ '/image_' + str(i) + '.jpg', 'wb') as f:
                f.write(image_response.content)
            pages_count += 1
        else:
            print(f'Страница {i} не найдена' )

    print(f'\nВсего сохранено страниц: {pages_count} ')

get_images()