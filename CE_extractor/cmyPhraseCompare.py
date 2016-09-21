# -*- coding: UTF-8 -*- 

#######################################################################################
#--------------------------------- Function Introduce --------------------------------#
#######################################################################################
# This functions set not used in CE_relation project 
# This functions set intends to:
# 1. Using Standford_parser to Parse the text of Abstract, Conclusion, CEsets, and forming phrase
# 2. compare the phrase n-gram between CEsets and  Abstract or Conclusion or A+C


#######################################################################################
#---------------------------------- Global variable ----------------------------------#
#######################################################################################
import os
import nltk
import re
import string
import xlwt,xlrd
import pyodbc
from cmyToolkit import *
from cmyWordsCompare import *
from cmyPreprocess import *
from nltk.parse import stanford
#--------- set some folder path ------------------
dbfile = os.path.join(os.getcwd(),'CErelation.accdb')
corpdir = os.path.join(os.getcwd(),"Corpus","TXT")
pkdir = os.path.join(os.getcwd(),"PK")
###---- stanford_parser java package ----  
os.environ['STANFORD_PARSER'] = 'E:/jars/stanford-parser.jar'  
os.environ['STANFORD_MODELS'] = 'E:/jars/stanford-parser-3.5.2-models.jar'  
###---- JAVA_HOME path ----
java_path = "E:\Program Files\Java\jdk1.8.0_45\bin\java.exe"  
os.environ['JAVAHOME'] = java_path  
###---- initiate a parser ---- 
parser = stanford.StanfordParser(model_path="E:\jars\englishPCFG.ser.gz")  

#######################################################################################
#-------------------------------------- Classes --------------------------------------#
#######################################################################################
class FPhraseSeq:
    def __init__(self,ftag,absphrase,concphrase,cephrase):
        self.Ftag = ftag
        self.AbsP = absphrase
        self.ConcP = concphrase
        self.CEP = cephrase
        
class FPhraseDic:
    def __init__(self,ftag,abspdic,concpdic,acpdic,cepdic):
        self.Ftag = ftag
        self.AbsPdic = abspdic
        self.ConcPdic = concpdic
        self.A_CPDic = acpdic
        self.CEPDic = cepdic
        
class CoPhrase:
    def __init__(self,fphrasedic,OnAbs,Abs2CE,OnConc,Conc2CE,OnAC,AC2CE,rate2Abs,rate2Conc,rate2AC,componabs,componconc,componac):
        self.FPDic = fphrasedic
        self.OnAbs = OnAbs
        self.OnConc = OnConc
        self.OnAC = OnAC
        self.Abs2CE = Abs2CE
        self.Conc2CE = Conc2CE
        self.AC2CE = AC2CE
        self.rate2Abs = rate2Abs
        self.rate2Conc = rate2Conc
        self.rate2AC = rate2AC
        self.ComPOnAbs = componabs
        self.ComPOnConc = componconc
        self.ComPOnAC = componac


def GetPhraseSeq(ftag):
    AbsText = ReadDB_AbsText(ftag)
    ConcText = ReadDB_ConcText(ftag)
    CE_A_Text,CE_B_Text = ReadDB_CEText(ftag)
    
#######################################################################################
#---------------------------------- Main function ------------------------------------#
#######################################################################################         
if __name__ == "__main__":
    GetPhraseSeq("f0002")
    
           
