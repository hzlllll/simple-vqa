from keras.preprocessing.text import Tokenizer
from keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.utils import to_categorical
import json
import os
from easy_vqa import get_train_questions, get_test_questions, get_train_image_paths, get_test_image_paths, get_answers


def setupbyPath(imgPath):
    _, name = os.path.split(imgPath)
    id, _ = os.path.splitext(name)

    def read_questions(path, id):
        with open(path, 'r') as file:
            qs = json.load(file)
        texts = []
        answers = []
        image_ids = []
        train_qs_all = []
        with open('data_num/train/questions.json', 'r') as file:
            tqs = json.load(file)
        for q in tqs:
            train_qs_all.append(q[0])
        for q in qs:
            if q[2] != int(id):
                continue
            texts.append(q[0])
            answers.append(q[1])
            image_ids.append(q[2])
        return (train_qs_all, texts, answers, image_ids)

    is_train = imgPath.find("train")
    print(is_train)
    if is_train != -1:
        train_qs_all, train_qs, train_answers, train_image_ids = read_questions(
            'data_num/train/questions.json', id)
    else:
        train_qs_all, train_qs, train_answers, train_image_ids = read_questions(
            'data_num/test/questions.json', id)
    with open('data_num/answers.txt', 'r') as file:
        all_answers = [a.strip() for a in file]
    num_answers = len(all_answers)

    def load_and_proccess_image(image_path):
        # Load image, then scale and shift pixel values to [-0.5, 0.5]
        im = img_to_array(load_img(image_path))
        return im / 255 - 0.5

    def read_images(paths):
        # paths is a dict mapping image ID to image path
        # Returns a dict mapping image ID to the processed image
        ims = {}
        for image_id, image_path in paths.items():
            ims[image_id] = load_and_proccess_image(image_path)
        return ims

    def extract_paths(dir, name):
        paths = {}
        for filename in os.listdir(dir):
            if filename != name:
                continue
            if filename.endswith('.png'):
                image_id = int(filename[:-4])
                paths[image_id] = os.path.join(dir, filename)
        return paths

    if is_train != -1:
        train_ims = read_images(extract_paths('data_num/train/images', name))
    else:
        train_ims = read_images(extract_paths('data_num/test/images', name))
    #print(train_ims)
    #im_shape = train_ims[0].shape
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(train_qs_all)

    # We add one because the Keras Tokenizer reserves index 0 and never uses it.

    train_X_seqs = tokenizer.texts_to_matrix(train_qs)

    train_X_ims = [train_ims[id] for id in train_image_ids]
    train_answer_indices = [all_answers.index(a) for a in train_answers]
    train_Y = to_categorical(train_answer_indices)

    #print(train_answer_indices, train_Y, train_qs, len(train_X_seqs),train_X_seqs[0].shape)
    vocab_size = len(tokenizer.word_index) + 1
    return (train_X_ims, train_X_seqs, train_Y, train_qs, train_answers,
            num_answers, all_answers)


def setup(use_data_dir):
    print('\n--- Reading questions...')
    if use_data_dir:
        # Read data from data/ folder
        def read_questions(path):
            with open(path, 'r') as file:
                qs = json.load(file)
            texts = [q[0] for q in qs]
            answers = [q[1] for q in qs]
            image_ids = [q[2] for q in qs]
            return (texts, answers, image_ids)

        train_qs, train_answers, train_image_ids = read_questions(
            'data_num/train/questions.json')
        test_qs, test_answers, test_image_ids = read_questions(
            'data_num/test/questions.json')
        print("load")
    else:
        # Use the easy-vqa package
        train_qs, train_answers, train_image_ids = get_train_questions()
        test_qs, test_answers, test_image_ids = get_test_questions()
    print(
        f'Read {len(train_qs)} training questions and {len(test_qs)} testing questions.'
    )

    print('\n--- Reading answers...')
    if use_data_dir:
        # Read answers from data/ folder
        with open('data_num/answers.txt', 'r') as file:
            all_answers = [a.strip() for a in file]
    else:
        # Read answers from the easy-vqa package
        all_answers = get_answers()
    num_answers = len(all_answers)
    print(f'Found {num_answers} total answers:')
    print(all_answers)

    print('\n--- Reading/processing images...')

    def load_and_proccess_image(image_path):
        # Load image, then scale and shift pixel values to [-0.5, 0.5]
        im = img_to_array(load_img(image_path))
        return im / 255 - 0.5

    def read_images(paths):
        # paths is a dict mapping image ID to image path
        # Returns a dict mapping image ID to the processed image
        ims = {}
        for image_id, image_path in paths.items():
            ims[image_id] = load_and_proccess_image(image_path)
        return ims

    if use_data_dir:
        # Read images from data/ folder
        def extract_paths(dir):
            paths = {}
            for filename in os.listdir(dir):
                if filename.endswith('.png'):
                    image_id = int(filename[:-4])
                    paths[image_id] = os.path.join(dir, filename)
            return paths

        train_ims = read_images(extract_paths('data_num/train/images'))
        test_ims = read_images(extract_paths('data_num/test/images'))
    else:
        # Read images from the easy-vqa package
        train_ims = read_images(get_train_image_paths())
        test_ims = read_images(get_test_image_paths())
    im_shape = train_ims[0].shape
    print(
        f'Read {len(train_ims)} training images and {len(test_ims)} testing images.'
    )
    print(f'Each image has shape {im_shape}.')

    print('\n--- Fitting question tokenizer...')
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(train_qs)

    # We add one because the Keras Tokenizer reserves index 0 and never uses it.
    vocab_size = len(tokenizer.word_index) + 1
    print(f'Vocab Size: {vocab_size}')
    print(tokenizer.word_index)

    print('\n--- Converting questions to bags of words...')
    train_X_seqs = tokenizer.texts_to_matrix(train_qs)
    test_X_seqs = tokenizer.texts_to_matrix(test_qs)
    print(f'Example question bag of words: {train_X_seqs[0]}')

    print('\n--- Creating model input images...')
    train_X_ims = [train_ims[id] for id in train_image_ids]
    test_X_ims = [test_ims[id] for id in test_image_ids]

    print('\n--- Creating model outputs...')
    train_answer_indices = [all_answers.index(a) for a in train_answers]
    test_answer_indices = [all_answers.index(a) for a in test_answers]
    train_Y = to_categorical(train_answer_indices)
    test_Y = to_categorical(test_answer_indices)
    print(f'Example model output: {train_Y[0]}')

    return (train_X_ims, train_X_seqs, train_Y, test_X_ims, test_X_seqs,
            test_Y, im_shape, vocab_size, num_answers, all_answers, test_qs,
            test_answer_indices)  # for the analyze script
