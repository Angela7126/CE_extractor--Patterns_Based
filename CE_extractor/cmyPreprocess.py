# -*- coding: UTF-8 -*- 

#######################################################################################
# --------------------------------- Function Introduce ------------------------------ #
#######################################################################################
# This functions set intends to:
# 1. Split the txt_type file into sections, paragraphs, sentences and sub_sentences object;
# 2. Insert current file info into xlsx tables


#######################################################################################
# ---------------------------------- Global variable -------------------------------- #
#######################################################################################
import os
import re
import xlwt
from cmyToolkit import *
from nltk.parse import stanford
from nltk.tree import *
from cmyPackage import *

# ------------ set some folder path ---------------
corpdir = os.path.join(os.getcwd(), "Corpus")
pkdir = os.path.join(os.getcwd(), "PK")
TXTcorpdir = os.path.join(os.getcwd(), "Corpus", "TXT")
TXTpkdir = os.path.join(os.getcwd(), "PK", "TXT")
DICpkdir = os.path.join(os.getcwd(), "PK", "DIC")
ctxtdir = os.path.join(os.getcwd(), "CheckTXT")
xlsdir = os.path.join(os.getcwd(), 'XLS')
dbfile = os.path.join(os.getcwd(), 'CErelation.accdb')
### ---- stanford_parser java package ----  
os.environ['STANFORD_PARSER'] = r'D:\jars\stanford-parser.jar'
os.environ['STANFORD_MODELS'] = r'D:\jars\stanford-parser-3.5.2-models.jar'
### ---- JAVA_HOME path ----
java_path = r"C:\Program Files\Java\jdk1.8.0_45\bin\java.exe"
os.environ['JAVAHOME'] = java_path


#######################################################################################
# ---------------------------------- Extract Patterns ------------------------------- #
#######################################################################################
# ============= extract paragraph from the whole text ===============
def Extract_txt_P(file_text):
    # file_text split into paragraph
    P_txt_list = re.split("[\n]{2,}", file_text)
    return P_txt_list


# ============= extract sentence from a paragraph ===============
def Extract_txt_S(file_text):
    # file_text split into paragraph
    S_txt_list = re.split("(?<=[\.|?|!|;|:])[ |\"|\'|\)]+", file_text.strip())
    return S_txt_list


# =========== delete extra blank characters =========
def sent_txt_process(s_txt):
    # replace the '\n' in the sentence with ' '
    s_txt = re.sub('[ ]+', ' ', re.sub('[\r|\n]+', ' ', s_txt))
    # delete the space at the begin and the end of the sentence.
    s_txt = s_txt.strip()
    return s_txt


#######################################################################################
# ---------------------------------- Check Patterns --------------------------------- #
#######################################################################################
# +++++ check whether a string is the begin of a section +++++
def CheckSec(s_txt):
    return re.match("[\d]+\.[ ]*$", s_txt)


# +++++ check whether a string is the begin of a subsection +++++
def CheckSubSec(s_txt):
    return re.match(r"[\d]+\.[\d]+[ ]*", s_txt)


# +++++ check whether a string is the begin of abstraction +++++
def CheckAbs(s_txt):
    return re.match("abstract[ ]*$", s_txt.lower())


# +++++ check whether a string is the begin of keywords +++++
def CheckKey(s_txt):
    return re.match("keywords", s_txt.lower())


# +++++ check whether a string is the begin of a reference +++++
def CheckRef(s_txt):
    return re.match("references", s_txt.lower())


#######################################################################################
# -------------------------------- xlsx tables related ------------------------------ #
#######################################################################################
# ^^^^^^^^^^^^^^ set the font of a xls ceil ^^^^^^^^^^^^^^
def set_xlstyle(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


# ^^^^^^^^^^^^^^^ write a xls file ^^^^^^^^^^^^^^^^^^
def WriteXls(curfile):
    FIpath = os.path.join(xlsdir, curfile.Ftag + '.xls')  # creating xls files for each paper
    # WB = xlwt.Workbook()
    WB = xlwt.Workbook(encoding='utf-8')
    # the default encoding is "ascii", if encoding as ascii will cause error when save
    # ------------------Creat FileInfo sheet WS0-------------------
    WS0 = WB.add_sheet('FileInfo', cell_overwrite_ok='True')
    FIrow0 = ['Ftag', 'Ftitle', 'Author', 'auinfo', 'KeyW']
    for i in range(len(FIrow0)):
        WS0.write(0, i, FIrow0[i], set_xlstyle('Times New Roman', 220, True))
    WS0.write(1, 0, curfile.Ftag)
    WS0.write(1, 1, curfile.Ftitle)
    WS0.write(1, 2, curfile.author)
    WS0.write(1, 3, '; '.join(curfile.auinfo))
    WS0.write(1, 4, '; '.join(curfile.KeyW))
    # ------------------Creat Refer Sheet WSRefer-------------------------
    WSRefer = WB.add_sheet('Refer', cell_overwrite_ok='True')
    FRrow0 = ['Ftag', 'Rtag', 'text']
    for i in range(len(FRrow0)):
        WSRefer.write(0, i, FRrow0[i], set_xlstyle('Times New Roman', 220, True))
    r = 1
    for R in curfile.Refer:
        WSRefer.write(r, 0, curfile.Ftag)
        WSRefer.write(r, 1, str(R.Rtag))
        WSRefer.write(r, 2, R.text)
        r = r + 1
    # ------------------Creat Sent Sheet WSsent-------------------------
    WSsent = WB.add_sheet('Sent', cell_overwrite_ok='True')
    FSrow0 = ['Ftag', 'Ctag', 'SCtag', 'Ptag', 'Stag', 'text']
    for i in range(len(FSrow0)):
        WSsent.write(0, i, FSrow0[i], set_xlstyle('Times New Roman', 220, True))
    r = 1
    for s in curfile.S_list:
        WSsent.write(r, 0, curfile.Ftag)
        WSsent.write(r, 1, str(s.Ctag))
        WSsent.write(r, 2, str(s.SCtag))
        WSsent.write(r, 3, str(s.Ptag))
        WSsent.write(r, 4, str(s.Stag))
        WSsent.write(r, 5, s.text)
        r = r + 1
    # ------------------Creat SecInfo Sheet WSsec-------------------------
    WSsec = WB.add_sheet('SecInfo', cell_overwrite_ok='True')
    FCrow0 = ['Ftag', 'Ctag', 'Ctitle', 'sc_num', 'p_num']
    for i in range(len(FCrow0)):
        WSsec.write(0, i, FCrow0[i], set_xlstyle('Times New Roman', 220, True))

    if len(curfile.Abstract) > 0:
        FCrow1 = [curfile.Ftag, '0', 'Abstract', '1', str((curfile.Abstract)[-1].Ptag + 1)]
        for i in range(len(FCrow1)):
            WSsec.write(1, i, FCrow1[i])
        r = 2
    else:
        r = 1
    for s in curfile.C_list:
        WSsec.write(r, 0, curfile.Ftag)
        WSsec.write(r, 1, str(s.Ctag))
        WSsec.write(r, 2, s.Ctitle)
        WSsec.write(r, 3, str(s.sc_num))
        WSsec.write(r, 4, str(s.p_num))
        r = r + 1
    # ------------------Creat SecInfo Sheet WSsubsec-------------------------
    WSsubsec = WB.add_sheet('SubSecInfo', cell_overwrite_ok='True')
    FSCrow0 = ['Ftag', 'Ctag', 'SCtag', 'SCtitle', 'p_num']
    for i in range(len(FSCrow0)):
        WSsubsec.write(0, i, FSCrow0[i], set_xlstyle('Times New Roman', 220, True))
    r = 1
    for s in curfile.C_list:
        for sc in s.sclist:
            WSsubsec.write(r, 0, curfile.Ftag)
            WSsubsec.write(r, 1, str(sc.Ctag))
            WSsubsec.write(r, 2, str(sc.SCtag))
            WSsubsec.write(r, 3, sc.SCtitle)
            WSsubsec.write(r, 4, str(sc.p_num))
            r = r + 1
    WB.save(FIpath)


#######################################################################################
# -------------------------------- Dealing whole corpus ----------------------------- #
#######################################################################################
def FilePaser():
    [file_pn, file_pn_new] = Get_Build_fpathes(TXTcorpdir, TXTpkdir)
    # file_pn is the file path set of all files in TXTcorpdir, and file_pn_new is the new file path set in TXTpkdir according to each file_pn
    filenum = len(file_pn)  # filenum is the number of files in the corpus
    Flist = Loadpickle(os.path.join(DICpkdir,"KGPaperList.pk"))#[]  # Flist is the paper class list for every paper in file_pn
    SCIDpattern = re.compile(r'(?<=\d\.)[\d]+ ')  # regular expression pattern to get SCID
    CIDpattern = re.compile(r'[\d]+(?=[\.| ])')  # regular expression pattern to get CID
    RIDpattern = re.compile(r'(?<=\[).+(?=\])')  # regular expression pattern to get RID
    ### ---- initiate a parser ----
    parser = stanford.StanfordParser(model_path=r"D:\jars\englishPCFG.ser.gz")
    # errorfilepath = os.path.join(os.getcwd(),'errorfile2.txt')
    # errorfile = codecs.open(errorfilepath,'w','utf8')

    for fi in [21, 27, 28,  32, 33]:#filenum):
        print "start process " + file_pn[fi] + '...'
        fname, ftype = os.path.splitext(os.path.basename(file_pn[fi]))  # fname is the file name of file_pn[fi]
        fp = ReadFile(os.path.join(TXTcorpdir, file_pn[fi]))  # get the text of file_pn[fi]
        P_txt_list = Extract_txt_P(fp)  # get paragraph text list
        # -------- creating a Paper object ---------------
        Curfile = Paper(fname)
        Curfile.Ftitle = sent_txt_process(P_txt_list[0])
        Curfile.auinfo.append(sent_txt_process(P_txt_list[1]))
        Curfile.auinfo.append(sent_txt_process(P_txt_list[2]))
        Curfile.author = sent_txt_process(P_txt_list[3])
        # errorfile.write(curfile.Ftag+"\n")
        # -------------- parameter initial --------------------
        PID = 0
        SID = 0
        Pstart = 0
        PSstart = 0
        Sstart = 0
        CID = 0
        SCID = 0
        RID = 0
        tempC_list = []
        tempSC_list = []
        tempP_list = []
        tempS_list = []
        Subsec0flag = 0
        # Subsec0flag = 1 means that current section has no subsection yet
        # Subsec0flag = 0 means that current section has built subsection
        Curstate = 0
        # Curstate = 1 means append current parag to current SubSection
        # Curstate = 2 means append current parag to abstract
        # Curstate = 3 means append current parag to reference
        # ---------------- process the main body ---------------
        for i in range(4, len(P_txt_list)):
            # extract the sentence text from the current paragraph
            S_txt_list = []
            for j in Extract_txt_S(P_txt_list[i]):
                if len(j) > 0:
                    S_txt_list.append(j)
            Snum = len(S_txt_list)
            if Snum == 0:
                continue
                # ---------check whether current paragraph is the begin of keywords,abstract,...,section------
            check = S_txt_list[0]
            # if current paragraph is keywords, put it into curfile.keyW
            if CheckKey(check):
                for k in S_txt_list:
                    klist = re.split("[:|;|,|.]", k)
                    for tempk in klist:
                        if re.match("^[\s]*$", tempk):
                            continue
                        Curfile.KeyW.append(tempk)
                del Curfile.KeyW[0]
            # if "abstract" has shown, the following paragraph should put into curfile.Abstract
            elif CheckAbs(check):
                Curstate = 2
                continue
            # if "Reference" has shown, the following paragraph should put into curfile.Refer
            elif CheckRef(check):
                Curstate = 3
                continue
            # if digit like "1.6 asdfkl" has shown, the following paragraph should put into a subsection
            elif CheckSubSec(check):
                if Subsec0flag == 1 and PSstart < PID:  # if there has history subsection content but has no subsection for current section yet, build a subsection 0
                    tempSC_list.append(SubSec(CID, 0, None))
                if len(tempSC_list) > 0 and PSstart < PID:  # put history subsection content into last subsection
                    tempSC_list[-1].p_num = PID - PSstart
                    tempSC_list[-1].plist.extend(tempP_list[PSstart:PID])
                SCID = int((SCIDpattern.search(check)).group())  # get SCID for new subsection
                SCtitle = re.split(r'[\d]+ ', check)  # get SCtitle for new subsection
                tempSC_list.append(SubSec(CID, SCID, SCtitle[1] + ' ' + ' '.join(
                    S_txt_list[1:Snum])))  # create a new empty subsection object
                PSstart = PID  # set history content start position of the new subsection object
                Curstate = 1
                Subsec0flag = 0  # There has subsection in current section
                continue
            # if digit like "2. dsdlfj" has shown, build a new section object
            elif CheckSec(check):
                if Subsec0flag == 1:  # if last section has no subsection, create a subsection 0
                    tempSC_list.append(SubSec(CID, 0, None))
                if len(tempSC_list) > 0:
                    tempSC_list[-1].p_num = PID - PSstart
                    tempSC_list[-1].plist.extend(tempP_list[PSstart:PID])
                if len(tempC_list) > 0:  # if put history content into last section
                    tempC_list[-1].p_num = PID - Pstart
                    tempC_list[-1].plist.extend(tempP_list[Pstart:PID])
                    tempC_list[-1].sc_num = len(tempSC_list)
                    tempC_list[-1].sclist.extend(tempSC_list)
                CID = int((CIDpattern.search(check)).group())  # get CID for new section
                tempC_list.append(Sec(CID, ' '.join(S_txt_list[1:Snum])))  # create a new section object
                Pstart = PID  # set hisotry content start for new section object
                PSstart = PID  # set hisotry content start for future subsection object of the new section object
                SCID = 0
                Subsec0flag = 1
                tempSC_list = []
                Curstate = 1
                continue
            # if the current P_txt_list[i] is the text
            else:
                if Curstate == 3:  # if has find "Reference", put the following reference into Curfile.Refer
                    RID = (RIDpattern.search(S_txt_list[0])).group()
                    try:
                        RID = int(RID)
                    except ValueError:
                        pass
                    Curfile.Refer.append(Refer(RID, ' '.join(S_txt_list)))
                    continue

                for j in range(Snum):  # create Sent object set for current paragraph
                    tempsent = Sent(CID, SCID, PID, SID, S_txt_list[j])

                    try:
                        tempsentPT = parser.raw_parse(S_txt_list[j])
                    except UnicodeDecodeError:
                        # errorfile.write(str(tempsent.Stag)+":  "+S_txt_list[j]+"\n")
                        pass
                    tempsentPTlst = []
                    try:
                        while True:
                            tempsentPTlst.append(tempsentPT.next())
                    except StopIteration:
                        pass;
                    tempsent.PTree = tempsentPTlst

                    tempS_list.append(tempsent)
                    SID = SID + 1

                if Curstate == 2:  # if has find "Abstract", put the following paragraph into Curfile.Abstract
                    Curfile.Abstract.extend(tempS_list[Sstart:SID])

                tempP_list.append(Parag(CID, SCID, PID, SID - Sstart, tempS_list[Sstart:SID]))  # create Parag object
                Sstart = SID  # set Sstart as the begin of next paragraph
                PID = PID + 1  # increase the PID for next Paragraph
        # --------------- put history content into last Subsection ----------------
        if Subsec0flag == 1 and PSstart < PID:
            tempSC_list.append(SubSec(CID, 0, None))
        if len(tempSC_list) > 0:
            tempSC_list[-1].p_num = PID - PSstart
            tempSC_list[-1].plist.extend(tempP_list[PSstart:PID])
        # -------------- put history content into last section ----------------
        if len(tempC_list) > 0:
            tempC_list[-1].sc_num = len(tempSC_list)
            tempC_list[-1].sclist.extend(tempSC_list)
            tempC_list[-1].p_num = PID - Pstart
            tempC_list[-1].plist.extend(tempP_list[Pstart:PID])
        # -------------- complete Curfile object ------------------
        Curfile.c_num = len(tempC_list)
        Curfile.C_list = tempC_list
        Curfile.p_num = len(tempP_list)
        Curfile.P_list = tempP_list
        Curfile.s_num = len(tempS_list)
        Curfile.S_list = tempS_list
        print "process completed!\n"
        # errorfile.write("\n\n\n\n")
        # -------------- write xls file --------------
        WriteXls(Curfile)
        # ----------- pickle current Curfile ---------
        Dumppickle(file_pn_new[fi], Curfile)
        # ---------- put Curfile into Flist ----------
        del(Flist[fi])
        Flist.insert(fi, Curfile)
        # Flist.append(Curfile)
    Dumppickle(os.path.join(DICpkdir, "KGPaperList.pk"), Flist)
    return Flist


#######################################################################################
# --------------------------- Some demonstration functions -------------------------- #
#######################################################################################
# -------------------- Show the current paper object --------------------
def cmyShowFileInfo(f):
    print "Ftag: " + str(f.Ftag)
    n = f.c_num
    print "C_num in " + str(f.Ftag) + " : " + str(n)
    print "Author of " + str(f.Ftag) + " : " + str(f.author)
    print "Title of " + str(f.Ftag) + " : " + str(f.Ftitle)
    print "\n"


# -------------------- Show the current paper's abstract --------------------
def cmyShowFileAbs(f):
    print "\t++++++++++++++++++++++Abstract++++++++++++++++++++++++++"
    for a in f.Abstract:
        print "\t\t\t--------Stag: " + str(a.Stag) + "--------"
        print "\t" + a.text
    print "\n"


# -------------------- Show the current paper's keywords --------------------
def cmyShowFileKeyW(f):
    print "\t^^^^^^^^^^^^^^^^^^^^^Keywords^^^^^^^^^^^^^^^^^^^^^^^"
    for k in f.KeyW:
        print "\t\t\t" + k
    print "\n"


# -------------------- Show the current paper's references --------------------
def cmyShowFileRefer(f):
    print "\t~~~~~~~~~~~~~~~~~~~~~References~~~~~~~~~~~~~~~~~~~~~~~~~~"
    for r in f.Refer:
        print "\t\t\t--------Rtag: " + str(r.Rtag) + "--------"
        print "\t" + r.text
    print "\n"


# -------------------- Show the current paper's sections information --------------------    
def cmyShowSecInfo(f):
    for tempc in f.C_list[0:2]:
        print "\t==================Ctag: " + str(tempc.Ctag) + " Ctitle: " + str(tempc.Ctitle) + "=================="
        print "\tsc_num: " + str(tempc.sc_num)
        print "\tp_num: " + str(tempc.p_num)
        for sc in tempc.sclist:
            print "\t\t#################SCtag: " + str(sc.SCtag) + " SCtitle: " + str(sc.SCtitle) + "################"
            print "\t\t p_num:" + str(sc.p_num)
            for p in sc.plist:
                print "\t\t\t************Ptag: " + str(p.Ptag) + "************"
                print "\t\t\tsent_num: " + str(p.sent_num)
                for s in p.slist:
                    print "\t\t\t\t\t--------Stag: " + str(s.Stag) + "--------"
                    print "\t\t\t" + s.text
    print "\n"
    print "\n"


# -------------------- Show the current paper's paragraph information --------------------
def cmyShowParagInfo(f):
    for tempp in f.P_list:
        print "\t************Ptag: " + str(tempp.Ptag) + " Sec: " + str(tempp.Ctag) + " Subsec: "+ str(tempp.SCtag)+ "*************"
        print "\t\tsent_num: " + str(tempp.sent_num)
        for s in tempp.slist:
            print "\t\t\t\t\t--------Stag: " + str(s.Stag) + "--------"
            print "\t\t\t" + s.text
    print "\n"


# -------------------- Show the sentence number of the whole corpus -------------------
def cmyShowSentNum(Paperlistpath):
    Flist = Loadpickle(Paperlistpath);
    sentnum_total = 0;
    for f in Flist:
        print f.Ftag, f.Ftitle, "SentNum =", len(f.S_list);
        sentnum_total += len(f.S_list);
    print "TotalSentNum = ", sentnum_total


# ----------- reproduce a text type file from a 'Paper' object storing in a PK file ----------
def PK2TXT(txt_pn, pk_pn):
    curfile = Loadpickle(pk_pn)
    fp = open(txt_pn, 'w');

    fp.write(curfile.Ftitle + '\r\n\r\n');
    for af in curfile.auinfo:
        fp.write(af + '\r\n\r\n');
    fp.write(curfile.author + '\r\n\r\n');

    if (len(curfile.Abstract) != 0):
        fp.write('Abstract\r\n\r\n')
        for aa in curfile.Abstract[0:-1]:
            fp.write(aa.text + ' ');
        fp.write((curfile.Abstract)[-1].text)
        fp.write('\r\n\r\n');

    if (len(curfile.KeyW) != 0):
        fp.write("Keywords: ")
        for kk in curfile.KeyW:
            fp.write(kk + '; ')
        fp.write('\r\n\r\n');

    for sec in curfile.C_list:
        fp.write(str(sec.Ctag) + '. ');
        fp.write(sec.Ctitle + '\r\n\r\n');
        for subsec in sec.sclist:
            if subsec.SCtag > 0:
                fp.write(str(sec.Ctag) + '.' + str(subsec.SCtag) + ' ');
                fp.write(subsec.SCtitle + '\r\n\r\n');
            for p in subsec.plist:
                for s in p.slist[0:-1]:
                    fp.write(s.text + ' ')
                fp.write((p.slist)[-1].text)
                fp.write('\r\n\r\n')

    if (len(curfile.Refer) != 0):
        fp.write("Reference\r\n\r\n")
        for r in curfile.Refer:
            fp.write(r.text + '\r\n\r\n')

    fp.close()


#######################################################################################
# ---------------------------------- Main function ---------------------------------- #
#######################################################################################

if __name__ == "__main__":
    Flist = FilePaser()
    paperpkfp = os.path.join(DICpkdir, "KGPaperList.pk")
    PaperList = Loadpickle(paperpkfp)
    for paper in PaperList:
        cmyShowFileInfo(paper)
    # Dumppickle(os.path.join(DICpkdir, "KGPaperList.pk"), PaperList)

 # cmyShowFileInfo(f)
 # cmyShowFileKeyW(f)
 # cmyShowFileAbs(f)
 # cmyShowFileRefer(f)
 # cmyShowSecInfo(f)

 ############################## Some unused Function #####################################
 #
 # ----Intend to write/read ACCESS database, but failed with connection----
 # import win32com.client
 # conn = win32com.client.Dispatch(r'ADODB.Connection')
 # DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE='+os.path.join(os.getcwd(),'CErelation.accdb')+';'
 # def DBInsert(self,curfile):
 #     conn.Open(DSN)
 #     rs = win32com.client.Dispatch(r'ADODB.Recordset')
 #     rs_name = 'MyRecordset'
 #     rs.open('['+rs_name+']',conn,1,3)
 #     rs.AddNew()
 #     rs.Fields.Item(1).Value = 'data'
 #     rs.Update()
 #
 # ----------------- Sub-Sentence class -------------------
 # class SubSent:
 #    def __init__(self, subs, t):
 #        self.SStag = subs
#        self.text = t
