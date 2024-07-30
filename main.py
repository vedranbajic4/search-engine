import pickle
import re
from pdfminer.high_level import extract_text
from pdfminer.pdfpage import PDFPage
from reportlab.lib import colors

from classes import Result, Trie
from fpdf import FPDF

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

pdf = FPDF('P', 'mm', 'Letter')
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font('times')
ca = canvas.Canvas("res.pdf", pagesize=letter)

BROJ_RECI = 6
BROJ_ISPISA = 6
PDF_PATH = "book.pdf"
reci = []  #reci za pretragu
resultati = []
tries = []
graf = {}
rec_pojava = []
didumean = {}

boolean_symbols = ["AND", "OR", "NOT"]
tokens = []


stranice_koje_valjaju = {}


def nadji_tekst(pg):
    reci2 = []
    for r in reci:
        if r[-1] == '*':
            reci2.append(r[:-1])
    ceoret = []
    with open(PDF_PATH, "rb") as file:
        text = extract_text(PDF_PATH, page_numbers=[pg])
        text = re.split(r'[ ,\n]+', text)
        for i in range(len(text)):
            if text[i].lower() in reci:
                ret = ""
                for i in range(max(0, i-BROJ_ISPISA), min(i+BROJ_ISPISA, len(text))):
                    ret = ret + text[i] + " "
                ceoret.append(ret)

            for r in reci2:
                if text[i][0:len(r)].lower() == r:
                    ret = ""
                    for i in range(max(0, i - BROJ_ISPISA), min(i + BROJ_ISPISA, len(text))):
                        ret = ret + text[i] + " "
                    ceoret.append(ret)

    #print(len(ceoret))
    return ceoret


def pretrazi(rec):
    global resultati, rec_pojava
    #print("Pretrazujem: ", rec)

    for i in range(len(tries)):
        t = tries[i]
        num = t.search(rec)
        if len(rec_pojava) <= i:
            rec_pojava.append({rec: num})
        else:
            rec_pojava[i][rec] = num


def input_serialized_data():
    global tries, didumean, graf
    with open("data/data1.pickle", "rb") as file:
        tries = pickle.load(file)

    with open("data/data2.pickle", "rb") as file:
        graf = pickle.load(file)

    with open("data/data3.pickle", "rb") as file:
        didumean = pickle.load(file)


def ispisi_najcesce():
    #print("ispis najcesce")

    for r in reci:
        for i in range(len(r) - 1):
            s = r[:i] + r[i + 1:]
            #print(s)
            if s in didumean:
                print("Did you mean " + s + "?")


def prikazi_rezultate():
    global resultati, stranice_koje_valjaju
    resultati.sort()
    #draw_highlighted_text(ca, 100, 750, "neki drugi tesktje python text", ["python"])

    max = -1
    for i in range(len(resultati)):
        if not resultati[i].postoji():
            max = i
            break

    br2 = 0
    #print("Rezultat pretrage:")
    for i in range(len(resultati)):
        #print(i, " ", br2, " ", BROJ_ISPISA)

        if not resultati[i].postoji():
            #print("Jel moguce da breakuje")
            break

        #print(resultati[i].get_weight())
        #print("Index ", resultati[i].get_index(), " strr: ", stranice_koje_valjaju[resultati[i].get_index()])
        if not stranice_koje_valjaju[resultati[i].get_index()]:
            continue

        granica = 24
        x = 80
        br = 0
        y = 750
        sv_reci = ""
        for r in reci:
            sv_reci = sv_reci + r + " "
        te = "Index stranice " + str(resultati[i].get_index()) + " ---------- Searching for: " + sv_reci
        draw_highlighted_text(ca, x, y, te, ["@@@@"])
        y = 700
        x = 100
        lista = nadji_tekst(resultati[i].get_index())
        print("...")
        for j in lista:
            draw_highlighted_text(ca, x, y, j, reci)
            y -= 30
            br += 1
            if br >= granica:
                y = 700
                x = 100
                ca.showPage()
                br = 0

        ca.showPage()

        resultati[i].add_text(lista)
        resultati[i].ispisi_rez(reci)

        if br2 % BROJ_ISPISA == (BROJ_ISPISA - 1):
            print(" Zelite li jos ", BROJ_ISPISA, " rezultata: 1/2 (da/ne)")
            opcija = input()

            if opcija != "1":
                break
        br2 += 1

    if max <= BROJ_ISPISA:
        ispisi_najcesce()


def izracunaj(c1, op, c2):
    if op == "AND":
        return c1 > 0 and c2 > 0
    elif op == "OR":
        return c1 > 0 or c2 > 0
    elif op == "NOT":
        return c1 > 0 >= c2
    else:
        print("Greska kod operacije: ", c1, op, c2)


'''
graf:
143  ->  51
303  ->  141
607  ->  57
'''


def sredi_rezultate():
    global resultati, stranice_koje_valjaju, bolean_izraz
    stranice_koje_valjaju = {}
    resultati = []
    bolean_izraz = False
    for e in tokens:
        if e in boolean_symbols:
            bolean_izraz = True

    if bolean_izraz: # moram da racunam expression! !! ! 1
        for i in range(len(tries)): # idem kroz svaku stranicu, i moram da izracunam izraz. Kad to dobijem, ostalo je easy
            stek = []
            #print("Tokeni: ")
            for t in tokens:
                #print(t, end=" ")
                if t != ')':
                    stek.append(t)
                else:   # dobio sam ), skidam zadnja 3 i izracunam
                    c1 = stek.pop()
                    op = stek.pop()
                    c2 = stek.pop()
                    stek.pop()  # skidam ( npr: (((c2 op c1
                    x1 = 0
                    x2 = 0

                    if c1 == "@@@@@@@@@@":
                        x1 = 1
                    elif c1 == "##########":
                        x1 = 0
                    else:
                        x1 = rec_pojava[i][c1]

                    if c2 == "@@@@@@@@@@":
                        x2 = 1
                    elif c2 == "##########":
                        x2 = 0
                    else:
                        x2 = rec_pojava[i][c2]

                    if izracunaj(x2, op, x1):
                        stek.append("@@@@@@@@@@")
                    else:
                        stek.append("##########")
            '''print("")
            print("Stek: ")
            for s in stek:
                print(s, end=" ")
            print("")'''
            # kad sam prosao kroz sve, mogu da imam viska ali bez zagrada(nadam se) i to samo redom iscepam
            while len(stek) > 1:
                c1 = stek.pop()
                op = stek.pop()
                c2 = stek.pop()
                #stek.pop()  # skidam ( npr: (((c2 op c1 TOGA OVDE NEMA
                x1 = 0
                x2 = 0

                if c1 == "@@@@@@@@@@":
                    x1 = 1
                elif c1 == "##########":
                    x1 = 0
                else:
                    x1 = rec_pojava[i][c1]

                if c2 == "@@@@@@@@@@":
                    x2 = 1
                elif c2 == "##########":
                    x2 = 0
                else:
                    x2 = rec_pojava[i][c2]

                if izracunaj(x2, op, x1):
                    stek.append("@@@@@@@@@@")
                else:
                    stek.append("##########")
            poslednji = stek.pop()
            if poslednji == "@@@@@@@@@@":
                stranice_koje_valjaju[i] = True
            else:
                stranice_koje_valjaju[i] = False
            #print(poslednji)
    else:
        for i in range(len(tries)):
            stranice_koje_valjaju[i] = True

    for i in range(len(tries)):
        w = 0
        while True:
            br = 0
            for v in rec_pojava[i].values():
                if v > 0:
                    br += 1
            if br == 0:
                break
            rec_pojava[i] = {key: value - 1 for key, value in rec_pojava[i].items()}
            w += br * br

        resultati.append(Result(i, w))

    for e in graf:
        for x in graf[e]:
            n1 = e + 21
            n2 = x + 21
            # n1 -> n2
            #print(n1, " -> ", n2)
            if resultati[n2].get_weight() == 0:  # necu da dodajem weight na stranicu gde nema reci, koja ima 0
                continue

            resultati[n2].add_weight(resultati[n1].get_weight() // 2)  # za broj pojavljivanja na prvoj stranici
            resultati[n2].add_weight(4)  # za vezu


def autocomplete(exp):
    br = 0
    nove_reci = []
    sorted_dict = dict(sorted(didumean.items(), key=lambda item: item[1], reverse=True))
    for r in sorted_dict:
        if r[:len(exp) - 1] == exp[:-1] and len(r) >= len(exp):
            print("Opcija : ", br, " ", r)
            br += 1
            nove_reci.append(r)
            if br == 3:
                break
    try:
        op = eval(input("Unesite opciju: "))
        return nove_reci[op]
    except Exception as e:
        print("Nije dobro nesto")
        return "-1"


def sredi_izraz(exp):
    global reci, resultati, rec_pojava, tokens

    tokens = find_words_and_tokens(exp)

    resultati = []
    reci = []
    rec_pojava = []

    for e in tokens:
        if e not in boolean_symbols and e != '(' and e != ')':
            reci.append(e)

    if exp[-1] == '#':
        exp = autocomplete(exp)
        if exp == "-1":
            return
        reci = [exp]


def make_trie(text):
    words = re.split(r'[ ,\n]+', text)

    t = Trie()
    for elem in words:
        if elem not in didumean:
            didumean[elem.lower()] = 0
        didumean[elem.lower()] += 1

        t.insert(elem.lower())
        #print(elem, end=" ")
    tries.append(t)
    #print(45*"_")


def search_word(word):
    word = word.lower()
    for i in range(len(tries)):
        t = tries[i]
        brpon = t.search(word)
        #print("Na stranici: ", i, " brpon == ", brpon)


# Funkcija za ekstrakciju teksta iz PDF-a stranicu po stranicu
def extract_text_by_page():
    global graf, tries
    pattern = r'(?:see|go to|look on|visit|more on|look|on|of|to) page (\d+)'
    ukupno = 0
    with open(PDF_PATH, "rb") as file:
        for page_num, page in enumerate(PDFPage.get_pages(file)):
            text = extract_text(PDF_PATH, page_numbers=[page_num])
            make_trie(text)
            matches = re.findall(pattern, text, re.IGNORECASE)
            # pravljenje grafa
            graf[page_num] = []
            if len(matches) > 0:
                print(page_num, " - >")
            for e in matches:
                graf[page_num].append(int(e) + 21)
                print(int(e) + 21, end=" ")
                ukupno += 1
            if len(matches) > 0:
                print("")

            if page_num % 10 == 0:
                print(page_num)

    #with open("data/data3.pickle", "wb") as file:
    #    pickle.dump(didumean, file)
    print("Ukupno : ", ukupno)
    with open("data/data2.pickle", "wb") as file:
        pickle.dump(graf, file)

    #with open("data/data1.pickle", "wb") as file:
    #    pickle.dump(tries, file)
    exit(0)


def draw_highlighted_text(ca, x, y, text, highlight_words, highlight_color=colors.yellow):
    words = text.split()
    ca.setFont("Helvetica", 12)
    #print(ca)
    for word in words:
        word_width = ca.stringWidth(word, "Helvetica", 12)
        if word.lower() in highlight_words:
            #print("wordddd")
            ca.setFillColor(highlight_color)
            ca.rect(x, y - 2, word_width, 14, fill=1)
        ca.setFillColor(colors.black)
        ca.drawString(x, y, word)
        x += word_width + ca.stringWidth(" ", "Helvetica", 12)


def find_words_and_tokens(expression):
    pattern = r'[a-zA-Z0-9_]+\b|NOT|AND|OR|[()]'
    tokens = re.findall(pattern, expression, flags=re.IGNORECASE)
    return tokens


if __name__ == '__main__':
    '''pdf_file = "res.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    
    print(c)'''
    #extract_text_by_page()
    #draw_highlighted_text(ca, 100, 750, "wje python text", ["python"])
    input_serialized_data()

    while True:
        izraz = input("Unesite izraz za pretragu: ")
        if izraz == "-1":
            print("IZLAZAK")
            break

        sredi_izraz(izraz)
        for e in reci:
            pretrazi(e)
        sredi_rezultate()

        prikazi_rezultate()
        #print("\n\n")

    ca.save()
