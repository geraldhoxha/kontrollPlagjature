#Librarite e nevojshme 

# TfidfVectroeizer kthen ne vektor tipin string
from sklearn.feature_extraction.text import TfidfVectorizer

# Cosine_similarity mbart funksionin matematikor 
#    n                 /   ___________         ____________
#   Shuma(Ai * Bi)   /   \/Shuma(Ai^2)   *   \/Shuma(Bi^2)
#    i=1           /
from sklearn.metrics.pairwise import cosine_similarity

# Extract_text mundeson perpunimin e skedareve PDF
from pdfminer.high_level import extract_text

# Mundeson ngjyrat e ndryshme ne CMD
from colorama import Fore, Back, Style

# Extract_text mundeson perpunimin e skedareve DOCX
from docx import Document

#Mundeson perpunimin e kornizave te te dhenave
import pandas as pd

# Mundeson funksione qe nderveprojne me sistemin operativ
import os


# Modeli i objektit 
class Plagjature:

    # Liste boshe qe do te ruhen te dhenat e perpunuara dhe
    # jo te perpunuara
    studentet = []
    provimet = []
    vektoret = []
    list_vektoresh = []
    rezultatet = []
    text = []

    # Funksionet qe do te ekzekutohen kur objekti te krijohet
    def __init__(self, oneFile=None):
        self.oneFile = oneFile
        # Pastron CLI
        os.system("cls")

    # Lexon te gjitha skedaret DOCX ne direktori
    def getDocx(self):

        # Merr titujt e skedareve DOCX ne direktori
        docx_files = [sked for sked in os.listdir() if sked.endswith('.docx')]

        # Shton ne listen 'studentet' te gjithe emrat e skedareve
        self.studentet += [sked for sked in docx_files]

        # Krijon nje varg tekstesh nga DOCX
        provimet_docx = []
        for skedar in docx_files:
            doc = Document(skedar)

            # Mbledh cdo paragraf dhe e shton ne 'fullText'
            fullText = []
            for para in doc.paragraphs:
                fullText.append(para.text)
            fullText = '\n'.join(fullText)
            provimet_docx.append(fullText)

        # Perditeson variablin qe ruan te dhenat qe do te krahasohen
        self.provimet += [sked for sked in provimet_docx]

    # Lexon te gjitha skedaret PDF    
    def getPDF(self):

        # Merr titujt e skedareve PDF per tu lexuar
        pdf_file = [sked for sked in os.listdir() if sked.endswith('.pdf')]

        # Shton ne listen e studenteve te gjithe emrat e skedareve
        self.studentet += [sked for sked in pdf_file]

        # Krijon nje varg me skedaret PDF
        provimet_pdf = []
        for pdf in pdf_file:
            file = extract_text(pdf)
            provimet_pdf.append(file)

        # Perditeson variablin qe ruan te dhenat qe do te krahasohen
        self.provimet += [sked for sked in provimet_pdf]

    # Konfigurimi per krahasim te skedareve
    def configurim(self, include_txt=False, include_docx=True, include_pdf = True):

        # Shton ne listen e krahasuesve skedaret TXT
        if include_txt:
            self.studentet = [sked for sked in os.listdir() if sked.endswith('.txt')]
            self.provimet = provimet = [open(sked).read() for sked in self.studentet]

        # Shton ne listen e krahasuesve skedaret DOCX
        if include_docx:
            self.getDocx()

        # Shton ne listen e krahasuesve skedaret PDF
        if include_pdf:
            self.getPDF()

        try:

            # Vektorizon te gjithe skedaret me metoden TfIDf (Tterm Frequency–Inverse Document Frequency)
            self.vektoret = self.vektorizim(self.provimet)

            # Krion nje list vektoresh ku secili vektor permban:
            #   1: Emrin e skedarit
            #   2: Te gjithe skedaret e vektorizuar per krahasim
            self.list_vektoresh = list(zip(self.studentet, self.vektoret))

            # Ruan rezuktatet ne nje variabel "rezultatet"
            self.rezultatet = self.kontrollo_plagjature()
        except:

            # Shfaq nje 'error' nese nuk ka te dhena ose konfigurimet nuk perzgjedhin asnje skedar
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}Konfigurimet nuk perzgjedhin asjne skedar {Back.RED}!{Style.RESET_ALL}")
        

    # Funksioni qe kthen nje list te vektorizuar te tekstit
    def vektorizim(self, tekst):
        return TfidfVectorizer().fit_transform(tekst).toarray()
    
    # Funksioni qe kryen krahasimin e skedareve sipas 'cosine similarity'
    def krahasim(self, sked1, sked2):
        return cosine_similarity([sked1, sked2])
    
    # 
    def kontrollo_plagjature(self):
        rezultatet = set()
        
        # Krahason 1 skedar te vetem me te gjith te tjeret ne direktori
        if self.oneFile:

            # Ruan emrin dhe tekstin e skedarit qe do te krahasohet me te tjeret
            emer_sked, te_dhenat = [(emer_sked,te_dhenat)
                    for emer_sked,te_dhenat
                    in self.list_vektoresh
                    if emer_sked == self.oneFile][0]

            # Fshin skedarin qe do te kontrollohet nga lista e ku mbahen skedaret per krahasim
            del self.list_vektoresh[self.list_vektoresh.index((emer_sked,te_dhenat))]

            # Fillon krahasimin e skedareve
            for student_1, provim_1 in self.list_vektoresh:
                ngjashmeria = self.krahasim(te_dhenat, provim_1)[0][1]
                grup_student = sorted((emer_sked, student_1))
                
                # Ruan te dhenat ne nje variabel
                krahasimi = (grup_student[0], grup_student[1], round(float(ngjashmeria),2)*100)
                rezultatet.add(krahasimi)

        else:
            
            # Nese nuk kemi specifikuar 1 skedar per krahasim,
            # programi do te krahasoje skedaret me njeri tjetri
            for student_1, provim_1 in self.list_vektoresh:

                # Kopjon skedarin origjinal dhe krahason cdo skedar ne variablen e kopjuar
                # bashke me skedaret e variables origjinale
                vektor_i_ri = self.list_vektoresh.copy()
                indeksi_aktual = vektor_i_ri.index((student_1, provim_1))

                # Skedari i radhes ne variablen e kopjuar fshihet ne menyre qe
                # nje skedar te mos krahasohet me veten
                del vektor_i_ri[indeksi_aktual]

                # Fillon krahasimin
                for student_2, provim_2 in vektor_i_ri:
                    ngjashmeria = self.krahasim(provim_1, provim_2)[0][1]
                    grup_student = sorted((student_1, student_2))

                    # Ruan te dhenat ne nje variabel
                    krahasimi = (grup_student[0], grup_student[1], round(float(ngjashmeria),2)*100)
                    rezultatet.add(krahasimi)
        return rezultatet


    # Funksioni qe afishon te dhenat ne CLI
    def shfaq_te_dhenat(self):
        print("\n")

        # Tregon me ngjyra te ndryshme nivelin e ngjashmerise
        for rezult in self.rezultatet:
            if rezult[2] > 70:
                indigator = Back.RED 
            elif rezult[2]> 50:
                indigator = Back.YELLOW
            else:
                indigator = Back.GREEN
            print(f'{Fore.WHITE}| '+
                    f'{Fore.CYAN}{rezult[0]} {Fore.WHITE}- '+
                    f'{Fore.CYAN}{rezult[1]}{Fore.WHITE} | -> '+
                    f'{Fore.BLACK}{indigator} {rezult[2]}% '+
                    f'{Style.RESET_ALL}.\n')
            print('\n')
        print("\n")
        os.system("pause")

    # Ruan te dhenat ne nje format CSV
    def saveCSV(self):
        save = pd.DataFrame(self.rezultatet)

        # Vendos si emer kolone emrat qe duhen
        save.rename(columns={0: "Skedar krahasues", 1:"Skedar per krahasim", 2:"Ngjashmeria"}, index=None, inplace=True)
        save.reset_index(drop=True, inplace=True)

        # Ruan formatin CSV
        save.to_csv("rezultatet.csv")
