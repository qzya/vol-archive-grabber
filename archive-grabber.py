import os, requests
from bs4 import BeautifulSoup as bs

BASE_URL = 'https://gosarchive.gov35.ru/archive1/unit/'
IMAGES_URL = 'https://gosarchive.gov35.ru/archive1/image/'
headers = {}

# get cookies from response of the main page and set global headers for use in get_images() function
def set_cookies(response):
    for cookie in response.cookies:
        if cookie.name == 'PHPSESSID':
            headers['Cookie'] = f'{cookie.name}={cookie.value}'

# make directories and description file
def make_dirs_and_desc(arch_id, response):
    path = os.getcwd() + '/' + arch_id
    if (not os.path.isdir(path) ):
        os.mkdir(path)
    soup = bs(response.text,'html.parser')
    with open(path + '/desc' + '.html', 'w') as f:
        f.write(str(soup.find(class_='well')))

# handle input of  document number and prepare dirs
def prepare_dirs():
    # Document`s number handling
    while True:
        arch_id = input('Введите номер дела:\n')
        if not arch_id.isdigit() or len(arch_id) > 6:
            print('Не более 6 цифр')
            continue
        else:
            # request the main page of the document:
            main_response = requests.get(BASE_URL + arch_id, headers=headers)

            # set cookies, parse and save description, make directories
            if (main_response.status_code == 200):
                set_cookies(main_response)
                make_dirs_and_desc(arch_id, main_response)
                return arch_id
            else:
                print('Дело не найдено! Возможно неверно указан номер дела')
                continue

# handle inputs of pages range
def handle_inputs():
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
                return pages_range

# requests and saves images; checks status code and bytes object for empty
def get_images(arch_id, pages_range):
    pages_count = 0
    for i in range(pages_range[0], pages_range[1]+1):
        image_response = requests.get(IMAGES_URL + arch_id + '?n=' + str(i), headers=headers)

        if (image_response.status_code == 200 and bool(image_response.content) != False):
            print(f'Сохранаяем страницу #{i}...', end='\r', flush=True)
            with open(arch_id+ '/image_' + str(i) + '.jpg', 'wb') as f:
                f.write(image_response.content)
            pages_count += 1
        else:
            print(f'Страница {i} не найдена' )

    print(f'\nВсего сохранено страниц: {pages_count} ')

if __name__ == "__main__":
    get_images(prepare_dirs(), handle_inputs())

exit()