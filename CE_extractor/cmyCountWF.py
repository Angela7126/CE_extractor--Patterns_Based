# -*- coding: UTF-8 -*- 

#######################################################################################
# --------------------------------- Function Introduce ------------------------------ #
#######################################################################################
# This functions set intends to:
# 1. split the file text into words
# 2. then count the word frequency.

#######################################################################################
# --------------------------------- Function Results -------------------------------- #
#######################################################################################
# There are 5402 words which contains more than 1 letter in all test files.
# and, there are 7464 pairs of (words, pos)
#
# We consider there are 35 word-level patterns:
# 1 page 11 patterns (192 words; 72 min-f): to; in; as; with; by; through; according; if; when; so; concerns; 
# 2 page 8 patterns (196 words; 34 min-f): way; because; indicate; shows; explanation; derived; since; enable;
# 3 page 4(196 words; 22 min-f): lead; concern; due; therefore;
# 4 page 4(196 words; 16 min-f): strategy; ensure; reason; implies;
# 5 page 2(196 words; 12 min-f): show; required;
# 6 page 2(196 words; 9 min-f): requests; requires;
# 7 page 1(196 words; 7 min-f): why
# 10 page 1(196 words; 4 min-f): request;
# 11 page 1(196 words; 3 min-f): once;
# 22 page 1(196 words; 1 min-f): require
#
# consider (word, pos) pairs:
# 1 page 5 pairs (30 pairs, min-f 332): ['to', 'TO']; ['in', 'IN']; ['as', 'IN']; ['with', 'IN']; ['by', 'IN'];
# 2 page 4 pairs (147 pairs, min-f 73): ['through', 'IN']; ['according', 'VBG']; ['if', 'IN']; ['when', 'WRB'];
# 3 page 6 pairs (147 pairs, min-f 38): ['concerns', 'VBZ']; ['way', 'NN']; ['so', 'RB']; ['because', 'IN']; ['shows', 'VBZ']; ['as', 'RB']
# 4 page 6 pairs (147 pairs, min-f 27): ['derived', 'VBN']; ['explanation', 'NN']; ['since', 'IN']; ['lead', 'VB']; ['so', 'IN']; ['due', 'JJ']
# 5 page 4 pairs (147 pairs, min-f 20): ['therefore', 'RB']; ['enable', 'VB']; ['indicate', 'VB']; ['indicate', 'VBP']
# 6 page 3 pairs (147 pairs, min-f 16): ['strategy', 'NN']; ['ensure', 'VB']; ['implies', 'VBZ']
# 7 page 2 pairs (147 pairs, min-f 13): ['concern', 'VB']; ['concern', 'NN']
# 8 page 2 pairs (147 pairs, min-f 10): ['reason', 'NN']; ['required', 'VBN']
# 9 page 4 pairs (147 pairs, min-f 9): ['enable', 'VBP']; ['requires', 'VBZ']; ['show', 'VB']; ['because', 'RB']
# 10 page 1 pairs (147 pairs, min-f 8): ['concerns', 'NNS']
# 12 page 1 pairs (147 pairs, min-f 6): ['reason', 'VB']
# 13 page 2 pairs (147 pairs, min-f 5): ['why', 'WRB']; ['requests', 'NNS']
# 17 page 2 pairs (147 pairs, min-f 3): ['in', 'RP']; ['requests', 'VBZ']
# 18 page 1 pairs (147 pairs, min-f 3): ['show', 'VBP']
# 19 page 1 pairs (147 pairs, min-f 3): ['once', 'RB']
# 20 page 1 pairs (147 pairs, min-f 3): ['lead', 'VBP']
# 22 page 1 pairs (147 pairs, min-f 2): ['explanation', 'VB']
# 25 page 3 pairs (145 pairs, min-f 2): ['in', 'RB']; ['derived', 'JJ']; ['request', 'VBP']
# 26 page 1 pairs (147 pairs, min-f 2): ['request', 'NN']
# 28 page 1 pairs (147 pairs, min-f 2): ['through', 'RP']
# 30 page 1 pairs (147 pairs, min-f 1): ['why', 'NNP']
# 31 page 2 pairs (147 pairs, min-f 1): ['once', 'IN']; ['required', 'JJ']
# 34 page 1 pairs (147 pairs, min-f 1): ['require', 'VBP']
# 36 page 1 pairs (147 pairs, min-f 1): ['so', 'CC']
# 37 page 1 pairs (147 pairs, min-f 1): ['why', 'VBG']
# 38 page 1 pairs (147 pairs, min-f 1): ['reason', 'NNP']
# 42 page 1 pairs (147 pairs, min-f 1): ['explanation', 'NNP']
# 46 page 1 pairs (147 pairs, min-f 1): ['to', 'IN']
# 47 page 2 pairs (144 pairs, min-f 1): ['why', 'VBZ']; ['shows', 'NNS']
# 48 page 1 pairs (135 pairs, min-f 1): ['with', 'RP']
# 49 page 1 pairs (144 pairs, min-f 1): ['requests', 'VBD']
# 50 page 1 pairs (147 pairs, min-f 1): ['show', 'NN']

#######################################################################################
# ---------------------------------- Global variable -------------------------------- #
#######################################################################################
import os
import nltk
import re
import string
import sys
from cmyPackage import *
from nltk.parse import stanford
from nltk.tree import *

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
# -------------------------- Words Frequency for each File -------------------------- #
#######################################################################################
def Build_w_pos_DIC():
    pk_path_list = Get_file_pathes( TXTpkdir)  # Return the file path list for the pickle files for each document after pre-processing
    WPFlist = []  # The WPFdic for the whole corpus，each element is a WPFdic for a document
    ParseTreelist = []  # The Stanford-parser Tree list for the whole corpus, each element is a parser tree list for a document
    Puncs = Loadpickle(os.path.join(os.getcwd(), "PK", "Puncs.pk"))  # The punctuation list that we need to Ignore
    # parser = stanford.StanfordParser(model_path="D:\jars\englishPCFG.ser.gz") # Create a stanford-parser object
    for pkpath in pk_path_list:
        print "start process " + pkpath + '...'
        curfile = Loadpickle(pkpath)
        curWPF = WPF()
        curParseTreelist = []
        sentlist = curfile.S_list

        for sent in sentlist:
            sentPT = sent.PTree
            curParseTreelist.extend(sentPT)
            for temptree in sentPT:
                for wp in temptree.pos():  # pos()函数返回该句法树所有：(叶子结点-词,对应的POS——tag), 是一个tuple的list
                    key = (wp[0]).lower()  # 词小写
                    pos = wp[1]
                    # ---------- 遇到词是标点符号的直接跳过 -------------------
                    if key in Puncs:
                        continue
                    elif len(key) < 2:
                        continue
                    else:
                        # ----------- 否则插入当前文章的W_Pdic，W_Fdic，WP_Fdic三个词典中 -----------
                        if (curWPF.W_Pdic).has_key(key):
                            (curWPF.W_Fdic)[key] += 1
                            if pos not in (curWPF.W_Pdic)[key]:
                                (curWPF.W_Pdic)[key].append(pos)
                        else:
                            (curWPF.W_Pdic)[key] = [pos]
                            (curWPF.W_Fdic)[key] = 1
                        if (curWPF.WP_Fdic).has_key((key, pos)):
                            (curWPF.WP_Fdic)[(key, pos)] += 1
                        else:
                            (curWPF.WP_Fdic)[(key, pos)] = 1
        # ------------- 将当前文章的句法树列表以及WPFdic加入文档集的句法树列表以及WPFdic列表之中 ----------
        WPFlist.append(curWPF)
        ParseTreelist.append(curParseTreelist)
        print "process completed!\n"

    # --------存储Pickle文件以便下次访问--------------------
    Dumppickle(os.path.join(DICpkdir, 'KGWPFdiclist.pk'), WPFlist)
    Dumppickle(os.path.join(DICpkdir, 'KGParseTreelist.pk'), ParseTreelist)

    return [ParseTreelist, WPFlist]


#######################################################################################
# ------------------------ Words Frequency for whole corpus ------------------------- #
#######################################################################################
def GetTotalWPFdic():
    WPFdiclist = Loadpickle(os.path.join(DICpkdir, 'KGWPFdiclist.pk'))
    WPFdic = WPF()
    for curdic in WPFdiclist:
        for k, v in (curdic.W_Fdic).items():
            if len(k) < 2:
                continue
            elif k in (WPFdic.W_Fdic).keys():
                WPFdic.W_Fdic[k] += v
            else:
                WPFdic.W_Fdic[k] = v
        for k, v in (curdic.W_Pdic).items():
            if len(k) < 2:
                continue
            elif k in (WPFdic.W_Pdic).keys():
                WPFdic.W_Pdic[k] = list(set(WPFdic.W_Pdic[k] + v))
            else:
                WPFdic.W_Pdic[k] = v
        for k, v in (curdic.WP_Fdic).items():
            if len(k[0]) < 2:
                continue
            elif k in (WPFdic.WP_Fdic).keys():
                WPFdic.WP_Fdic[k] += v
            else:
                WPFdic.WP_Fdic[k] = v

    # --------Store the WPFdic object  as Pickle file--------------------
    Dumppickle(os.path.join(DICpkdir, 'KGTotalWPFdic.pk'), WPFdic)
    # --- Write the WPTdic object as text file for human observation convenience  ---
    WPFpath = os.path.join(os.getcwd(), 'Wfrequence', 'WPFdic.txt')
    WPFfp = codecs.open(WPFpath, 'w', 'utf8')
    WriteTXT(WPFfp, WPFdic)


#######################################################################################
# -------------------------- Some demonstration functions --------------------------- #
#######################################################################################
def showWordFrequency():
    WPFdiclist = Loadpickle(os.path.join(DICpkdir, 'KGWPFdiclist.pk'))
    for i in range(len(WPFdiclist)):
        fname = 'WPFf%04d' %(i + 1) + '.txt'
        WPFpath = os.path.join(r"E:\Programs\Eclipse\CE_relation\CEextractor\Wfrequence\txt", fname)
        WPFfp = codecs.open(WPFpath, 'w', 'utf8')
        WPFfp.write("f%04d" %(i + 1) + ':\n\n')
        WriteTXT(WPFfp, WPFdiclist[i])


def WriteTXT(WPFfp, curWPFdic):
    W_Fdic = sorted(curWPFdic.W_Fdic.iteritems(), key=lambda asd: asd[1], reverse=True)
    W_Pdic = curWPFdic.W_Pdic
    WP_Fdic = sorted(curWPFdic.WP_Fdic.iteritems(), key=lambda asd: asd[1], reverse=True)

    WPFfp.write("W_Fdic:\n")
    i = 1
    for dic in W_Fdic:
        WPFfp.write("%-20s: %-8d" % (dic[0], dic[1]))
        if i % 4 == 0:
            WPFfp.write('\n')
        i = i + 1
    WPFfp.write('\n\n')

    WPFfp.write("WP_Fdic:\n")
    i = 1
    for dic in WP_Fdic:
        WP = [x.encode('utf8') for x in list(dic[0])]
        WPFfp.write("%-35s: %-8d" % (WP, dic[1]))
        if i % 3 == 0:
            WPFfp.write('\n')
        i = i + 1
    WPFfp.write('\n\n')

    WPFfp.write("W_Pdic:\n")
    i = 1
    for dic in W_Pdic.items():
        P = [x.encode('utf8') for x in dic[1]]
        WPFfp.write("%-20s: %-35s" % (dic[0].encode('utf8'), P))
        if i % 2 == 0:
            WPFfp.write('\n')
        i = i + 1

    WPFfp.close()


#######################################################################################
# --------------------------------- Main function ----------------------------------- #
#######################################################################################
if __name__ == "__main__":
    [ParseTreelist,WPFlist] = Build_w_pos_DIC()
    GetTotalWPFdic()
    # showWordFrequency()
