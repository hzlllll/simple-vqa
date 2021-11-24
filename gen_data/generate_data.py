from shape import Shape
from color import Color, Number
from images import create_image
from questions import create_questions
from random import choice
import json
import os

if not os.path.exists('easy_vqa/data_num/train/images'):
    os.makedirs('easy_vqa/data_num/train/images/')
if not os.path.exists('easy_vqa/data_num/test/images'):
    os.makedirs('easy_vqa/data_num/test/images/')

colors = list(Color)
shapes = list(Shape)
numbers = list(Number)
NUM_TRAIN = 4000
NUM_TEST = 1000


def create_data(image_path, num):
    qs = []
    num_yes_no = 0
    for i in range(num):
        shape = choice(shapes)
        color = choice(colors)
        number = choice(numbers)
        create_image(f'{image_path}/{i}.png', shape, color, number)
        new_qs, new_num_yes_no = create_questions(shape, color, i, number)
        qs += new_qs
        num_yes_no += new_num_yes_no
    return qs, num_yes_no


train_questions, num_train_yes_no = create_data(
    'easy_vqa/data_num/train/images', NUM_TRAIN)
test_questions, num_test_yes_no = create_data('easy_vqa/data_num/test/images',
                                              NUM_TEST)

all_questions = train_questions + test_questions
all_answers = list(set(map(lambda q: q[1], all_questions)))

with open('easy_vqa/data_num/train/questions.json', 'w') as file:
    json.dump(train_questions, file)
with open('easy_vqa/data_num/test/questions.json', 'w') as file:
    json.dump(test_questions, file)

with open('easy_vqa/data_num/answers.txt', 'w') as file:
    for answer in all_answers:
        file.write(f'{answer}\n')

print(
    f'Generated {NUM_TRAIN} train images and {len(train_questions)} train questions.'
)
print(
    f'Generated {NUM_TEST} test images and {len(test_questions)} test questions.'
)
print(f'{len(all_answers)} total possible answers.')
print(f'{num_train_yes_no} training questions are yes/no.')
print(f'{num_test_yes_no} testing questions are yes/no.')
