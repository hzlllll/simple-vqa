from PIL import Image, ImageTk

import tkinter.filedialog
import tkinter as tk
from prepare_data import setupbyPath
from keras.models import load_model
import numpy as np

window = tk.Tk()


def selectPath():
    path_ = tk.filedialog.askopenfilename()
    path.set(path_)

    print(path_)
    global train_X_ims
    global train_X_seqs
    global all_answers
    global num_answers
    train_X_ims, train_X_seqs, train_Y, train_qs, train_as, num_answers, all_answers = setupbyPath(
        path_)
    img = Image.open(path_)
    photo = ImageTk.PhotoImage(img)
    Lab = tk.Label(window, image=photo)
    Lab.image = photo
    Lab.grid(row=1, column=0)

    train_X_ims = np.array(train_X_ims)
    train_X_seqs = np.array(train_X_seqs)
    asns = ""
    qss = ""
    for i in range(len(train_qs)):
        qss += train_qs[i] + '\n'
        asns += train_as[i] + '\n'
    qs.set(qss)
    asn.set(asns)


def pred():
    predictions = model.predict(
        {
            'input_1': train_X_ims,
            'input_2': train_X_seqs
        }, )
    for idx in range(num_answers):
        answer = all_answers[idx]
        #print(f'\nStatistics for answer {idx}, {answer}')
    passn = ""
    for i in range(len(predictions)):
        #print(np.argmax(predictions[i]))
        passn += all_answers[np.argmax(predictions[i])] + '\n'
    pas.set(passn)
    # Lab = tk.Label(window, text=all_answers[np.argmax(predictions[i])])
    # Lab.text = all_answers[np.argmax(predictions[i])]
    # Lab.grid(row=2 + i, column=3)
    print(predictions, all_answers)


model = load_model('model_num.h5')
window.title('my window')
window.geometry('1200x600')
path = tk.StringVar()
qs = tk.StringVar()
asn = tk.StringVar()
pas = tk.StringVar()

qsL = tk.Label(window, textvariable=qs)
qsL.grid(row=2, column=0)
asL = tk.Label(window, textvariable=asn)
asL.grid(row=2, column=1)
pasL = tk.Label(window, textvariable=pas)
pasL.grid(row=2, column=2)
tk.Label(window, text="目标路径:").grid(row=0, column=0)
tk.Entry(window, width=100, textvariable=path).grid(row=0, column=1)
tk.Button(window, text="路径选择", command=selectPath).grid(row=0, column=2)
tk.Button(window, text="预测", command=pred).grid(row=0, column=3)
# 这里是窗口的内容

window.mainloop()