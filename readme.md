# Kontroll plagjature

Ndiq instruksionet e thjeshta te instalimit per perdorimin e programit

## Instalimi i librarive

Librarite e nevojshme jane te ruajtura ne skedarin 'requirements.txt'.
Mund te instalohen nje nga nje me komanden:
```bash
pip install "emri i librarise"
```


...ose mund te instalohen njeheresh me komanden:

```bash
pip install -r requirements.txt
```

## Perdorimi

Per te perdorur programin, ne te njejten direktori duhet te ndodhen dhe skedaret qe do te kontrollosh.
Pasi i ke kopjuar skedaret ne direktori, shkruaj ne cli komandat e meposhtme:
```bash
python app.py --save -file="emrin e skedarit qe do te kontrollosh"
```


## Krijimi i nje programi

Per te krijuar nje program qe mund ta aksesosh kudo ne kompjuter, ndiq hapat e meposhtme:

#### 1. Krijimi i skedarit .exe
Hap cmd ne direktorine perkatese dhe fut komanden e meposhtme
```bash
pyinstaller app.py --name=checkfiles --icon=logo.ico
```
! Kjo do te zgjase 2-3 minuta.

#### 2. Perditeso variablat e mjedisit

Pasi instalimi te kete perfunduar, futu ne direktorite
-> dist -> checkfiles dhe kopjo linkun.
P.sh: C:\Users\User\Desktop\MyProgram\dist\checkfiles

  ##### 2.1 

Kliko butonin START dhe kerko "environment variables"

  ##### 2.2

Kliko ne fund te 'Enviroment Variables'

  ##### 2.3

Ne dritaren e re qe do te hapet, te paneli i pare kliko dy here ne 'Path'

  ##### 2.4

Kliko 'New', dhe me pas fut linkun qe ke kopjuar.

P.sh: C:\Users\User\Desktop\MyProgram\dist\checkfiles

#### 3. Testimi i programit

Programi tani eshte global ne kompjuter. Mund te hapesh cmd ne cdo direktori dhe te klikosh komandat per kontroll si me posht:

```bash
python app.py --save -file="skedari juaj"
```

#### Note
 - Ka probleme
 - Duhet perditsuar
