# -*- coding: UTF-8 -*- 

#######################################################################################
#--------------------------------- Function Introduce --------------------------------#
#######################################################################################
# This functions set intends to:
# 1. read the accdb files
# 2. Get the words set of Abstract and Conclusion
# 3. compare the words used in the CE_relation cases and the words used in Abstract and Conclusion

#######################################################################################
#--------------------------------- Function Results ----------------------------------#
#######################################################################################
# f0001
# OnAbs: 84.1666666667%
# OnConc: 69.8412698413%
# OnAC: 76.8292682927%
# Abs2CE: 28.8507391512%
# Conc2CE: 22.8898426323%
# AC2CE: 35.0023843586%
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
# OnConc: 87.2340425532%
# OnAC: 86.387434555%
# Abs2CE: 32.3000898473%
# Conc2CE: 36.1185983827%
# AC2CE: 43.7556154537%
# WAbs: 78.5714285714%
# WConc: 82.8767123288%
# W2AC: 78.2828282828%
# ComWOnAbs: 
# [u'limited', u'abilities', u'semantic', u'spaces', u'human', u'issues', u'previous', u'machine', u'physiological', u'explain', u'environment', u'pre-designed', u'resources', u'rules', u'graph-based', u'realistic', u'individuals', u'including', u'mental', u'intelligence', u'humans', u'discover', u'cyber', u'society', u'loops', u'machines', u'scientific', u'principles', u'space', u'closed', u'limitations', u'ability', u'extend', u'mechanisms', u'multi-disciplinary', u'create', u'emerge', u'linking', u'psychological', u'philosophical', u'establish', u'interact', u'live', u'2', u'structures', u'form', u'explanation', u'cooperate', u'link', u'cp3sme', u'cyber-physical-socio', u'learn', u'expect', u'links', u'computing', u'process', u'characteristics', u'mind', u'images', u'diverse', u'socio', u'lifetime', u'linked', u'ideas', u'1', u'ideal', u'complex', u'solve', u'physical', u'evolve', u'multiple', u'models', u'includes', u'data', u'algorithms', u'fundamental', u'laws']
# ComWOnConc: 
# [u'limited', u'emerging', u'semantic', u'guided', u'spaces', u'query', u'issues', u'machine', u'multi-dimensional', u'sciences', u'thinking', u'environment', u'bush', u'concerns', u'4', u'rules', u'respective', u'communities', u'realize', u'advanced', u'evolution', u'facets', u'philosophical', u'establishing', u'human', u'classifying', u'intelligence', u'cyber', u'breakthrough', u'cyber-physical-socio', u'89', u'recommendation', u'images', u'machines', u'principles', u'network', u'space', u'reasoning', u'memex', u'3', u'closed', u'relational', u'scientific', u'nature', u'mechanisms', u'objects', u'web', u'inductive', u'implicit', u'hyperlink', u'study', u'changed', u'personal', u'browsing', u'emerge', u'ability', u'classification', u'linking', u'behaving', u'networking', u'basis', u'support', u'computing', u'question', u'relations', u'live', u'2', u'basic', u'introducing', u'diversity', u'analogical', u'self-organized', u'forming', u'explanation', u'cooperate', u'link', u'cp3sme', u'technologies', u'integrating', u'engineering', u'future', u'next-generation', u'interactive', u'links', u'exploring', u'characteristics', u'loops', u'diverse', u'socio', u'extending', u'develop', u'realizing', u'answering', u'1', u'ideal', u'complex', u'intelligent', u'applications', u'development', u'evolve', u'extended', u'communicating', u'models', u'turing', u'philosophy', u'flows', u'includes', u'lens', u'levels', u'preliminary', u'improving', u'model', u'interacting', u'realized', u'multi-disciplinary', u'lead', u'traditional', u'fundamental', u'controlling', u'sensing', u'laws']
# ComWOnAC: 
# [u'limited', u'emerging', u'abilities', u'semantic', u'guided', u'ideas', u'spaces', u'human', u'query', u'algorithms', u'issues', u'previous', u'1', u'multi-dimensional', u'classification', u'physiological', u'explain', u'environment', u'complex', u'4', u'pre-designed', u'resources', u'ideal', u'rules', u'realize', u'advanced', u'evolution', u'graph-based', u'facets', u'integrating', u'establishing', u'realistic', u'individuals', u'including', u'mental', u'classifying', u'intelligence', u'humans', u'discover', u'cyber', u'society', u'89', u'recommendation', u'loops', u'multiple', u'extended', u'machines', u'ability', u'network', u'space', u'reasoning', u'memex', u'3', u'closed', u'limitations', u'scientific', u'extend', u'nature', u'mechanisms', u'objects', u'web', u'networking', u'inductive', u'hyperlink', u'study', u'changed', u'thinking', u'browsing', u'multi-disciplinary', u'interact', u'exploring', u'emerge', u'relational', u'solve', u'linking', u'psychological', u'philosophical', u'relations', u'personal', u'establish', u'implicit', u'behaving', u'basis', u'create', u'support', u'question', u'bush', u'live', u'2', u'basic', u'structures', u'introducing', u'diversity', u'analogical', u'form', u'explanation', u'principles', u'link', u'cp3sme', u'technologies', u'breakthrough', u'cyber-physical-socio', u'future', u'learn', u'next-generation', u'model', u'interactive', u'links', u'computing', u'process', u'characteristics', u'mind', u'images', u'engineering', u'diverse', u'socio', u'lifetime', u'linked', u'respective', u'develop', u'self-organized', u'realizing', u'answering', u'expect', u'machine', u'sciences', u'forming', u'physical', u'intelligent', u'applications', u'development', u'evolve', u'communicating', u'models', u'turing', u'philosophy', u'flows', u'includes', u'lens', u'extending', u'levels', u'preliminary', u'improving', u'cooperate', u'data', u'concerns', u'interacting', u'realized', u'lead', u'communities', u'traditional', u'fundamental', u'controlling', u'sensing', u'laws']
# #-------------------------------------------------

#######################################################################################
#---------------------------------- Global variable ----------------------------------#
#######################################################################################
from cmyToolkit import *
import os
import nltk
import re
import pyodbc
#--------- set some folder path ------------------
corpdir = os.path.join(os.getcwd(),"Corpus")
pkdir = os.path.join(os.getcwd(),"PK")
TXTcorpdir = os.path.join(os.getcwd(),"Corpus","TXT")
TXTpkdir = os.path.join(os.getcwd(),"PK","TXT")
DICpkdir = os.path.join(os.getcwd(),"PK","DIC")
ctxtdir = os.path.join(os.getcwd(),"CheckTXT")
xlsdir = os.path.join(os.getcwd(),'XLS')
dbfile = os.path.join(os.getcwd(),'CErelation.accdb')

#######################################################################################
#-------------------------------------- Classes --------------------------------------#
#######################################################################################
class FText:
    def __init__(self,ftag,abs_text,conc_text,ce_text):
        self.Ftag = ftag
        self.AbsText = abs_text
        self.ConcText = conc_text
        self.CEText = ce_text
        self.CE_A_Text = [] 
        self.CE_B_Text = []
        
class FWordDic:
    def __init__(self,ftag,absworddic,concworddic,acworddic,ceworddic):
        self.Ftag = ftag
        self.AbsWordDic = absworddic
        self.ConcWordDic = concworddic
        self.A_CWordDic = acworddic
        self.CEWordDic = ceworddic

class CoWords:
    def __init__(self,FWDic,OnAbs,Abs2CE,OnConc,Conc2CE,OnAC,AC2CE,wAbs,wConc,wAC,comwonabs,comwonconc,comwonac):
        self.FWDic = FWDic
        self.OnAbs = OnAbs
        self.OnConc = OnConc
        self.OnAC = OnAC
        self.Abs2CE = Abs2CE
        self.Conc2CE = Conc2CE
        self.AC2CE = AC2CE
        self.WAbs = wAbs
        self.WConc = wConc
        self.WAC = wAC
        self.ComWOnAbs = comwonabs
        self.ComWOnConc = comwonconc
        self.ComWOnAC = comwonac

#######################################################################################
#----------------------------------- Check Patterns ----------------------------------#
#######################################################################################        
def Check_C_P_S(text):
    pieces = text.split('. ')
    TypeSheet = []
    for p in pieces:
        if re.match("^[\s]*$",p): continue #if p is a empty string
        elif re.match("[C|P|S][\d]+$", p):
            if p[0] == 'S':   type = 0
            elif p[0] == 'P': type = 1
            else:             type = 2
            TypeSheet.append([type,int(p[1:])])
        else:
            TypeSheet.append([-1,p])
        
    return TypeSheet


#######################################################################################
#--------------------------------- Read Database file --------------------------------#
#######################################################################################
def ReadDB_Ftaglist():
    #----------- Connect Database --------------
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + dbfile + ";Uid=;Pwd=;")
    cursor = conn.cursor()
    #-------------------------------------------
    FtagSQL = "SELECT Ftag from FileInfo;"
    FtagList = [];
    for row in cursor.execute(FtagSQL):
        FtagList.append(row.Ftag)
    
    cursor.close()
    conn.close()
    
    return FtagList

def ReadDB_AbsText(ftag):
    #----------- Connect Database --------------
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + dbfile + ";Uid=;Pwd=;")
    cursor = conn.cursor()
    #-------------------------------------------
    AbsText = []
    AbsSQL = "SELECT text from Sent where Ftag = \'"+ftag+"\' and Ctag = 0"
    for row in cursor.execute(AbsSQL):
        AbsText.append(row.text)
        
    cursor.close()
    conn.close()
    
    return AbsText

def ReadDB_ConcText(ftag):
    #----------- Connect Database --------------
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + dbfile + ";Uid=;Pwd=;")
    cursor = conn.cursor()
    #-------------------------------------------
    ConcCtagSQL = "SELECT Ctag from SecInfo where Ftag = \'" +ftag+"\' and Ctitle in ('Conclusion','conclusion','summary','Summary')"
    ConcCtag = ((cursor.execute(ConcCtagSQL)).fetchone()).Ctag
    ConcSQL = "SELECT text from Sent where Ftag = \'"+ftag+"\' and Ctag ="+str(ConcCtag)
    ConcText = []
    
    for row in cursor.execute(ConcSQL):
        ConcText.append(row.text)
        
    cursor.close()
    conn.close()
    
    return ConcText

def ReadDB_CEText(ftag):
    #----------- Connect Database --------------
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + dbfile + ";Uid=;Pwd=;")
    cursor = conn.cursor()
    #-------------------------------------------
    Type = ['Stag','Ptag','Ctag']
    CESQL = "SELECT ID, Context, A, B from CE_Relation where Ftag = \'"+ftag+"\' order by ID"
    CE_A_Text = []
    CE_B_Text = []
      
    for row in cursor.execute(CESQL):
        ATypeList = Check_C_P_S(row.A)
        BTypeList = Check_C_P_S(row.B)
        AText = [];
        BText = [];
                
        for a in ATypeList:
            if a[0] == -1:
                AText.append(a[1])
            else:
                tempcursor = conn.cursor()
                tempSQL = "SELECT Stag, text from Sent where Ftag = \'"+ftag+"\' and "+Type[a[0]]+" = "+str(a[1])+" order by Stag"
                for row1 in tempcursor.execute(tempSQL):
                    AText.append(row1.text)
                tempcursor.close()   
        
        for b in BTypeList:
            if b[0] == -1:
                BText.append(b[1])
            else:
                tempcursor = conn.cursor()
                tempSQL = "SELECT Stag, text from Sent where Ftag = \'"+ftag+"\' and "+Type[b[0]]+" = "+str(b[1])+" order by Stag"
                for row1 in tempcursor.execute(tempSQL):
                    BText.append(row1.text)
                tempcursor.close()

        CE_A_Text.append(AText)
        CE_B_Text.append(BText)        
    
    cursor.close()
    conn.close()
    return [CE_A_Text,CE_B_Text];


#######################################################################################
#--------------------------- Calculate Word Frequency --------------------------------#
#######################################################################################
###---- remove pairs in 'Dic' if their keys in 'Removelist' ---- 
def DicRemove(Dic,Removelist):
    for r in Removelist:
        if Dic.has_key(r): del Dic[r]
    return Dic

###---- count the words in text and update values in 'Dic' ----
def Text2WordDic(Dic,text):
    tokens = nltk.word_tokenize(text)
    for t in tokens:
        t = t.lower()
        if not Dic.has_key(t):
            Dic[t] = 1
        else:
            Dic[t] += 1
    return Dic

###---- Create FWordDic(f,AbsWordDic,ConcWordDic,A_CWordDic,CEWordDic) for each file in data base file----
def GetWordDic(): 
    Ftag = ReadDB_Ftaglist()
    FWord = []
    FTextList = []
    #--------- Get SentSet & CE relation cases for each files---------
    for f in Ftag:
        # ****** Get Abstract Words Dictionary ******  
        AbsText = ReadDB_AbsText(f)
        AbsWordDic = {}
        for text in AbsText:
            AbsWordDic = Text2WordDic(AbsWordDic,text)
        # ****** Get Conclusion Words Dictionary ******
        ConcText = ReadDB_ConcText(f)
        ConcWordDic = {}        
        for text in ConcText:
            ConcWordDic = Text2WordDic(ConcWordDic, text)
        # ****** Get CE relation cases Words Dictionary ******
        CE_A_Text,CE_B_Text = ReadDB_CEText(f)
        CE_Text = [];
        CEWordDic = {}
        
        for idx,A in enumerate(CE_A_Text):
            B = CE_B_Text[idx];
            for atext in A: 
                CE_Text.append(atext);
            for btext in B:
                CE_Text.append(btext);

        for text in CE_Text:
            CEWordDic = Text2WordDic(CEWordDic, text)

        # ****** Get the Abstract & Conclusion union word dict ******
        A_CWordDic = AbsWordDic.copy()
        for k,v in ConcWordDic.items():
            if A_CWordDic.has_key(k):
                A_CWordDic[k] = A_CWordDic[k]+v
            else:
                A_CWordDic[k] = v
        tempFText = FText(f,AbsText,ConcText,CE_Text);
        tempFText.CE_A_Text = CE_A_Text;
        tempFText.CE_B_Text = CE_B_Text;        
        FTextList.append(tempFText);        
        FWord.append(FWordDic(f,AbsWordDic,ConcWordDic,A_CWordDic,CEWordDic))
    
    Dumppickle(os.path.join(DICpkdir,"FTextList.pk"), FTextList)
    Dumppickle(os.path.join(DICpkdir,"FWordDic.pk"), FWord)
    
    return FWord

#######################################################################################
#--------------- Calculate percent of common words in CE and Abs&Conc ----------------#
#######################################################################################
def GetCE_AC_CoWordsPercent(FWord):
    #----------- Get stop words, Punctions------------
    StopW = Loadpickle(os.path.join(pkdir,'StopW.pk'))
    Puncs = Loadpickle(os.path.join(pkdir,'Puncs.pk'))
    #------------Calculate Words Similarity -----------
    FCoWord = []
    Removelist = Puncs + StopW;
    for f in FWord:
        # remove Punctions and StopWords from WordDics
        f.AbsWordDic = DicRemove(f.AbsWordDic, Removelist);
        f.ConcWordDic = DicRemove(f.ConcWordDic, Removelist);
        f.A_CWordDic = DicRemove(f.A_CWordDic, Removelist);
        f.CEWordDic = DicRemove(f.CEWordDic, Removelist);
        # calculate each word's rate in each Dict
        SumAWords = float(sum(f.AbsWordDic.values()));
        SumCWords = float(sum(f.ConcWordDic.values()));
        SumACWords = float(sum(f.A_CWordDic.values()));
        SumCEWords = float(sum(f.CEWordDic.values()));
        for a,av in f.AbsWordDic.items():
            f.AbsWordDic[a] =  av/SumAWords
        for c,cv in f.ConcWordDic.items():
            f.ConcWordDic[c] = cv/SumCWords
        for ac,acv in f.A_CWordDic.items():
            f.A_CWordDic[ac] = acv/SumACWords
        for ce,cev in f.CEWordDic.items():
            f.CEWordDic[ce] = cev/SumCEWords
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
        for a,av in f.AbsWordDic.items():
            if f.CEWordDic.has_key(a):
                OnAbs += av
                Abs2CE += f.CEWordDic[a]
                ComWOnAbs.append(a)
        for c,cv in f.ConcWordDic.items():
            if f.CEWordDic.has_key(c):
                OnConc += cv
                Conc2CE += f.CEWordDic[c]
                ComWOnConc.append(c)
        for ac,acv in f.A_CWordDic.items():
            if f.CEWordDic.has_key(ac):
                OnAC += acv
                AC2CE += f.CEWordDic[ac]
                ComWOnAC.append(ac)
        
        wAbs = 0.0 if len(f.AbsWordDic) ==0 else float(len(ComWOnAbs))/len(f.AbsWordDic);
        wConc = 0.0 if len(f.AbsWordDic) ==0 else float(len(ComWOnConc))/len(f.ConcWordDic); 
        wAC = 0.0 if len(f.A_CWordDic) ==0 else float(len(ComWOnAC))/len(f.A_CWordDic);
        
        FCoWord.append(CoWords(f,OnAbs,Abs2CE,OnConc,Conc2CE,OnAC,AC2CE,wAbs,wConc,wAC,ComWOnAbs,ComWOnConc,ComWOnAC))
    
    Dumppickle(os.path.join(DICpkdir,"FCoWord.pk"), FCoWord)
    return FCoWord

#######################################################################################
#--------------------------- Some demonstration functions ----------------------------#
#######################################################################################
def showFText(FTextList):
    for ftext in FTextList:
        print "Current file:", ftext.Ftag;
        print "Abstract Text:"
        for abs in ftext.AbsText:
            print "\t",abs;
        print "Conclusion Text:"
        for conc in ftext.ConcText:
            print "\t",conc;
        print "CE cases Text:"
        for ce in ftext.CEText:
            print "\t",ce;    
        print "#-------------------------------------------------\n";

def showCoWordPercent(FCoWord):
    for f in FCoWord:
        print (f.FWDic).Ftag
        #print sorted((f.FWDic).CEWordDic.iteritems(),key = lambda asd:asd[1], reverse = True)
        print "OnAbs: " + str(f.OnAbs*100) +"%" 
        print "OnConc: " + str(f.OnConc*100) + "%"
        print "OnAC: " + str(f.OnAC*100) + "%"
        print "Abs2CE: " + str(f.Abs2CE*100) + "%"
        print "Conc2CE: " + str(f.Conc2CE*100) + "%"
        print "AC2CE: " + str(f.AC2CE*100) + "%"
        print "WAbs: " + str(f.WAbs*100) + "%"
        print "WConc: " + str(f.WConc*100) + "%"
        print "W2AC: " + str(f.WAC*100) + "%"
        print "ComWOnAbs: " 
        print f.ComWOnAbs
        print "ComWOnConc: " 
        print f.ComWOnConc
        print "ComWOnAC: " 
        print f.ComWOnAC
        print "#-------------------------------------------------"

def CoWord_PK2TXT(CoWordfp,FCoWord):
    CoWordTXT = codecs.open(CoWordfp,'w','utf8')
    
    for f in FCoWord:
        CoWordTXT.write((f.FWDic).Ftag + "\n");
        CoWordTXT.write("OnAbs: %.4f" %(f.OnAbs*100) +"%\n");
        CoWordTXT.write("OnConc: %.4f" %(f.OnConc*100) + "%\n");
        CoWordTXT.write("OnAC: %.4f" %(f.OnAC*100) + "%\n");
        CoWordTXT.write("Abs2CE: %.4f" %(f.Abs2CE*100) + "%\n");
        CoWordTXT.write("Conc2CE: %.4f" %(f.Conc2CE*100) + "%\n");
        CoWordTXT.write("AC2CE: %.4f" %(f.AC2CE*100) + "%\n");
        CoWordTXT.write("WAbs: %.4f" %(f.WAbs*100) + "%\n");
        CoWordTXT.write("WConc: %.4f" %(f.WConc*100) + "%\n");
        CoWordTXT.write("WAC: %.4f" %(f.WAC*100) + "%\n");
        CoWordTXT.write("ComWOnAbs: \n");
        CoWordTXT.write(str(f.ComWOnAbs) + "\n")
        CoWordTXT.write("ComWOnConc:  \n");
        CoWordTXT.write(str(f.ComWOnConc) + "\n")
        CoWordTXT.write("ComWOnAC:  \n" );
        CoWordTXT.write(str(f.ComWOnAC)+ "\n")
        CoWordTXT.write("#-------------------------------------------------\n\n\n");

#######################################################################################
#---------------------------------- Main function ------------------------------------#
#######################################################################################       
if __name__ == "__main__": 
    FCoWord = GetCE_AC_CoWordsPercent(GetWordDic())
    showCoWordPercent(FCoWord)
    CoWordfp = os.path.join(ctxtdir,'CE_AC_CoWordsPercent.txt');
    CoWord_PK2TXT(CoWordfp,FCoWord);