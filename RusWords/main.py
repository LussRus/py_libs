import glob
import os
from bs4 import BeautifulSoup
import requests as requests
from pathlib import Path
import json
import concurrent.futures
import codecs

url = 'https://wordsonline.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
rus_symbs = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
temp_file = 'temp/temp.html'
words_dir = 'words'
debug_mode = True
write_new = False
MAX_THREADS = 10
folders = ['adject', 'nouns', 'verbs']

def get_all_words_from_page(num, symb):
    arr = []
    page_url = f'{url}{symb}'
    if num:
        page_url += f'?page={num}'
    print(f"Get {page_url}")
    page = requests.get(page_url, headers=headers).text
    print(f'Page length {len(page)}')
    if len(page) < 5000:
        return arr
    soup = BeautifulSoup(page, 'html.parser')
    li = soup.find('ul', class_='list-words').find_all('li')
    for a in li:
        arr.append(a.text)
    return arr

def store_words_with_letter(arr, symb):
    print(f'{words_dir}/{symb}.json')
    with open(f'{words_dir}/{symb}.json', 'w') as f:
        json.dump(arr, f)

def get_words_with_letter(symb):
    print(f'Parse letter {symb}')
    if debug_mode:
        fn = Path(temp_file)
        if fn.is_file():
            with open(fn, 'r') as f:
                page = f.read()
        else:
            furl = f'{url}{symb}'
            print(furl)
            page = requests.get(url=furl, headers=headers).text
            if write_new:
                with open(temp_file, 'w') as f:
                    f.write(page)
    else:
        page = requests.get(url=f'{url}{symb}', headers=headers).text
    words = []
    soup = BeautifulSoup(page, "html.parser")
    paginator = soup.find('ul', class_='pagination').find_all('li')
    l = len(paginator)
    num_of_pages = paginator[l-1].text
    print(f'Num of pages for letter {symb} is {num_of_pages}')
    for num in range(0,int(num_of_pages)):
        words += get_all_words_from_page(num, symb)
    store_words_with_letter(words, symb)
    print(f"Parsing letter {symb} has been finished")

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as ex:
        ex.map(get_words_with_letter, rus_symbs)

def merge_all_files(dir=words_dir, js='json'):
    final_file = 'summary.json'
    res_arr = []
    for symb in rus_symbs:
        with open(f'{dir}/{symb}.json', 'r') as f:
            a = json.load(f)
            res_arr += a
    if js == 'json':
        with open(f'{dir}/{final_file}', 'w', encoding='utf8') as f:
            json.dump(res_arr, f, ensure_ascii=False)
    else:
        with open(f'{dir}/{final_file}', 'w') as f:
            json.dump(res_arr, f)


def convert_to_txt(dir = words_dir):
    big_res = ''
    for symb in rus_symbs:
        res = ''
        with open(f'{dir}/json/{symb}.json', 'r') as f:
            arr = json.load(f)
            for a in arr:
                res += a + '\n'
        big_res += res
        with open(f'{dir}/txt/{symb}.txt', 'w') as f:
            f.write(res)
        f.close()
        with codecs.open(f'{words_dir}/json/{symb}.json', 'w', encoding='utf8') as f:
            json.dump(arr, f, ensure_ascii=False)
    with open(f'{dir}/txt/summary.txt', 'w') as f:
        f.write(big_res)
    f.close()
    with open(f'{dir}/json/summary.json', 'w', encoding='utf8') as f:
        json.dump(big_res.split('\n'), f, ensure_ascii=False)

excl_arr = ['кий', 'ый', 'ая', 'ое', 'чик']
verb_arr = ['ть',]

def word_has(w, arr):
    for el in arr:
        if el in w:
            return True
    return False

def select_noun(symb, js='json', base_dir = f'{words_dir}/UTF8'):
    fn = f'{base_dir}/json/raw/{symb}.json'
    with open(fn, 'r') as f:
        arr = json.load(f)
        js = {}
        txt = {}
        for folder in folders:
            js[folder] = []
            txt[folder] = ''
        for word in arr:
            if not word_has(word, excl_arr):
                if word_has(word, verb_arr):
                    js['verbs'].append(word)
                    txt['verbs'] += word+'\n'
                else:
                    js['nouns'].append(word)
                    txt['nouns'] += word+'\n'
            else:
                js['adject'].append(word)
                txt['adject'] += word+'\n'
    for folder in folders:
        if js == 'json':
            with codecs.open(f'{base_dir}/json/{folder}/{symb}.json', 'w', encoding='utf8') as f:
                json.dump(js[folder], f, ensure_ascii=False)
        else:
            with codecs.open(f'{base_dir}/json/{folder}/{symb}.json', 'w') as f:
                json.dump(js[folder], f)
        with open(f'{base_dir}/txt/{folder}/{symb}.txt', 'w') as f:
            f.write(txt[folder])
        f.close()

def join_all_json_in_dir(dir = f'{words_dir}/UTF8'):
    for fld in folders:
        merge_all_files(f'{dir}/json/{fld}', 'json')
    for folder in folders:
        for symb in rus_symbs:
            f = f'{dir}/txt/{folder}/{symb}.txt'
            os.system("cat " + f + f" >> {dir}/txt/{folder}/summary.txt")

if '__main__' == __name__:
#    main()
#    merge_all_files()
#    convert_to_txt()
    for symb in rus_symbs:
        select_noun(symb, 'n', f'{words_dir}/cp1251')
    join_all_json_in_dir(f'{words_dir}/cp1251')