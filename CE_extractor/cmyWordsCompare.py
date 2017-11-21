# -*- coding: UTF-8 -*- 

#######################################################################################
# --------------------------------- Function Introduce ------------------------------ #
#######################################################################################
# This functions set intends to:
# 1. read the accdb files
# 2. Get the words set of Abstract and Conclusion
# 3. compare the words used in the CE_relation cases and the words used in Abstract and Conclusion

#######################################################################################
# ---------------------------------- Global variable -------------------------------- #
#######################################################################################
import os
import nltk
import re
import xlwt
import xlrd
import pyodbc
from xlutils.copy import copy
from cmyPackage import *

# --------- set some folder path ------------------
corpdir = os.path.join(os.getcwd(), "Corpus")
pkdir = os.path.join(os.getcwd(), "PK")
TXTcorpdir = os.path.join(os.getcwd(), "Corpus", "TXT")
TXTpkdir = os.path.join(os.getcwd(), "PK", "TXT")
DICpkdir = os.path.join(os.getcwd(), "PK", "DIC")
ctxtdir = os.path.join(os.getcwd(), "CheckTXT")
xlsdir = os.path.join(os.getcwd(), 'XLS')
dbfile = os.path.join(os.getcwd(), 'CErelation.accdb')

#######################################################################################
# ----------------------------------- Check Patterns -------------------------------- #
#######################################################################################        
def Check_C_P_S(text):
    pieces = text.split('. ')
    TypeSheet = []
    for p in pieces:
        if re.match("^[\s]*$", p):  # if p is a empty string
            continue
        elif re.match("[C|P|S][\d]+$", p):
            if p[0] == 'S':
                type = 0
            elif p[0] == 'P':
                type = 1
            else:
                type = 2
            TypeSheet.append([type, int(p[1:])])
        else:
            TypeSheet.append([-1, p])

    return TypeSheet


#######################################################################################
# --------------------------------- Read Database file ------------------------------ #
#######################################################################################
def ReadDB_Ftaglist():
    # ----------- Connect Database --------------
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + dbfile + ";Uid=;Pwd=;")
    cursor = conn.cursor()
    # -------------------------------------------
    FtagSQL = "SELECT Ftag from FileInfo;"
    FtagList = []
    for row in cursor.execute(FtagSQL):
        FtagList.append(row.Ftag)

    cursor.close()
    conn.close()

    return FtagList


def ReadDB_AbsText(ftag):
    # ----------- Connect Database --------------
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + dbfile + ";Uid=;Pwd=;")
    cursor = conn.cursor()
    # -------------------------------------------
    AbsText = []
    AbsSQL = "SELECT text from Sent where Ftag = \'" + ftag + "\' and Ctag = 0"
    for row in cursor.execute(AbsSQL):
        AbsText.append(row.text)

    cursor.close()
    conn.close()

    return AbsText


def ReadDB_ConcText(ftag):
    # ----------- Connect Database --------------
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + dbfile + ";Uid=;Pwd=;")
    cursor = conn.cursor()
    # -------------------------------------------
    ConcCtagSQL = "SELECT Ctag from SecInfo where Ftag = \'" + ftag + "\' and Ctitle in ('Conclusion','conclusion','summary','Summary')"
    try:
        ConcCtag = ((cursor.execute(ConcCtagSQL)).fetchone()).Ctag
    except AttributeError:
        # print ftag, "cannot find the section named as conclusion"
        return ""

    ConcSQL = "SELECT text from Sent where Ftag = \'" + ftag + "\' and Ctag =" + str(ConcCtag)
    ConcText = []

    for row in cursor.execute(ConcSQL):
        ConcText.append(row.text)

    cursor.close()
    conn.close()

    return ConcText


def ReadDB_CEText(ftag):
    # ----------- Connect Database --------------
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + dbfile + ";Uid=;Pwd=;")
    cursor = conn.cursor()
    # -------------------------------------------
    Type = ['Stag', 'Ptag', 'Ctag']
    CESQL = "SELECT ID, Context, A, B from CE_Relation where Ftag = \'" + ftag + "\' order by ID"
    CE_A_Text = []
    CE_B_Text = []

    for row in cursor.execute(CESQL):
        ATypeList = Check_C_P_S(row.A)
        BTypeList = Check_C_P_S(row.B)
        AText = []
        BText = []

        for a in ATypeList:
            if a[0] == -1:
                AText.append(a[1])
            else:
                tempcursor = conn.cursor()
                tempSQL = "SELECT Stag, text from Sent where Ftag = \'" + ftag + "\' and " + Type[a[0]] + " = " + str(
                    a[1]) + " order by Stag"
                for row1 in tempcursor.execute(tempSQL):
                    AText.append(row1.text)
                tempcursor.close()

        for b in BTypeList:
            if b[0] == -1:
                BText.append(b[1])
            else:
                tempcursor = conn.cursor()
                tempSQL = "SELECT Stag, text from Sent where Ftag = \'" + ftag + "\' and " + Type[b[0]] + " = " + str(
                    b[1]) + " order by Stag"
                for row1 in tempcursor.execute(tempSQL):
                    BText.append(row1.text)
                tempcursor.close()

        CE_A_Text.append(AText)
        CE_B_Text.append(BText)

    cursor.close()
    conn.close()
    return [CE_A_Text, CE_B_Text]


#######################################################################################
# --------------------------- Calculate Word Frequency ------------------------------ #
#######################################################################################
### ---- remove pairs in 'Dic' if their keys in 'Removelist' ---- 
def DicRemove(Dic, Removelist):
    for r in Removelist:
        if Dic.has_key(r): del Dic[r]
    return Dic


### ---- count the words in text and update values in 'Dic' ----
def Text2WordDic(Dic, text):
    tokens = nltk.word_tokenize(text)
    for t in tokens:
        t = t.lower()
        if not Dic.has_key(t):
            Dic[t] = 1
        else:
            Dic[t] += 1
    return Dic


### ---- Create FWordDic(f,AbsWordDic,ConcWordDic,A_CWordDic,CEWordDic) for each file in data base file----
def GetWordDic():
    Ftag = ReadDB_Ftaglist()
    FWord = []
    FTextList = []
    # --------- Get SentSet & CE relation cases for each files---------
    for f in Ftag:
        # ****** Get Abstract Words Dictionary ******  
        AbsText = ReadDB_AbsText(f)
        AbsWordDic = {}
        for text in AbsText:
            AbsWordDic = Text2WordDic(AbsWordDic, text)
        # ****** Get Conclusion Words Dictionary ******
        ConcText = ReadDB_ConcText(f)
        ConcWordDic = {}
        for text in ConcText:
            ConcWordDic = Text2WordDic(ConcWordDic, text)
        # ****** Get CE relation cases Words Dictionary ******
        CE_A_Text, CE_B_Text = ReadDB_CEText(f)
        CE_Text = []
        CEWordDic = {}

        for idx, A in enumerate(CE_A_Text):
            B = CE_B_Text[idx]
            for atext in A:
                CE_Text.append(atext)
            for btext in B:
                CE_Text.append(btext)

        for text in CE_Text:
            CEWordDic = Text2WordDic(CEWordDic, text)

        # ****** Get the Abstract & Conclusion union word dict ******
        A_CWordDic = AbsWordDic.copy()
        for k, v in ConcWordDic.items():
            if A_CWordDic.has_key(k):
                A_CWordDic[k] = A_CWordDic[k] + v
            else:
                A_CWordDic[k] = v
        tempFText = FText(f, AbsText, ConcText, CE_Text)
        tempFText.CE_A_Text = CE_A_Text
        tempFText.CE_B_Text = CE_B_Text
        FTextList.append(tempFText)
        FWord.append(FWordDic(f, AbsWordDic, ConcWordDic, A_CWordDic, CEWordDic))

    Dumppickle(os.path.join(DICpkdir, "KGFTextList.pk"), FTextList)
    Dumppickle(os.path.join(DICpkdir, "KGFWordDic.pk"), FWord)

    return FWord


#######################################################################################
# --------------- Calculate percent of common words in CE and Abs&Conc ----------------#
#######################################################################################
def GetCE_AC_CoWordsPercent(FWord):
    # ----------- Get stop words, Punctions------------
    StopW = Loadpickle(os.path.join(pkdir, 'StopW.pk'))
    Puncs = Loadpickle(os.path.join(pkdir, 'Puncs.pk'))
    # ------------Calculate Words Similarity -----------
    FCoWord = []
    Removelist = Puncs + StopW
    for f in FWord:
        # remove Punctions and StopWords from WordDics
        f.AbsWordDic = DicRemove(f.AbsWordDic, Removelist)
        f.ConcWordDic = DicRemove(f.ConcWordDic, Removelist)
        f.A_CWordDic = DicRemove(f.A_CWordDic, Removelist)
        f.CEWordDic = DicRemove(f.CEWordDic, Removelist)
        # calculate each word's rate in each Dict
        SumAWords = float(sum(f.AbsWordDic.values()))
        SumCWords = float(sum(f.ConcWordDic.values()))
        SumACWords = float(sum(f.A_CWordDic.values()))
        SumCEWords = float(sum(f.CEWordDic.values()))
        for a, av in f.AbsWordDic.items():
            f.AbsWordDic[a] = av / SumAWords
        for c, cv in f.ConcWordDic.items():
            f.ConcWordDic[c] = cv / SumCWords
        for ac, acv in f.A_CWordDic.items():
            f.A_CWordDic[ac] = acv / SumACWords
        for ce, cev in f.CEWordDic.items():
            f.CEWordDic[ce] = cev / SumCEWords
        # calculate common words proportion
        OnAbs = 0
        OnConc = 0
        OnAC = 0
        Abs2CE = 0
        Conc2CE = 0
        AC2CE = 0
        ComWOnAbs = []
        ComWOnConc = []
        ComWOnAC = []
        for a, av in f.AbsWordDic.items():
            if f.CEWordDic.has_key(a):
                OnAbs += av
                Abs2CE += f.CEWordDic[a]
                ComWOnAbs.append(a)
        for c, cv in f.ConcWordDic.items():
            if f.CEWordDic.has_key(c):
                OnConc += cv
                Conc2CE += f.CEWordDic[c]
                ComWOnConc.append(c)
        for ac, acv in f.A_CWordDic.items():
            if f.CEWordDic.has_key(ac):
                OnAC += acv
                AC2CE += f.CEWordDic[ac]
                ComWOnAC.append(ac)

        wAbs = 0.0 if len(f.AbsWordDic) == 0 else float(len(ComWOnAbs)) / len(f.AbsWordDic)
        wConc = 0.0 if len(f.ConcWordDic) == 0 else float(len(ComWOnConc)) / len(f.ConcWordDic)
        wAC = 0.0 if len(f.A_CWordDic) == 0 else float(len(ComWOnAC)) / len(f.A_CWordDic)

        FCoWord.append(
            CoWords(f, OnAbs, Abs2CE, OnConc, Conc2CE, OnAC, AC2CE, wAbs, wConc, wAC, ComWOnAbs, ComWOnConc, ComWOnAC))

    Dumppickle(os.path.join(DICpkdir, "KGFCoWord.pk"), FCoWord)
    return FCoWord


#######################################################################################
# --------------------------- Some demonstration functions -------------------------- #
#######################################################################################
def showFText(FTextList):
    for ftext in FTextList:
        print "Current file:", ftext.Ftag
        print "Abstract Text:"
        for abs in ftext.AbsText:
            print "\t", abs
        print "Conclusion Text:"
        for conc in ftext.ConcText:
            print "\t", conc
        print "CE cases Text:"
        for ce in ftext.CEText:
            print "\t", ce
        print "#-------------------------------------------------\n"


def showCoWordPercent(FCoWord):
    for f in FCoWord:
        print (f.FWDic).Ftag
        # print sorted((f.FWDic).CEWordDic.iteritems(),key = lambda asd:asd[1], reverse = True)
        print "OnAbs: " + str(f.OnAbs * 100) + "%"
        print "OnConc: " + str(f.OnConc * 100) + "%"
        print "OnAC: " + str(f.OnAC * 100) + "%"
        print "Abs2CE: " + str(f.Abs2CE * 100) + "%"
        print "Conc2CE: " + str(f.Conc2CE * 100) + "%"
        print "AC2CE: " + str(f.AC2CE * 100) + "%"
        print "WAbs: " + str(f.WAbs * 100) + "%"
        print "WConc: " + str(f.WConc * 100) + "%"
        print "W2AC: " + str(f.WAC * 100) + "%"
        print "ComWOnAbs: "
        print f.ComWOnAbs
        print "ComWOnConc: "
        print f.ComWOnConc
        print "ComWOnAC: "
        print f.ComWOnAC
        print "#-------------------------------------------------"


def CoWord_PK2TXT(CoWordfp, FCoWord):
    CoWordTXT = codecs.open(CoWordfp, 'w', 'utf8')

    for f in FCoWord:
        CoWordTXT.write((f.FWDic).Ftag + "\n")
        CoWordTXT.write("OnAbs: %.4f" % (f.OnAbs * 100) + "%\n")
        CoWordTXT.write("OnConc: %.4f" % (f.OnConc * 100) + "%\n")
        CoWordTXT.write("OnAC: %.4f" % (f.OnAC * 100) + "%\n")
        CoWordTXT.write("Abs2CE: %.4f" % (f.Abs2CE * 100) + "%\n")
        CoWordTXT.write("Conc2CE: %.4f" % (f.Conc2CE * 100) + "%\n")
        CoWordTXT.write("AC2CE: %.4f" % (f.AC2CE * 100) + "%\n")
        CoWordTXT.write("WAbs: %.4f" % (f.WAbs * 100) + "%\n")
        CoWordTXT.write("WConc: %.4f" % (f.WConc * 100) + "%\n")
        CoWordTXT.write("WAC: %.4f" % (f.WAC * 100) + "%\n")
        CoWordTXT.write("ComWOnAbs: \n")
        CoWordTXT.write(str(f.ComWOnAbs) + "\n")
        CoWordTXT.write("ComWOnConc:  \n")
        CoWordTXT.write(str(f.ComWOnConc) + "\n")
        CoWordTXT.write("ComWOnAC:  \n")
        CoWordTXT.write(str(f.ComWOnAC) + "\n")
        CoWordTXT.write("#-------------------------------------------------\n\n\n")

def CoWord_PK2XLS(CoWordXlsfp, FCoWord, newSheetName):
    oldWB = xlrd.open_workbook(CoWordXlsfp, formatting_info=True)
    WB = copy(oldWB)
    # ------------------Creat sheet WS0-------------------
    WS = WB.add_sheet(newSheetName, cell_overwrite_ok='True')
    TitleRow = ['Ftag', 'OnAbs', 'OnConc', 'OnAC', 'Abs2CE', 'Conc2CE', 'AC2CE', 'WAbs', 'WConc', 'WAC']
    for i in range(len(TitleRow)):
        WS.write(0, i, TitleRow[i], xlwt.easyxf('font: bold on'))
    for i, f in enumerate(FCoWord):
        WS.write(i + 1, 0, (f.FWDic).Ftag )
        WS.write(i + 1, 1, "%.4f" % (f.OnAbs * 100))
        WS.write(i + 1, 2, "%.4f" % (f.OnConc * 100))
        WS.write(i + 1, 3, "%.4f" % (f.OnAC * 100))
        WS.write(i + 1, 4, "%.4f" % (f.Abs2CE * 100))
        WS.write(i + 1, 5, "%.4f" % (f.Conc2CE * 100))
        WS.write(i + 1, 6, "%.4f" % (f.AC2CE * 100))
        WS.write(i + 1, 7, "%.4f" % (f.WAbs * 100))
        WS.write(i + 1, 8, "%.4f" % (f.WConc * 100))
        WS.write(i + 1, 9, "%.4f" % (f.WAC * 100))
    WB.save(CoWordXlsfp)


#######################################################################################
# ---------------------------------- Main function ---------------------------------- #
#######################################################################################       
if __name__ == "__main__":
    # FCoWord = GetCE_AC_CoWordsPercent(GetWordDic())
    FCoWord = Loadpickle(os.path.join(DICpkdir, "KGFCoWord.pk"))
    # showCoWordPercent(FCoWord)
    # CoWordfp = os.path.join(ctxtdir, 'CE_AC_CoWordsPercent.txt')
    # CoWord_PK2TXT(CoWordfp, FCoWord)
    CoWordXlsfp = os.path.join(xlsdir, 'figures.xls')
    CoWord_PK2XLS(CoWordXlsfp, FCoWord, 'Man_CE_AC_CoWord')

#######################################################################################
# --------------------------------- Function Results -------------------------------- #
#######################################################################################
# f0001
# OnAbs: 84.1666666667%
# OnConc: 69.8412698413%
# OnAC: 76.8292682927%
# Abs2CE: 28.8232491663%
# Conc2CE: 22.8680323964%
# AC2CE: 34.9690328728%
# WAbs: 78.5714285714%
# WConc: 61.8556701031%
# W2AC: 64.4295302013%
# ComWOnAbs:
# [u'text', u'desirable', u'satisfied', u'paper', u'human', u'previous', u'multi-dimensional', u'rapid', u'forms', u'extends', u'summarizes', u'3', u'half', u'summary', u'automatic', u'methods', u'hard', u'principles', u'dimensions', u'space', u'pictures', u'implicit', u'evaluation', u'core', u'interactions', u'expansion', u'understanding', u'approaches', u'key', u'generate', u'language', u'studied', u'methodology', u'carries', u'citations', u'social', u'suitable', u'neglect', u'automatically', u'behaviors', u'texts', u'2', u'basic', u'form', u'continual', u'extension', u'involved', u'videos', u'century', u'process', u'characteristics', u'diverse', u'physical', u'1', u'empirically', u'complex', u'development', u'cyberspace', u'multiple', u'representations', u'summarization', u'explicit', u'traditional', u'graphs', u'fundamental', u'representation']
# ComWOnConc:
# [u'represent', u'text', u'existing', u'paper', u'human', u'previous', u'readers', u'forms', u'concerns', u'systems', u'summarizes', u'realize', u'evolution', u'cognitive', u'spaces', u'including', u'automatic', u'essential', u'cyberspace', u'hard', u'society', u'video', u'multiple', u'human-level', u'dimensions', u'pictures', u'symbiotic', u'nature', u'implicit', u'method', u'core', u'interactions', u'selecting', u'understanding', u'explore', u'relying', u'carried', u'involved', u'social', u'texts', u'citations', u'basic', u'differences', u'approaches', u'videos', u'diverse', u'writers', u'relies', u'picture', u'reflect', u'representations', u'structure', u'network', u'summarization', u'natural', u'explicit', u'graphs', u'fundamental', u'studying', u'representation']
# ComWOnAC:
# [u'represent', u'text', u'desirable', u'satisfied', u'existing', u'paper', u'human', u'previous', u'multi-dimensional', u'rapid', u'readers', u'forms', u'concerns', u'extends', u'systems', u'summarizes', u'half', u'2', u'realize', u'evolution', u'cognitive', u'summary', u'network', u'spaces', u'including', u'automatic', u'essential', u'empirically', u'methods', u'picture', u'hard', u'principles', u'society', u'video', u'human-level', u'dimensions', u'space', u'pictures', u'symbiotic', u'nature', u'method', u'3', u'evaluation', u'core', u'interactions', u'selecting', u'expansion', u'understanding', u'approaches', u'key', u'carried', u'language', u'studied', u'explore', u'carries', u'social', u'writers', u'suitable', u'neglect', u'automatically', u'texts', u'videos', u'implicit', u'citations', u'basic', u'summarization', u'form', u'differences', u'continual', u'natural', u'extension', u'involved', u'behaviors', u'generate', u'century', u'process', u'characteristics', u'relying', u'diverse', u'physical', u'1', u'methodology', u'complex', u'relies', u'development', u'cyberspace', u'multiple', u'reflect', u'representations', u'structure', u'explicit', u'traditional', u'graphs', u'fundamental', u'studying', u'representation']
# #-------------------------------------------------
# f0002
# OnAbs: 79.0322580645%
# OnConc: 54.1176470588%
# OnAC: 64.6258503401%
# Abs2CE: 37.037037037%
# Conc2CE: 32.4786324786%
# AC2CE: 49.2877492877%
# WAbs: 71.1111111111%
# WConc: 42.1875%
# W2AC: 51.5463917526%
# ComWOnAbs:
# [u'process', u'citation', u'powerful', u'e-science', u'including', u'consists', u'fusing', u'encouraging', u'knowledge', u'managing', u'data', u'solving', u'environment', u'inventing', u'teamwork', u'helps', u'cooperation', u'scientists', u'effectiveness', u'reach', u'flows', u'nodes', u'authors', u'services', u'unselfish', u'implicit', u'advanced', u'network', u'generalizing', u'effective', u'co-authors', u'flow']
# ComWOnConc:
# [u'dynamic', u'including', u'networks', u'knowledge', u'environment', u'helps', u'activities', u'rules', u'evolution', u'team', u'human', u'innovative', u'operation', u'scientists', u'scientific', u'article', u'generate', u'relevant', u'e-science', u'management', u'networking', u'teamwork', u'promote', u'documents', u'development', u'effective', u'flow']
# ComWOnAC:
# [u'relevant', u'powerful', u'e-science', u'including', u'consists', u'fusing', u'management', u'networking', u'knowledge', u'unselfish', u'solving', u'environment', u'teamwork', u'helps', u'activities', u'rules', u'dynamic', u'encouraging', u'implicit', u'inventing', u'promote', u'nodes', u'advanced', u'evolution', u'team', u'generate', u'process', u'citation', u'operation', u'documents', u'network', u'managing', u'networks', u'cooperation', u'scientists', u'effectiveness', u'development', u'scientific', u'innovative', u'human', u'reach', u'flows', u'authors', u'services', u'article', u'data', u'generalizing', u'effective', u'co-authors', u'flow']
# #-------------------------------------------------
# f0003
# OnAbs: 85.0340136054%
# OnConc: 87.6595744681%
# OnAC: 86.6492146597%
# Abs2CE: 32.3146067416%
# Conc2CE: 36.2247191011%
# AC2CE: 43.8651685393%
# WAbs: 78.5714285714%
# WConc: 83.5616438356%
# W2AC: 78.7878787879%
# ComWOnAbs:
# [u'limited', u'abilities', u'semantic', u'spaces', u'human', u'issues', u'previous', u'machine', u'physiological', u'explain', u'environment', u'pre-designed', u'resources', u'rules', u'graph-based', u'realistic', u'individuals', u'including', u'mental', u'intelligence', u'humans', u'discover', u'cyber', u'society', u'loops', u'machines', u'scientific', u'principles', u'space', u'closed', u'limitations', u'ability', u'extend', u'mechanisms', u'multi-disciplinary', u'create', u'emerge', u'linking', u'psychological', u'philosophical', u'establish', u'interact', u'live', u'2', u'structures', u'form', u'explanation', u'cooperate', u'link', u'cp3sme', u'cyber-physical-socio', u'learn', u'expect', u'links', u'computing', u'process', u'characteristics', u'mind', u'images', u'diverse', u'socio', u'lifetime', u'linked', u'ideas', u'1', u'ideal', u'complex', u'solve', u'physical', u'evolve', u'multiple', u'models', u'includes', u'data', u'algorithms', u'fundamental', u'laws']
# ComWOnConc:
# [u'limited', u'emerging', u'semantic', u'guided', u'spaces', u'query', u'issues', u'machine', u'multi-dimensional', u'sciences', u'thinking', u'environment', u'bush', u'concerns', u'4', u'rules', u'respective', u'communities', u'realize', u'advanced', u'gray', u'evolution', u'facets', u'philosophical', u'establishing', u'human', u'classifying', u'intelligence', u'cyber', u'breakthrough', u'cyber-physical-socio', u'89', u'recommendation', u'images', u'machines', u'principles', u'network', u'space', u'reasoning', u'memex', u'3', u'closed', u'relational', u'scientific', u'nature', u'mechanisms', u'objects', u'web', u'inductive', u'implicit', u'hyperlink', u'study', u'changed', u'personal', u'browsing', u'emerge', u'ability', u'classification', u'linking', u'behaving', u'networking', u'basis', u'support', u'computing', u'question', u'relations', u'live', u'2', u'basic', u'introducing', u'diversity', u'analogical', u'self-organized', u'forming', u'explanation', u'cooperate', u'link', u'cp3sme', u'technologies', u'integrating', u'engineering', u'future', u'next-generation', u'interactive', u'links', u'exploring', u'characteristics', u'loops', u'diverse', u'socio', u'extending', u'develop', u'realizing', u'answering', u'1', u'ideal', u'complex', u'intelligent', u'applications', u'development', u'evolve', u'extended', u'communicating', u'models', u'turing', u'philosophy', u'flows', u'includes', u'lens', u'levels', u'preliminary', u'improving', u'model', u'interacting', u'realized', u'multi-disciplinary', u'lead', u'traditional', u'fundamental', u'controlling', u'sensing', u'laws']
# ComWOnAC:
# [u'limited', u'emerging', u'abilities', u'semantic', u'guided', u'ideas', u'spaces', u'human', u'query', u'algorithms', u'issues', u'previous', u'1', u'multi-dimensional', u'classification', u'physiological', u'explain', u'environment', u'complex', u'4', u'pre-designed', u'resources', u'ideal', u'rules', u'realize', u'advanced', u'gray', u'evolution', u'graph-based', u'facets', u'integrating', u'establishing', u'realistic', u'individuals', u'including', u'mental', u'classifying', u'intelligence', u'humans', u'discover', u'cyber', u'society', u'89', u'recommendation', u'loops', u'multiple', u'extended', u'machines', u'ability', u'network', u'space', u'reasoning', u'memex', u'3', u'closed', u'limitations', u'scientific', u'extend', u'nature', u'mechanisms', u'objects', u'web', u'networking', u'inductive', u'hyperlink', u'study', u'changed', u'thinking', u'browsing', u'multi-disciplinary', u'interact', u'exploring', u'emerge', u'relational', u'solve', u'linking', u'psychological', u'philosophical', u'relations', u'personal', u'establish', u'implicit', u'behaving', u'basis', u'create', u'support', u'question', u'bush', u'live', u'2', u'basic', u'structures', u'introducing', u'diversity', u'analogical', u'form', u'explanation', u'principles', u'link', u'cp3sme', u'technologies', u'breakthrough', u'cyber-physical-socio', u'future', u'learn', u'next-generation', u'model', u'interactive', u'links', u'computing', u'process', u'characteristics', u'mind', u'images', u'engineering', u'diverse', u'socio', u'lifetime', u'linked', u'respective', u'develop', u'self-organized', u'realizing', u'answering', u'expect', u'machine', u'sciences', u'forming', u'physical', u'intelligent', u'applications', u'development', u'evolve', u'communicating', u'models', u'turing', u'philosophy', u'flows', u'includes', u'lens', u'extending', u'levels', u'preliminary', u'improving', u'cooperate', u'data', u'concerns', u'interacting', u'realized', u'lead', u'communities', u'traditional', u'fundamental', u'controlling', u'sensing', u'laws']
# #-------------------------------------------------
# f0014
# OnAbs: 0%
# OnConc: 0%
# OnAC: 0%
# Abs2CE: 0%
# Conc2CE: 0%
# AC2CE: 0%
# WAbs: 0.0%
# WConc: 0.0%
# W2AC: 0.0%
# ComWOnAbs:
# []
# ComWOnConc:
# []
# ComWOnAC:
# []
# #-------------------------------------------------
# f0015
# OnAbs: 0%
# OnConc: 74.2857142857%
# OnAC: 74.2857142857%
# Abs2CE: 0%
# Conc2CE: 22.7272727273%
# AC2CE: 22.7272727273%
# WAbs: 0.0%
# WConc: 66.0377358491%
# W2AC: 66.0377358491%
# ComWOnAbs:
# []
# ComWOnConc:
# [u'program', u'easier', u'fool', u'uderstand', u'designers', u'teller', u'easily', u'automatic', u'pleasanter', u'mental', u'deal', u'humans', u'computer', u'humane', u'machines', u'terms', u'properties', u'computers', u'create', u'apparent', u'ascribe', u'understand', u'careful', u'easiest', u'circumstances', u'future', u'control', u'machine', u'physical', u'ascription', u'users', u'programmers', u'user', u'programs', u'qualities']
# ComWOnAC:
# [u'program', u'easier', u'fool', u'uderstand', u'designers', u'teller', u'easily', u'automatic', u'pleasanter', u'mental', u'deal', u'humans', u'computer', u'humane', u'machines', u'programmers', u'terms', u'properties', u'computers', u'control', u'create', u'apparent', u'ascribe', u'understand', u'careful', u'easiest', u'circumstances', u'future', u'machine', u'physical', u'ascription', u'users', u'user', u'programs', u'qualities']
# #-------------------------------------------------
# f0016
# OnAbs: 58.2125603865%
# OnConc: 0%
# OnAC: 58.2125603865%
# Abs2CE: 55.5555555556%
# Conc2CE: 0%
# AC2CE: 55.5555555556%
# WAbs: 44.1064638783%
# WConc: 0.0%
# W2AC: 44.1064638783%
# ComWOnAbs:
# [u'lack', u'activated', u'reasoning', u'program', u'experimentally', u'idiots', u'non-feeble-minded', u'bacterial', u'bacteria', u'current', u'told', u'interns', u'modify', u'i.e', u'experience', u'action', u'opinion', u'scope', u'successful', u'infection', u'antibiotics', u'keeping', u'practicing', u'originally', u'values', u'learn', u'sense', u'intended', u'treatments', u'brittle', u'symptoms', u'systems', u'physicians', u'diseases', u'matches', u'domain', u'idea', u'performs', u'mycin', u'perform', u'variables', u'doctors', u'representing', u'require', u'programs', u'patients', u'determined', u'illness', u'programmers', u'medical', u'infections', u'knowledge', u'hope', u'meant', u'cholera', u'common', u'set', u'intelligence', u'computer', u'close', u'fails', u'pattern', u'sites', u'artificial', u'progress', u'ability', u'extend', u'usable', u'relevant', u'offers', u'partly', u'physician', u'contemplated', u'suppose', u'smart', u'discoveries', u'manner', u'experts', u'develop', u'doctor', u'consequence', u'difficult', u'hand', u'narrow', u'database', u'possessed', u'true', u'researchers', u'human', u'death', u'treatment', u'match', u'tests', u'designers', u'formal', u'specific', u'misled', u'popular', u'limitations', u'patient', u'ontology', u'ideology', u'absent', u'par', u'ai', u'recognize', u"''", u'formalism', u'hospitals', u'field', u'compares', u'users', u'students', u'includes', u'scores', u'rule']
# ComWOnConc:
# []
# ComWOnAC:
# [u'lack', u'activated', u'reasoning', u'knowledge', u'idiots', u'program', u'hope', u'meant', u'cholera', u'progress', u'experimentally', u'common', u'set', u'intelligence', u'computer', u'non-feeble-minded', u'close', u'bacterial', u'bacteria', u'pattern', u'sites', u'artificial', u'current', u'told', u'ability', u'extend', u'interns', u'modify', u'i.e', u'experience', u'discoveries', u'action', u'opinion', u'relevant', u'treatment', u'ontology', u'offers', u'scope', u'field', u'partly', u'successful', u'infection', u'antibiotics', u'keeping', u'practicing', u'contemplated', u'originally', u'values', u'learn', u'manner', u'usable', u'experts', u'sense', u'specific', u'develop', u'doctor', u'hospitals', u'consequence', u'difficult', u'intended', u'includes', u'suppose', u'treatments', u'narrow', u'programs', u'possessed', u'perform', u'researchers', u'true', u'human', u'brittle', u'death', u'symptoms', u'systems', u'smart', u'physicians', u'diseases', u'matches', u'designers', u'misled', u'popular', u'domain', u'idea', u'physician', u'students', u'tests', u'performs', u'limitations', u'patient', u'mycin', u'hand', u'ideology', u'variables', u'recognize', u'doctors', u'representing', u'absent', u'require', u'database', u'par', u'patients', u'determined', u'illness', u'ai', u"''", u'formalism', u'match', u'compares', u'users', u'programmers', u'fails', u'scores', u'formal', u'medical', u'infections', u'rule']
# #-------------------------------------------------
# f0027
# OnAbs: 38.8888888889%
# OnConc: 0%
# OnAC: 38.8888888889%
# Abs2CE: 10.5919003115%
# Conc2CE: 0%
# AC2CE: 10.5919003115%
# WAbs: 38.8888888889%
# WConc: 0.0%
# W2AC: 38.8888888889%
# ComWOnAbs:
# [u'notebooks', u'paper', u'scientific', u'analyse', u'data', u'amount', u'databases']
# ComWOnConc:
# []
# ComWOnAC:
# [u'databases', u'analyse', u'paper', u'data', u'scientific', u'notebooks', u'amount']
# #-------------------------------------------------
# f0028
# OnAbs: 0%
# OnConc: 74.0384615385%
# OnAC: 74.0384615385%
# Abs2CE: 0%
# Conc2CE: 41.5701415701%
# AC2CE: 41.5701415701%
# WAbs: 0.0%
# WConc: 63.2352941176%
# W2AC: 63.2352941176%
# ComWOnAbs:
# []
# ComWOnConc:
# [u'emerging', u'code', u'bandwidth', u'netcdf', u'file', u'centers', u'previous', u'visualization', u'languages', u'systems', u'easy', u'extensive', u'advances', u'questions', u'indexing', u'focus', u'community', u'performance', u'unifying', u'automatic', u'essential', u'disciplines', u'people', u'trend', u'visualize', u'describing', u'pace', u'analyze', u'access', u'3', u'scientists', u'metadata', u'terms', u'scientific', u'answers', u'standard', u'peta-scale', u'focused', u'central', u'programming', u'computational', u'instruments', u'analyzing', u'tools', u'interchange', u'management', u'system', u'2', u'archives', u'vehicle', u'non-procedural', u'separated', u'sharing', u'serve', u'understand', u'keeping', u'datasets', u'science', u'database', u'hdf', u'embed', u'synthesis', u'enable', u'archive', u'huge', u'algorithms', u'1', u'emphasis', u'resources', u'set-oriented', u'io', u'object', u'collection', u'extending', u'moving', u'sql', u'fits', u'data', u'types', u'programs', u'analysis', u'traditional', u'provide', u'parallelism', u'databases', u'link']
# ComWOnAC:
# [u'emerging', u'code', u'bandwidth', u'netcdf', u'questions', u'centers', u'previous', u'visualization', u'languages', u'systems', u'easy', u'extensive', u'advances', u'indexing', u'focus', u'datasets', u'metadata', u'automatic', u'essential', u'disciplines', u'people', u'trend', u'visualize', u'describing', u'hdf', u'access', u'3', u'scientists', u'unifying', u'terms', u'scientific', u'answers', u'standard', u'focused', u'central', u'programming', u'computational', u'instruments', u'community', u'analyzing', u'tools', u'interchange', u'management', u'peta-scale', u'data', u'system', u'2', u'archives', u'vehicle', u'analyze', u'non-procedural', u'separated', u'sharing', u'serve', u'understand', u'keeping', u'science', u'programs', u'pace', u'embed', u'synthesis', u'enable', u'file', u'huge', u'archive', u'1', u'emphasis', u'performance', u'resources', u'parallelism', u'io', u'object', u'collection', u'extending', u'moving', u'sql', u'fits', u'types', u'database', u'analysis', u'traditional', u'provide', u'algorithms', u'set-oriented', u'databases', u'link']
# #-------------------------------------------------
# f0029
# OnAbs: 50.0%
# OnConc: 43.8202247191%
# OnAC: 46.9945355191%
# Abs2CE: 26.7573696145%
# Conc2CE: 27.8911564626%
# AC2CE: 33.3333333333%
# WAbs: 42.8571428571%
# WConc: 38.6666666667%
# W2AC: 37.7358490566%
# ComWOnAbs:
# [u'ephemeral', u'observational', u'sky', u'cross-match', u'match', u'stationary', u'library', u'measurements', u'misses', u'masked', u'missing', u'step', u'objects', u'hits', u'classification', u'simply', u'table', u'statistics', u'instrument', u'bundles', u'observations', u'overlapping', u'moved', u'compared', u'field', u'spatial', u'object', u'bundle', u'variable', u'edge']
# ComWOnConc:
# [u'threshold', u'observational', u'cross-match', u'match', u'matches', u'runs', u'library', u'detection', u'misses', u'masked', u'sdss', u'missing', u'step', u'bundle', u'hits', u'region', u'classification', u'table', u'bundles', u'observations', u'figure', u'moved', u'ephemeral', u'astronomers', u'5', u'spatial', u'multiple', u'object', u'edge']
# ComWOnAC:
# [u'threshold', u'runs', u'detection', u'missing', u'objects', u'hits', u'region', u'classification', u'simply', u'table', u'bundles', u'figure', u'astronomers', u'edge', u'ephemeral', u'observational', u'sky', u'instrument', u'cross-match', u'match', u'matches', u'spatial', u'stationary', u'library', u'measurements', u'misses', u'masked', u'sdss', u'step', u'statistics', u'observations', u'overlapping', u'moved', u'compared', u'field', u'5', u'multiple', u'object', u'bundle', u'variable']
# #-------------------------------------------------