from flask import Blueprint, render_template, request
import numpy as numpy

mainpage = Blueprint('mainpage', __name__)

A = -0.0088
B = 3.9126
ehitisAluspinValue = [
    [1.8, 3.5, 14.0],
    [1.8, 3.5, 8.5],
    [1.8, 3.5, 7.0],
    [1.5, 2.8, 5.5],
    [1.4, 2.5, 4.5],
    [1.2, 2.1, 3.8],
    [1.0, 1.7, 2.8],
    [0.9, 1.4, 2.2],
    [0.7, 1.1, 1.5],
    [0.6, 0.9, 1.2],
    [0.5, 0.7, 0.9],
]

ehiAluspinKaugusRanges = [
    (0, 1),
    (1.1, 5),
    (5.1, 10),
    (10.1, 20),
    (20.1, 30),
    (30.1, 50),
    (50.1, 100),
    (100.1, 200),
    (200.1, 500),
    (500.1, 1000),
    (1000.1, 2000)
]


@mainpage.route('/', methods=['GET', 'POST'])
def arvuta():
    result = None
    maxVonkeKiirus = None
    checkMethod = 1
    kaugusOhutu = None
    kaugusArvuta = None
    laenguMassArvuta = None
    vonkeKiirusArvuta = None
    laenguMassOhutu = None
    vonkeKiirusOhutu = None
    if request.method == 'POST':
        arvutusMethod = request.form.get('arvutusMethod')
        arvutusObject = request.form.get('arvutusObject')
        vonkeKiirusArvuta = request.form.get('vonkeKiirusArvuta', type=float)
        vonkeKiirusOhutu = request.form.get('vonkeKiirusOhutu', type=float)
        kaugusArvuta = request.form.get('kaugusArvuta', type=float)
        kaugusOhutu = request.form.get('kaugusOhutu', type=float)
        laenguMassArvuta = request.form.get('laenguMassArvuta', type=float)
        laenguMassOhutu = request.form.get('laenguMassOhutu', type=float)
        ehitiseLiik = request.form.get('ehitiseLiik', type=float)
        obejAluspin = request.form.get('objectAluspinnas', type=float)
        ehitiseAluspin = request.form.get('ehitiseAluspinnas', type=int)
        if arvutusObject == "1":
            if arvutusMethod == "1":
                if kaugusArvuta != None and laenguMassArvuta != None:
                    result = vonkeKiirusArvutaFunc(kaugusArvuta, laenguMassArvuta)
                    checkMethod = 1
            elif arvutusMethod == "2":
                if vonkeKiirusArvuta != None and kaugusArvuta != None:
                    result = laenguMassArvutaFunc(vonkeKiirusArvuta, kaugusArvuta)
                    checkMethod = 1
        elif arvutusObject == "2":
            lubatudKiirus = ehitAluspinMaxVonkekiirus(ehitiseAluspin, kaugusOhutu)
            maxVonkeKiirus = vonkeMaxKiirusArvuta(lubatudKiirus, ehitiseLiik)
            result = maxLaenguMassArvuta(maxVonkeKiirus, kaugusOhutu, obejAluspin)
            checkMethod = 2
            maxVonkeKiirus = round(maxVonkeKiirus, 3)
            vonkeKiirusOhutu = vonkeKiirusOhutu / 10  # mm/s to cm/s convertion

    if result is not None:
        result = round(float(result), 3)
    data = {
        "kaugusArvuta": kaugusArvuta,
        "kaugusOhutu": kaugusOhutu,
        "result": result,
        "laenguMassArvuta": laenguMassArvuta,
        "laenguMassOhutu": laenguMassOhutu,
        "vonkeKiirusArvuta": vonkeKiirusArvuta,
        "vonkeKiirusOhutu": vonkeKiirusOhutu,
        "maxVonkeKiirus": maxVonkeKiirus,
        "checkMethod": checkMethod,
    }
    return render_template("main.html", data=data);
    result = None;


def vonkeKiirusArvutaFunc(kaugus, laenguMass):
    ds = kaugus / numpy.sqrt(laenguMass)
    vonkeKiirus = A * ds + B
    return vonkeKiirus


def laenguMassArvutaFunc(vonkeKiirus, kaugus):
    ds = (vonkeKiirus - B) / A
    laenguMass = (kaugus ** 2) / (ds ** 2)
    return laenguMass


def vonkeMaxKiirusArvuta(lubatudKiirus, ehiLiik):
    maxVonkeKiirus = lubatudKiirus * ehiLiik
    return maxVonkeKiirus


def maxLaenguMassArvuta(maxVonkeKiirus, kaugus, pinnas):
    laenguMass = ((maxVonkeKiirus ** 2) * (kaugus ** 2.7)) / (pinnas ** 2)
    return laenguMass


def ehitAluspinMaxVonkekiirus(ehitiseAluspin, kaugus):
    for idx, (low, high) in enumerate(ehiAluspinKaugusRanges):
        if low <= kaugus <= high:
            return ehitisAluspinValue[idx][ehitiseAluspin - 1]
    return 0