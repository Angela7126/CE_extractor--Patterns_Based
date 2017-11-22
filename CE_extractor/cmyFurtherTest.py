# -*- coding: UTF-8 -*- 

#######################################################################################
# --------------------------------- Function Introduce ------------------------------ #
#######################################################################################
# This functions set intends to:
# Statistic the cause-effect links extracted by 'cmyPatternMatching' function sets.
# 1. Get the cause-effect link sets storing in ./PK/DIC/CEList.py, which is a 2D list:
#    (1) each element of CElist is a 'CElink' object list for according file;
#    (2) The definition of 'CElink' class please see cmyPatternMatching.py;
# 2. Get the 'Paper' object list storing in ./PK/DIC/PaperList.py, which is a 1D list:
#    (1) each element of PaperList is a Paper object for a file in corpus;
#    (2) The definition of 'Paper' class please see cmyPreprocess.py; 
# 3. Count the distribution of CE cases on each section for each file:
#    (1) the name of each section;
#    (2) the number of sentences in each section;
#    (3) the number of CE cases in each section extracted by function 'CElinksForCorpus' in 'cmyPatternMatching.py';
#    (4) the number of sentences that covered by CE cases in each section;
#    (5) the Sentence cover rate in each section;
# 4. Calculate the percent of common words:
#    (1) Build 'FWordDic' object for each file in corpus, please see 'cmyWordsCompare.py' for details;
#    (2) Build 'CoWords' object for each file in corpus, please see 'cmyWordsCompare.py' for details;

#######################################################################################
# ---------------------------------- Global variable -------------------------------- #
#######################################################################################
import os
import re
import sys
import nltk
import string
import operator
from nltk.tree import *
from cmyPackage import *
from cmyWordsCompare import *

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
# --------------------------- Some demonstration functions -------------------------- #
#######################################################################################
def CESecDistribution2TXT(Recfp, PaperTestList):
    RecordFile = codecs.open(Recfp, 'w', 'utf8')
    for papertest in PaperTestList:
        RecordFile.write("Current File: " + papertest.Paperinfo.Ftag + " " + papertest.Paperinfo.Ftitle + "\n\n")
        for CESec in papertest.CESeclst:
            RecordFile.write("Section %d: " % CESec.Ctag + CESec.Ctitle + "\n")
            RecordFile.write("\tSentNum: %d" % len(CESec.Slist) + "\n")
            RecordFile.write("\tCENum: %d" % len(CESec.CElist) + "\n")
            RecordFile.write("\tSentCovered: %d" % len(CESec.CEsent) + "\n")
            RecordFile.write("\tCovered_Rate: %.4f" % (
                float(len(CESec.CEsent)) * 100 / len(CESec.Slist) if len(CESec.Slist) > 0 else 0) + "%\n\n")
        RecordFile.write("#-------------------------------------------------\n\n")

    RecordFile.write("####################### CE links on each Section #########################\n\n")
    for papertest in PaperTestList:
        RecordFile.write(papertest.Paperinfo.Ftag + "'s CE cases\n\n")
        for CESec in papertest.CESeclst:
            RecordFile.write("Section %d: " % CESec.Ctag + CESec.Ctitle + " has %d CE cases\n" % len(CESec.CElist))
            for idx, ce in enumerate(CESec.CElist):
                RecordFile.write("\tCASE: %d\n" % (idx + 1))
                RecordFile.write("\tStag: ")
                for ceSentInfo in ce.sInfo:
                    RecordFile.write("%d " % ceSentInfo.Stag)
                RecordFile.write("\n")
                RecordFile.write(
                    "\t\tPattern: " + '%d' % ce.pt.pfreq + ' %s' % ce.pt.main_token + "----" + ' %s' % ce.pt.constraints + '\n')
                RecordFile.write("\t\tsentTXT: ")
                for PT in ce.PTreelst:
                    RecordFile.write(' '.join(PT.leaves()) + ' ')
                RecordFile.write("\n")
                RecordFile.write("\t\tCause: " + ' '.join(ce.cause.PTree.leaves()) + '\n')
                RecordFile.write("\t\tEffect: " + ' '.join(ce.effect.PTree.leaves()) + '\n\n')
        RecordFile.write("#-------------------------------------------------\n\n")

def CESecDistribution2Xls(Recfp, PaperTestList):
    oldWB = xlrd.open_workbook(Recfp, formatting_info=True)
    WB = copy(oldWB)
    for i, f in enumerate(PaperTestList):
        WS = WB.add_sheet(f.Paperinfo.Ftag + "_SysCEonSec", cell_overwrite_ok='True')
        TitleRow = ['Section ID', 'Section Title', 'SentNum', 'CENum', 'SentCovered', 'Covered_Rate(%)']
        for j in range(len(TitleRow)):
            WS.write(0, j, TitleRow[j], xlwt.easyxf('font: bold on'))
        for j, CESec in enumerate(f.CESeclst):
            WS.write(j + 1, 0, "%d" % CESec.Ctag)
            WS.write(j + 1, 1, CESec.Ctitle.decode('utf-8'))
            WS.write(j + 1, 2, "%d" % len(CESec.Slist))
            WS.write(j + 1, 3, "%d" % len(CESec.CElist))
            WS.write(j + 1, 4, "%d" % len(CESec.CEsent))
            WS.write(j + 1, 5, " %.4f" % (float(len(CESec.CEsent)) * 100 / len(CESec.Slist) if len(CESec.Slist) > 0 else 0))
    WB.save(Recfp)

#######################################################################################
# ---------------------- Statistic for each paper in corpus ------------------------- #
#######################################################################################

def GetPaperTest():
    PaperList = Loadpickle(os.path.join(DICpkdir, "KGPaperList.pk"))
    CEList = Loadpickle(os.path.join(DICpkdir, "KGCEList.pk"))
    PaperTestList = []
    ConcRegExp = re.compile(ur'(?:conclusion|summary)',
                            re.I)  # Regular Expression using to check whether a section is the 'conclusion'

    for i in range(len(PaperList)):
        curf = PaperList[i]  # current file's 'Paper' object;
        curCEset = CEList[i]  # current file's CEcases sets extracted by 'CElinksForCorpus()'
        curpapertest = PaperTest(curf)  # current file's 'PaperTest()' object;
        curSlist = curf.S_list  # current file's sent list;
        SentVisit = [False] * len(curSlist)  # SentVisit is used to avoid re-add a sent into 'CEonSec' object's CEsent list;

        print "Current File:", curf.Ftag

        ### ---- Build CEonSec object list for each sections for current file ----  
        ### step 1: Initialization current file's CEonSec list with each Section's Ctag and Ctitle.
        ###         and sort the CEonSec list by its elements' Ctag value in ascending order.
        curCESecList = [CEonSec(0, 'Abstract')]
        for c in curf.C_list:
            curCESecList.append(CEonSec(c.Ctag, c.Ctitle))
        curCESecList.sort(key=operator.attrgetter('Ctag'))
        ### step 2: fill each CEonSec object's sent list.
        for s in curSlist:
            try:
                curCESecList[s.Ctag].Slist.append(s)
            except IndexError:
                print s.Ctag, type(s.Ctag), s.Stag, s.text
                sys.exit()
        ### step 3: fill each CEonSec object's CE list and CEsent list (the sent set construct its CE list);
        ###     Notice that we suppose there is no CE case skip two adjacent sections.
        ###     So, we use the CE case's first sent's Sec_id as the CE case's Sec_id.
        for ce in curCEset:
            if len(ce.sInfo) > 0:  # if the CE case has no sent information, skip it;
                cid = ce.sInfo[0].Ctag
                curCESecList[cid].CElist.append(ce)
                for ces in ce.sInfo:
                    if not SentVisit[ces.Stag]:
                        SentVisit[ces.Stag] = True
                        curCESecList[cid].CEsent.append(ces)
        ### step 4: sort the Slist and CEsent list for each CEonSec object by their 'Stag' value in ascending order
        for j in range(len(curCESecList)):
            curCESecList[j].Slist.sort(key=operator.attrgetter('Stag'))
            curCESecList[j].CEsent.sort(key=operator.attrgetter('Stag'))
        ### step 5: added current file's CEonSec object list into its PaperTest object
        curpapertest.CESeclst = curCESecList

        ### ---- Build 'FWordDic' object as current file's CE_AC Word Dictionary -- CE_AC_WDic ----
        ### step 1: get current file's Abstract text and Conclusion text and CEtext
        # Abstract sentences text list
        AbsText = []
        for abs in curCESecList[0].Slist:
            AbsText.append(abs.text)
        # Conclusion sentences text list
        ConcText = []
        if ConcRegExp.match(curCESecList[-1].Ctitle):
            for conc in curCESecList[-1].Slist:
                ConcText.append(conc.text)
        # CE cases sentences text list
        CEText = []
        for ce in curCEset:
            for ces in ce.sInfo:
                CEText.append(ces.text)
        # Build FText object and append it into FTextList
        curpapertest.ftext = FText(curf.Ftag, AbsText, ConcText, CEText)
        ### step 2: build AbsWordDic, ConcWordDic, A_CWordDic, CEWordDic for current file ----
        # Abstract Word Dictionary
        AbsWordDic = {}
        for text in AbsText:
            AbsWordDic = Text2WordDic(AbsWordDic, text)
        # Conclusion Word Dictionary
        ConcWordDic = {}
        for text in ConcText:
            ConcWordDic = Text2WordDic(ConcWordDic, text)
        # CE cases Word Dictionary
        CEWordDic = {}
        for text in CEText:
            CEWordDic = Text2WordDic(CEWordDic, text)
        # Abstract & Conclusion union Word Dictionary
        A_CWordDic = AbsWordDic.copy()
        for k, v in ConcWordDic.items():
            if A_CWordDic.has_key(k):
                A_CWordDic[k] = A_CWordDic[k] + v
            else:
                A_CWordDic[k] = v
        ### step 3: build FWordDic object and add it into current file's PaperTest object as its CE_AC_WDic
        curpapertest.CE_AC_WDic = FWordDic(curf.Ftag, AbsWordDic, ConcWordDic, A_CWordDic, CEWordDic)

        ### ---- Build 'CoWords' object as current file's CE_AC Common Word ratio -- CE_AC_CoWord ----
        curpapertest.CE_AC_CoWord = GetCE_AC_CoWordsPercent([curpapertest.CE_AC_WDic])[0]

        ### ---- Append current file's PaperTest object into PaperTest list ----
        PaperTestList.append(curpapertest)

    ### ---- Save lists into pickle files ----
    Dumppickle(os.path.join(DICpkdir, "KGPaperTextList_FurtherTest.pk"), PaperTestList)
    return PaperTestList


#######################################################################################
# ---------------------------------- Main function ---------------------------------- #
#######################################################################################       
if __name__ == "__main__":
    # PaperTestList = GetPaperTest()
    # Dumppickle(os.path.join(DICpkdir, "KGPaperTextList_FurtherTest.pk"), PaperTestList)
    PaperTestList = Loadpickle(os.path.join(DICpkdir, "KGPaperTextList_FurtherTest.pk"))
    # Recfp = os.path.join(ctxtdir, 'CESec_Distribution_LargeCorpus.txt')
    # CESecDistribution2TXT(Recfp, PaperTestList)
    # FCoWord = []
    # for papertest in PaperTestList:
    #     FCoWord.append(papertest.CE_AC_CoWord)
    # CoWordfp = os.path.join(ctxtdir, 'CE_AC_CoWordsPercent_LargeCorpus.txt')
    # CoWord_PK2TXT(CoWordfp, FCoWord)
    CoWordXlsfp = os.path.join(xlsdir, 'figures.xls')
    CESecDistribution2Xls(CoWordXlsfp, PaperTestList)
    # CoWord_PK2XLS(CoWordXlsfp, FCoWord, 'Sys_CE_AC_CoWord')
