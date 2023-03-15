import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def update_image():
    print("slika")

def request_body():
    request_body ={

		"nadm_visina": 299,
        "benzen": 1,
        "ge_sirina": 46.065851,
        "ge_dolzina": 14.517454,
        "pm2.5": 35.61,
        "o3": 51.407,
        "co": 0.452,
        "no2": 24.180,
        "so2": 3.21,
        "CE Ljubljanska": 0,
        "CE bolnica": 0,
        "Hrastnik": 0,
        "Iskrba": 0,
        "Koper": 0,
        "Kranj": 0,
        "Krvavec": 0,
        "LJ Bežigrad": 1,
        "LJ Celovška": 0,
        "LJ Vič": 0,
        "MB Titova": 0,
        "MB Vrbanski": 0,
        "MS Cankarjeva": 0,
        "MS Rakičan": 0,
        "NG Grčna": 0,
        "Novo mesto": 0,
        "Otlica": 0,
        "Ptuj": 0,
        "Rečica v I.Bistrici": 0,
        "Trbovlje": 0,
        "Zagorje": 0,
	    "promet": 90.500
	
	}

def reorder(df):
    new_data = pd.DataFrame()
    new_data['pm2.5'] = df['pm2.5']
    new_data['nadm_visina'] = df['nadm_visina']
    new_data['o3'] = df['o3']
    new_data['benzen'] = df['benzen']
    new_data['ge_sirina'] = df['ge_sirina']
    new_data['co'] = df['co']
    new_data['no2'] = df['no2']
    new_data['ge_dolzina'] = df['ge_dolzina']
    new_data['so2'] = df['so2']
    new_data['CE Ljubljanska'] = df['CE Ljubljanska']
    new_data['CE bolnica'] = df['CE bolnica']
    new_data['Hrastnik'] = df['Hrastnik']
    new_data['Iskrba'] = df['Iskrba']
    new_data['Koper'] = df['Koper']
    new_data['Kranj'] = df['Kranj']
    new_data['Krvavec'] = df['Krvavec']
    new_data['LJ Bežigrad'] = df['LJ Bežigrad']
    new_data['LJ Celovška'] = df['LJ Celovška']
    new_data['LJ Vič'] = df['LJ Vič']
    new_data['MB Titova'] = df['MB Titova']
    new_data['MB Vrbanski'] = df['MB Vrbanski']
    new_data['MS Cankarjeva'] = df['MS Cankarjeva']
    new_data['MS Rakičan'] = df['MS Rakičan']
    new_data['NG Grčna'] = df['NG Grčna']
    new_data['Novo mesto'] = df['Novo mesto']
    new_data['Otlica'] = df['Otlica']
    new_data['Ptuj'] = df['Ptuj']
    new_data['Rečica v I.Bistrici'] = df['Rečica v I.Bistrici']
    new_data['Trbovlje'] = df['Trbovlje']
    new_data['Zagorje'] = df['Zagorje']
    new_data['promet'] = df['promet']
    return new_data


def predict():
    object_json = request.json
    df = pd.json_normalize(object_json)
    df = reorder(df)
    print(object_json)

    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))
    model_path = os.path.join(root_dir, 'models', 'linear')

    f = open(model_path, 'rb')
    model = pickle.load(f)

    prediction = model.predict(df)
    return jsonify({'prediction': prediction[0]})






#GUI
root = tk.Tk()
root.title("Air quality")

root.geometry("500x200")

#rule_label = tk.Label(root, text="Rule:")
#rule_entry = tk.Entry(root, width=10)
#Avtomatsko nastavljeno pravilo na 190
#rule_entry.insert(0, "190")

OPTIONS = [
    "CE Ljubljanska",
    "CE bolnica",
    "Hrastnik",
    "Iskrba",
    "Koper",
    "Kranj",
    "Krvavec",
    "LJ Bežigrad",
    "LJ Celovška",
    "LJ Vič",
    "MB Titova",
    "MB Vrbanski",
    "MS Cankarjeva",
    "MS Rakičan",
    "NG Grčna",
    "Novo mesto",
    "Otlica",
    "Ptuj",
    "Rečica v I.Bistrici",
    "Trbovlje",
    "Zagorje"
] 


variable = tk.StringVar(root)
variable.set(OPTIONS[0]) # default value

w = tk.OptionMenu(root, variable, *OPTIONS)
w.pack()

def ok():
    print ("value is:" + variable.get())

button1 = tk.Button(root, text="OK", command=ok)
button1.pack()

button = tk.Button(root, text="Update", command=update_image)
button.pack()
figure = plt.figure(figsize=(10, 7))
canvas = FigureCanvasTkAgg(figure, master=root)

#rule_label.grid(row=0, column=0)
#rule_entry.grid(row=0, column=1)
#button.grid(row=0, column=2)
#canvas.get_tk_widget().grid(row=1, columnspan=3)

update_image()

root.mainloop()
