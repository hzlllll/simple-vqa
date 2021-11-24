from shape import Shape
from color import Color, Number
from random import randint


# 添加计数和yes no的问题
# TODO
def create_questions(shape, color, image_id, number):
    shape_name = shape.name.lower()
    color_name = color.name.lower()
    number_name = number.name.lower()
    questions = [
        (f'what shape is in the image?', shape_name),
        (f'what shape is present?', shape_name),
        (f'what shape does the image contain?', shape_name),
        (f'what is the {color_name} shape?', shape_name),
        (f'what color is the {shape_name}?', color_name),
        (f'what is the color of the {shape_name}?', color_name),
        (f'what color is the shape?', color_name),
        (f'what is the color of the shape?', color_name),
        (f'how many objects are in the image', number_name),
        (f'how many {shape_name}s are in the image', number_name),
        (f'how many objects do the image contain', number_name),
        (f'how many {color_name} {shape_name}s do the image contain',
         number_name),
    ]

    yes_no_questions = []

    for s in Shape:
        cur_shape_name = s.name.lower()
        pos_answer = 'yes' if s is shape else 'no'
        yes_no_questions.append((f'is there a {cur_shape_name}?', pos_answer))
        yes_no_questions.append(
            (f'is there a {cur_shape_name} in the image?', pos_answer))
        yes_no_questions.append(
            (f'does the image contain a {cur_shape_name}?', pos_answer))
        yes_no_questions.append(
            (f'is a {cur_shape_name} present?', pos_answer))

        neg_answer = 'no' if s is shape else 'yes'
        yes_no_questions.append(
            (f'is there not a {cur_shape_name}?', neg_answer))
        yes_no_questions.append(
            (f'is there not a {cur_shape_name} in the image?', neg_answer))
        yes_no_questions.append(
            (f'does the image not contain a {cur_shape_name}?', neg_answer))
        yes_no_questions.append(
            (f'is no {cur_shape_name} present?', neg_answer))

    for c in Color:
        cur_color_name = c.name.lower()
        pos_answer = 'yes' if c is color else 'no'
        yes_no_questions.append(
            (f'is there a {cur_color_name} shape?', pos_answer))
        yes_no_questions.append(
            (f'is there a {cur_color_name} shape in the image?', pos_answer))
        yes_no_questions.append(
            (f'does the image contain a {cur_color_name} shape?', pos_answer))
        yes_no_questions.append(
            (f'is a {cur_color_name} shape present?', pos_answer))

        neg_answer = 'no' if c is color else 'yes'
        yes_no_questions.append(
            (f'is there not a {cur_color_name} shape?', neg_answer))
        yes_no_questions.append(
            (f'is there not a {cur_color_name} shape in the image?',
             neg_answer))
        yes_no_questions.append(
            (f'does the image not contain a {cur_color_name} shape?',
             neg_answer))
        yes_no_questions.append(
            (f'is no {cur_color_name} shape present?', neg_answer))
    for n in Number:
        cur_number_name = n.name.lower()
        pos_answer = 'yes' if n is number else 'no'
        yes_no_questions.append(
            (f'are there {cur_number_name} objects?', pos_answer))
        yes_no_questions.append(
            (f'are there {cur_number_name} objects in the image?', pos_answer))
        yes_no_questions.append(
            (f'does the image contain {cur_number_name} objects?', pos_answer))
        yes_no_questions.append(
            (f'are there {cur_number_name} objects present?', pos_answer))

        neg_answer = 'no' if n is number else 'yes'
        yes_no_questions.append(
            (f'are there not  {cur_number_name} objects?', neg_answer))
        yes_no_questions.append(
            (f'are there not  {cur_number_name} objects in the image?',
             neg_answer))
        yes_no_questions.append(
            (f'does the image not contain  {cur_number_name} objects?',
             neg_answer))
        yes_no_questions.append(
            (f'are no {cur_number_name} objects present?', neg_answer))
    questions = list(filter(lambda _: randint(0, 99) < 32, questions))
    yes_no_questions = list(
        filter(lambda _: randint(0, 99) < 8, yes_no_questions))

    all_questions = questions + yes_no_questions
    return (list(map(lambda x: x + (image_id, ),
                     all_questions)), len(yes_no_questions))
