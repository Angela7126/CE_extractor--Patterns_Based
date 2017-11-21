# -*- coding: UTF-8 -*-

#######################################################################################
# --------------------------------- Function Introduce ------------------------------ #
#######################################################################################
# This functions set intends to:
#   Define a new Paper class -- Paper1;
#   Define a new Sent class -- Sent1;
#   Define a new CELink class -- CElink1.
# 1. Add human labeled Cause-effect cases id to each Sent object: self.manual_CEid, default as -1
# 2. Add pattern matched Cause-effect cases id to each Sent object: self.system_CEid, default as -1
# 3. Add manual_CEid and pattern_CEid to each CElink1
# 4. Add manual CE links set -- man_CE_list to each Paper1 object
# 5. Add pattern CE links set -- sys_CE_list to each Paper1 object

#######################################################################################
# ---------------------------------- Global variable -------------------------------- #
#######################################################################################
import os
import re
import sys
import pyodbc
import operator
import nltk
import xlwt
import xlrd
from xlutils.copy import copy
from cmyPackage import *
from cmyWordsCompare import ReadDB_Ftaglist, Check_C_P_S

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
def ShowCEPaper(CEPaper, paper):
    print "Ftag: " + str(paper.Ftag)
    print "c_num", CEPaper.c_num, "c_num_old:", paper.c_num
    print "p_num", CEPaper.p_num, "p_num_old:", paper.p_num
    print "s_num", CEPaper.s_num, "s_num_old:", paper.s_num
    # ShowCESentInfo(CEPaper)
    # for ce in CEPaper.sys_CE_list:
    #     print ce.sysCEid, ce.Staglst, ce.cw_span, ce.ew_span
    #     print
    for ce in CEPaper.man_CE_list:
        print ce.manCEid, ce.Staglst, ce.cw_span, ce.ew_span
        print
    print "-----------------------------------------"

def ShowCESentInfo(f):
    for s in f.S_list[0:50]:
        print "--------Stag: " + str(s.Stag) + "--------"
        print "Ctag:",s.Ctag,"SCtag",s.SCtag,"Ptag",s.Ptag,"text:",s.text
        print "sysCEidlst",s.sysCEidlst
        print "manCEidlst", s.manCEidlst
    print "\n"

class ManCESec:
    def __init__(self, ftag):
        self.Ftag = ftag
        self.CESeclst = []

def GetManCEonSec():
    CEPaperList = Loadpickle(os.path.join(DICpkdir, "KGCEPaperList.pk"))
    manCE_FtagList = ReadDB_Ftaglist()
    ManCESeclst = []

    for cepaper in CEPaperList:
        if cepaper.Ftag not in manCE_FtagList:
            continue
        ManCESeclst.append(ManCESec(cepaper.Ftag))
        SentVisit = [False] * len(cepaper.S_list)  # SentVisit is avoid re-add sents into 'CEonSec' object's CEsent list;

        curCESecList = [CEonSec(0, 'Abstract')]
        for c in cepaper.C_list:
            curCESecList.append(CEonSec(c.Ctag, c.Ctitle))
        curCESecList.sort(key=operator.attrgetter('Ctag'))
        ### step 2: fill each CEonSec object's sent list.
        for s in cepaper.S_list:
            try:
                curCESecList[s.Ctag].Slist.append(s)
            except IndexError:
                print s.Ctag, type(s.Ctag), s.Stag, s.text
                sys.exit()
        ### step 3: fill each CEonSec object's CE list and CEsent list (the sent set construct its CE list);
        ###     Notice that we suppose there is no CE case skip two adjacent sections.
        ###     So, we use the CE case's first sent's Sec_id as the CE case's Sec_id.
        for ce in cepaper.man_CE_list:
            if len(ce.Staglst) > 0:  # if the CE case has no sent information, skip it;
                cid = cepaper.S_list[ce.Staglst[0]].Ctag
                curCESecList[cid].CElist.append(ce)
                for ces in ce.Staglst:
                    if not SentVisit[ces]:
                        SentVisit[ces] = True
                        curCESecList[cid].CEsent.append(cepaper.S_list[ces])
        ### step 4: sort the Slist and CEsent list for each CEonSec object by their 'Stag' value in ascending order
        for j in range(len(curCESecList)):
            curCESecList[j].Slist.sort(key=operator.attrgetter('Stag'))
            curCESecList[j].CEsent.sort(key=operator.attrgetter('Stag'))
        ### step 5: added current file's CEonSec object list into its PaperTest object
        ManCESeclst[-1].CESeclst = curCESecList

    # print len(ManCESeclst)
    # for mance in ManCESeclst:
    #     print mance.Ftag
    Dumppickle(os.path.join(DICpkdir, "KGManCESeclst.pk"), ManCESeclst)
    return ManCESeclst

def CESecDistribution2Xls(Recfp, ManCESeclst):
    oldWB = xlrd.open_workbook(Recfp, formatting_info=True)
    WB = copy(oldWB)
    for i, mance in enumerate(ManCESeclst):
        WS = WB.add_sheet(mance.Ftag + "_ManCEonSec", cell_overwrite_ok='True')
        TitleRow = ['Section ID', 'Section Title', 'SentNum', 'CENum', 'SentCovered', 'Covered_Rate(%)']
        for j in range(len(TitleRow)):
            WS.write(0, j, TitleRow[j], xlwt.easyxf('font: bold on'))
        for j, CESec in enumerate(mance.CESeclst):
            WS.write(j + 1, 0, "%d" % CESec.Ctag)
            WS.write(j + 1, 1, CESec.Ctitle.decode('utf-8'))
            WS.write(j + 1, 2, "%d" % len(CESec.Slist))
            WS.write(j + 1, 3, "%d" % len(CESec.CElist))
            WS.write(j + 1, 4, "%d" % len(CESec.CEsent))
            WS.write(j + 1, 5, " %.4f" % (float(len(CESec.CEsent)) * 100 / len(CESec.Slist) if len(CESec.Slist) > 0 else 0))
    WB.save(Recfp)

#######################################################################################
# --------------------------------- Read Database file ------------------------------ #
#######################################################################################

def ReadDB_CELinks(Ftag):
    # ----------- Connect Database --------------
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + dbfile + ";Uid=;Pwd=;")
    ce_cursor = conn.cursor()
    # -------------------------------------------
    CESQL = "SELECT ID, Context, A, B, Pattern from CE_Relation where Ftag = \'"+Ftag+"\' order by ID;"
    CELinks = []
    for row in ce_cursor.execute(CESQL):
        CELinks.append(row)

    ce_cursor.close()
    conn.close()

    return CELinks

#######################################################################################
# --------------------------- Covert old object to new ------------------------------ #
#######################################################################################
# ---- Get Sentence ID list from CEPaper according to context_sheet ----
# Input:
#   1. context_sheet: a list of language units store in [type, text or id] form
#                     type -- the type of the language unit, 0 is sentence, 1 is paragraph, 2 is section, -1 is a piece of sentence text
#                     id -- the id of corresponding language unit in CEPaper
#                     text -- the text content of a piece of sentence
#   2. CEPaper: a Paper1 object
# Output:
#       a sentence id list that all of them involved in this cause-effect link
def GetSentIDlist(context_sheet, CEPaper):
    SentIDlst = []
    for ctxt in context_sheet:
        if ctxt[0] == 0:
            SentIDlst.append(ctxt[1])
        elif ctxt[0] == 1:
            para = CEPaper.P_list[ctxt[1]]
            for s in para.slist:
                SentIDlst.append(s.Stag)
        elif ctxt[0] == 2:
            sec = CEPaper.C_list[ctxt[1]]
            for para in sec.plist:
                for s in para.slist:
                    SentIDlst.append(s.Stag)
        else:
            continue
    return SentIDlst

# ---- Get the word span of a cause or effect in a sentence list ----
def FindCorEWordSpan(sheet, Staglst, paper):
    span = []
    # -- get cause or effect's text content or sentence id list
    c_or_e_txt = []
    c_or_e_staglst = []
    for tempsheet in sheet:
        if tempsheet[0] == -1:
            c_or_e_txt = nltk.word_tokenize(strdecode(tempsheet[1]))
        else:
            c_or_e_staglst.extend(GetSentIDlist([tempsheet], paper))
    # -- if cause or effect is text content
    if len(c_or_e_txt) != 0:
        sentwlen = [0]
        sentwords = []
        for sid in Staglst:
            tempwords = nltk.word_tokenize(strdecode(paper.S_list[sid].text))
            sentwlen.append(len(tempwords)+sentwlen[-1])
            sentwords.extend(tempwords)
        for i in range(len(sentwords)-len(c_or_e_txt)+1):
            if sentwords[i:i+len(c_or_e_txt)] != c_or_e_txt:
                continue
            j = i + len(c_or_e_txt) - 1
            idx = 1
            for sentlen in sentwlen[1:]:
                if i < sentlen:
                    span.append((idx-1, i-sentwlen[idx-1]))
                    break
                idx += 1
            for sentlen in sentwlen[idx:]:
                if j < sentlen:
                    span.append((idx - 1, j-sentwlen[idx - 1]))
                    break
                idx += 1
            break
        return span
    else:
        for i in range(len(Staglst)-len(c_or_e_staglst)+1):
            if Staglst[i:i+len(c_or_e_staglst)] != c_or_e_staglst:
                continue
            j = i + len(c_or_e_staglst)-1
            span.append((i, 0))
            sent_at_j_wlist = nltk.word_tokenize(strdecode(paper.S_list[Staglst[j]].text))
            span.append((j, len(sent_at_j_wlist)-1))
            break
        return span

# ---- convert the whole old pattern matched CElist into CELink1 object list ----
def GetSysCE(oldsysCElist):
    sysCElist = []
    sysce_sent_id_dict = {}
    for ceid, oldce in enumerate(oldsysCElist):
        ce = CELink1(ceid, oldce.pt)
        for temps in oldce.sInfo:
            ce.Staglst.append(temps.Stag)
            if sysce_sent_id_dict.has_key(temps.Stag):
                sysce_sent_id_dict[temps.Stag].append(ceid)
            else:
                sysce_sent_id_dict[temps.Stag] = [ceid]
        ce.cw_span = oldce.cause.span
        ce.ew_span = oldce.effect.span
        sysCElist.append(ce)
    return sysCElist, sysce_sent_id_dict

# ---- convert the whole old manual labeled CE list into CELink2 object list ----
def GetManCE(paper, oldmanCElist):
    # ---- convert the whole old manual labeled CElist into CELink1 object list ----
    manCElist = []
    mance_sent_id_dict = {}
    for oldmance in oldmanCElist:
        # --- create a CELink2 object for a manual labeled cause-effect link ---
        mance = CELink2(oldmance.ID, oldmance.Pattern)  # manual labeled ce's pattern only has main_tokens
        # --- get each ce link's Staglst ---
        context_sheet = Check_C_P_S(oldmance.Context)
        cause_sheet = Check_C_P_S(oldmance.A)
        effect_sheet = Check_C_P_S(oldmance.B)
        if cause_sheet[0][0] == -1 or effect_sheet[0][0] == -1:
            mance.Staglst = GetSentIDlist(context_sheet, paper)
        else:
            mance.Staglst = GetSentIDlist(cause_sheet, paper)
            mance.Staglst.extend(GetSentIDlist(effect_sheet, paper))
            mance.Staglst = sorted(list(set(mance.Staglst)))
        # --- find cause word span and effect word span ----
        mance.cw_span = FindCorEWordSpan(cause_sheet, mance.Staglst, paper)
        mance.ew_span = FindCorEWordSpan(effect_sheet, mance.Staglst, paper)
        for sid in mance.Staglst:
            if mance_sent_id_dict.has_key(sid):
                mance_sent_id_dict[sid].append(oldmance.ID)
            else:
                mance_sent_id_dict[sid] = [oldmance.ID]
        manCElist.append(mance)
    return manCElist, mance_sent_id_dict


# ---- Convert a Paper object to Paper1 object according to its pattern matched CE links list ----#
# Input:
#   1. paper -- a Paper object (see cmyPreprocess.py)
#   2. oldsysCElist -- the pattern matched cause-effect link list stored as CElink object (see cmyPatternMatching.py)
#   3. old manCElist -- the manual labeled cause-effect link list stored as a pyodbc.row object, each has "ID", "Context", "A", "B", "Pattern" attributes
# Output:
#   a Paper1 object
def PaperAddSysManCE(paper, oldsysCElist, oldmanCElist=[]):
    # ---- convert non sentence object related information ----
    newpaper = Paper1(paper.Ftag)
    newpaper.Ftitle = paper.Ftitle
    newpaper.author = paper.author
    newpaper.auinfo = paper.auinfo
    newpaper.KeyW = paper.KeyW
    newpaper.Refer = paper.Refer
    # ---- get pattern matched CE links list and mapping sentence id to pattern matched ce id ----
    sysCElist, sysce_sent_id_dict = GetSysCE(oldsysCElist)
    newpaper.sys_CE_list = sysCElist
    newpaper.sysce_sent_id_dict = sysce_sent_id_dict
    # ---- get manual labeled CE links list and mapping sentence id to manual labeled ce id ----
    if len(oldmanCElist) == 0:
        manCElist, mance_sent_id_dict = [], {}
    else:
        manCElist, mance_sent_id_dict = GetManCE(paper, oldmanCElist)
    newpaper.man_CE_list = manCElist
    newpaper.mance_sent_id_dict = mance_sent_id_dict
    # ---- convert the abstract into Sent1 object list ----
    for abs in paper.Abstract:
        newabs = Sent1(abs.Ctag, abs.SCtag, abs.Ptag, abs.Stag, abs.text)
        if sysce_sent_id_dict.has_key(newabs.Stag):
            newabs.sysCEidlst = sysce_sent_id_dict[newabs.Stag]
        if mance_sent_id_dict.has_key(newabs.Stag):
            newabs.manCEidlst = mance_sent_id_dict[newabs.Stag]
        newpaper.Abstract.append(newabs)
    # ---- convert each sentence in S_list into Sent1 object ----
    for s in paper.S_list:
        new_s = Sent1(s.Ctag, s.SCtag, s.Ptag, s.Stag, s.text)
        if sysce_sent_id_dict.has_key(s.Stag):
            new_s.sysCEidlst = sysce_sent_id_dict[s.Stag]
        if mance_sent_id_dict.has_key(s.Stag):
            new_s.manCEidlst = mance_sent_id_dict[s.Stag]
        newpaper.S_list.append(new_s)
    # ---- convert each paragraph's slist in P_list  ---- #
    newpaper.P_list = paper.P_list
    for newp in newpaper.P_list:
        newp.slist = []
        newp.sent_num = 0
    for new_s in newpaper.S_list:
        newpaper.P_list[new_s.Ptag].slist.append(new_s)
        newpaper.P_list[new_s.Ptag].sent_num += 1
    # ---- convert each section's plist in C_list ---- #
    newpaper.C_list = paper.C_list
    for idx in range(len(newpaper.C_list)):
        newpaper.C_list[idx].plist = []
        newpaper.C_list[idx].p_num = 0
        for subidx in range(len(newpaper.C_list[idx].sclist)):
            tempplist = newpaper.C_list[idx].sclist[subidx].plist
            newpaper.C_list[idx].sclist[subidx].plist = []
            newpaper.C_list[idx].sclist[subidx].p_num = 0
            for p in tempplist:
                newpaper.C_list[idx].sclist[subidx].plist.append(newpaper.P_list[p.Ptag])
                newpaper.C_list[idx].sclist[subidx].p_num += 1
                newpaper.C_list[idx].plist.append(newpaper.P_list[p.Ptag])
                newpaper.C_list[idx].p_num += 1
    # ---- get other number attribute ----
    newpaper.s_num = len(newpaper.S_list)
    newpaper.p_num = len(newpaper.P_list)
    newpaper.c_num = len(newpaper.C_list)
    return newpaper

# ---- Convert the whole corpus to Paper1 object list ----
def PaperList2Paper1List(paperpkfp, celistpkfp):
    PaperList = Loadpickle(paperpkfp)
    CEList = Loadpickle(celistpkfp)
    CEPaperList = []
    manCE_FtagList = ReadDB_Ftaglist()

    for idx, paper in enumerate(PaperList):
        oldsysCElist = CEList[idx]
        if paper.Ftag in manCE_FtagList:
            oldmanCElist = ReadDB_CELinks(paper.Ftag)
            CEPaper = PaperAddSysManCE(paper, oldsysCElist, oldmanCElist)
        else:
            CEPaper = PaperAddSysManCE(paper, oldsysCElist)
        # ShowCEPaper(CEPaper, paper)
        CEPaperList.append(CEPaper)
    Dumppickle(os.path.join(DICpkdir, "KGCEPaperList.pk"), CEPaperList)
    return

#######################################################################################
# ---------------------------------- Main function ---------------------------------- #
#######################################################################################
if __name__ == "__main__":
    # paperpkfp = os.path.join(DICpkdir, "KGPaperList.pk")
    # celistpkfp = os.path.join(DICpkdir, "KGCEList.pk")
    # PaperList2Paper1List(paperpkfp, celistpkfp)
    # ManCESeclst = GetManCEonSec()
    ManCESeclst = Loadpickle(os.path.join(DICpkdir, "KGManCESeclst.pk"))
    xlsfp = os.path.join(xlsdir, 'ManCEonSec_figures.xls')
    CESecDistribution2Xls(xlsfp, ManCESeclst)

