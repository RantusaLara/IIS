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
        "LJ Bežigrad": 0,
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

#request_body["benzen"] = 3
#print(request_body.get("benzen"))

variable = "Zagorje"

if variable == "MB Titova":
    request_body["nadm_visina"] = 200
    request_body["ge_sirina"] = 15.458585
    request_body["ge_dolzina"] = 14.585858
    request_body["MB Titova"]

print(request_body)
