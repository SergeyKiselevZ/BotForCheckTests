import core_processing_photo
import os
import chrome_lens_py
from threading import Thread
import asyncio


def text_to_dictionary(text):
    pass

def cutting_leaves(photo):
    pass

def cutting_text_on_photo(photo):
    pass

def answer_is_right(text, right_answer):
    pass

async def to_google_lens(path):
    api = chrome_lens_py.LensAPI()
    return await api.get_full_text(path)

def get_answers(text: list):
    text = [i.replace(' ', '').replace('-', ' ').split('\n')[1::] for i in text]
    return text

#print(get_answers(['Кравченко. М. 104\n1-2\n2-3\n4-5\n3-4', 'Якубов. А. 104\n1-1\n2-4\n3-3\n4-2', 'Шмаков. К 10A\n1-6\n2-2\n3-g\n4-C', 'Киселев. С. 104\n1-1\n2-2\n3-3\n4-4']))

def get_last_names(text: list[str]):
    text = [i.replace(' ', '').replace(',', '.').split('\n')[0] for i in text]
    return [i.split('.')[0].capitalize() for i in text]
#print(get_last_names(['Кравченко. М. 104\n1-2\n2-3\n4-5\n3-4', 'Якубов. А. 104\n1-1\n2-4\n3-3\n4-2', 'Шмаков. К 10A\n1-6\n2-2\n3-g\n4-C', 'Киселев. С. 104\n1-1\n2-2\n3-3\n4-4']))

def get_true_answers(text):
    return text.split('\n')
#print(get_true_answers('1 2\n2 3'))

def get_count(true_answers: list, answers:list) -> int:
    count = 0
    for i in answers:
        if i in true_answers:
            count += 1
    return count

#print(get_count(['1 2', '2 3', '4 5', '3 4'], ['1 1', '2 3', '4 5', '3 4']))

def get_criteria(text):
    text = text.split('\n')
    text = [i.split(' ') for i in text]
    criteria = {}
    for i in text:
        criteria[i[0]] = int(i[1])
    return criteria

#print(get_criteria('1 2\n2 3'))

async def main_processing(id, user_data):
    print('blalala')
    names = []
    path = 'tmp/' + str(id) + '/'
    for name in os.listdir(path):
        new_names = core_processing_photo.core(path, name, id)
        for i in new_names:
            names.append(i)
        #os.remove(path+name)
    text = []
    print(names)
    for i in names:
        print(i)
        text.append(await to_google_lens('tests/' + str(id)+'/'+i))

    print(text)
    answers = get_answers(text)
    last_names = get_last_names(text)
    criteria = get_criteria(user_data['criteria'])
    res = []
    print(answers)
    print(last_names)
    print(criteria)
    for i, name in enumerate(last_names):
        count = get_count(get_true_answers(user_data['answers']), answers[i])
        print(name, count)
        est = 0
        if count <= criteria['2']:
            est = 2
        elif count <= criteria['3']:
            est = 3
        elif count <= criteria['4']:
            est = 4
        elif count <= criteria['5']:
            est = 5

        res.append(f'{name}: {est}')

    return '\n'.join(res)