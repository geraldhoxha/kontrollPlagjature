# Modeli i krijuar 'Plagjature'
from model import Plagjature

# Librarite e nevojshme
from colorama import Fore, Back, Style, init
import sys
import os


# Funksioni qe kthen te dhenat per konfigurim
# Ky funksion kthen ne True ose False perzgjedhjet e perdoruesit
def konfigurimet():

    # Afishon nje nga nje menune e konfigurimeve
    print(f"\n{Style.BRIGHT}{Fore.GREEN}Perfshire skedaret 'Text'? " +
    f"{Fore.YELLOW}Shkruani 'Po' ose 'Jo': {Style.RESET_ALL}", end=" ")
    text = input()
    print(f"\n{Style.BRIGHT}{Fore.GREEN}Perfshire skedaret 'Word'? "+
    f"{Fore.YELLOW}Shkruani 'Po' ose 'Jo': {Style.RESET_ALL}" , end=" ")
    docxs = input()
    print(f"\n{Style.BRIGHT}{Fore.GREEN}Perfshire skedaret 'PDF'? " +
    f"{Fore.YELLOW}Shkruani 'Po' ose 'Jo': {Style.RESET_ALL}" , end=" ")
    pdfs = input()

    # Kontrollon nese pergjigja eshte pozitive, ne te kundert nuk perzgjidhen skedaret TXT
    text = True if text == 'true'\
            or text == 'True' \
            or text == 'Po'\
            or text == 'po'\
            or text == 'Yes'\
            or text == 'yes'\
            or text == 'y'\
            or text == 'Y'\
            or text == 'p'\
            or text == 'P'\
        else False

    # Kontrollon nese pergjigja eshte negative, ne te kundert perzgjidhen skedaret DOCX
    docxs = False if docxs == 'false'\
            or docxs == 'False'\
            or docxs == 'Jo'\
            or docxs == 'jo'\
            or docxs == 'No'\
            or docxs == 'no'\
            or docxs == 'n'\
            or docxs == 'N'\
            or docxs == 'j'\
            or docxs == 'J'\
        else True

    # Kontrollon nese pergjigja eshte negative, ne te kundert perzgjidhen skedaret PDF
    pdfs = False if pdfs == 'false'\
            or pdfs == 'False'\
            or pdfs == 'Jo'\
            or pdfs == 'jo'\
            or pdfs == 'No'\
            or pdfs == 'no'\
            or pdfs == 'n'\
            or pdfs == 'N'\
            or pdfs == 'j'\
            or pdfs == 'J'\
        else True

    # Kthen tre variablat per konfigurim
    return text, docxs, pdfs


# Kontrollon para ekzekutimit te programit nese perdoruesi perzgjedh 1 skedar
# per tu kontrolluar
def check_one_file():
    try:
        # Ruan emrin e skedarit ne nje variabel
        skedari = [i for i in sys.argv if i.startswith("-file=")][-1].split('=')[1]

        # Kthen nje error nese skedari nuk ekziston ne direktor
        if skedari not in os.listdir():
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}Skedari i nuk ekziston ne direktori {Back.RED}!{Style.RESET_ALL}")
            return 'Error'

        '''
        Sintaksa per perzgjedhjen e nje skedari eshte:

                -file=< EMRI I SKEDARIT >
        '''
        # Kthen emrin e skedarit te perzgjedhur
        return skedari
    except:

        # Nese perdoruesi nuk kerkon nje skedar te vetem
        return False


# Funksioni qe ekzekuon programin
def runApp(save, singlefile=False):

    # Ruan variablat per konfigurim
    text, docxs, pdfs = konfigurimet()

    # Inicializon modelin me pergjigjen e funksionit 'check_one_file'
    app = Plagjature(singlefile)

    # Ekzekuton programin
    app.configurim(include_txt=text, include_docx=docxs, include_pdf=pdfs)

    # Ruan ne CSV
    if save:
        app.saveCSV()

    # Shfaq te dhenat ne CLI
    app.shfaq_te_dhenat()

def _help():
 
    try:
        return True if "help" or "-help" in sys.argv else False
    except:
        return False



if __name__=="__main__":
    # Inicializon ngjyrat e kerkuara ne program (Globale)
    init()

    '''
    Sintaksa per ruajtjen e skedarit ne CSV eshte:

            -save
    '''

    # Kthen True nese perdoruesi kerkon te ruhet ne CSV, perndryshe kthen False
    csv = True if '-save' in sys.argv else False

    # Ruan ne nje variabel pergjigjen e funksionit 'check_one_file'
    singlefile = check_one_file()

    if singlefile == 'Error':
        sys.exit()
    
    if _help:
        print('\nShkruani "checkfiles" dhe prisni disa sekonda (ne varesi te numrit te skedareve).', end="\n\n")
        print('Programi do te filloje dhe ju do shkruani "po" ose "jo" konfigurimeve.')
        print("\t    Konfigurimet jane:")
        print("\t\t        -Deshironi skedaret .txt (nese e lini bosh, programi NUK do te skanoje skedaret .txt)")
        print('\t\t        -Deshironi skedaret .docx (nese e lini bosh, programi DO TE skanoje skedaret .docx "Word")')
        print('\t\t        -Deshironi skedaret .pdf (nese e lini bosh, pogrami DO TE skanoje skedaret .pdf "PDF"', end="\n\n")

        print("Rezultatet do te jene nje krahasim ndermjet skedareve, si the do kene nje ngjyre korensponduese qe nenkuptojne:")
        print('\t\t        -Jeshile:	Ngjashmeri e dobet')
        print('\t\t        -E verdhe:	Ngjashmeri mesatare')
        print('\t\t        -E kuqe:	Ngjasmeri e larte')
        print("\n\n\n")

        print(f'{"-" * 100}')
        print("Funksione te programit:")
        print("|\t-save:\t\t Ruan rezultatet ne nje format .csv. Sintaksa: [ checkfiles --save ]")
        print("|\t-file:\t\t Specifikon skedarin per krahasimin. Sintaksa: [ checkfile -file='EMRI I SKEDARIT']")
        print("\nShembull:")
        print("\t\t[ checkfiles -save -file=Cloud_Programming.pdf ]")
        sys.exit()

    # Ekzekuton programin
    runApp(csv, singlefile)
