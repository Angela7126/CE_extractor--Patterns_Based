# -*- coding: UTF-8 -*- 
import os  
  
from nltk.parse import stanford
from nltk.tree import Tree  
  
### ---- stanford_parser java package ----  
os.environ['STANFORD_PARSER'] = r'D:\jars\stanford-parser.jar'
os.environ['STANFORD_MODELS'] = r'D:\jars\stanford-parser-3.5.2-models.jar'
### ---- JAVA_HOME path ----
java_path = r"C:\Program Files\Java\jdk1.8.0_45\bin\java.exe"
os.environ['JAVAHOME'] = java_path
### ---- initiate a parser ----
parser = stanford.StanfordParser(model_path=r"D:\jars\englishPCFG.ser.gz")

sentences = parser.raw_parse("Today cause-effect love sunshine. You too me while some book. Hello world!")

### ---- check whether a leave span index is legal ----
def checkLvsIdx(PTlst,LvsIdx,sp):
    ### ---- index should be a nonegtive number 
    if LvsIdx[0][0] < 0 or LvsIdx[0][1] < 0 or LvsIdx[1][0] < 0 or LvsIdx[1][1] < 0:
        return False
    ### ---- start_leave_index should 'before' than end_leave_index
    if LvsIdx[0][0]*sp > LvsIdx[1][0]*sp:
        return False
    if LvsIdx[0][0] == LvsIdx[1][0] and LvsIdx[0][1]*sp > LvsIdx[1][1]*sp:
        return False
    ### ---- start_leave_index and end_leave_index should be found in PTlst
    PTnum = len(PTlst)
    if LvsIdx[0][0] >= PTnum or LvsIdx[1][0] >= PTnum:
        return False
    STlen = len(PTlst[LvsIdx[0][0]].leaves())
    ETlen = len(PTlst[LvsIdx[1][0]].leaves())
    if LvsIdx[0][1] >= STlen or LvsIdx[1][1] >= ETlen:
        return False
    return True


### ---- move a leave index a step 'forward' ----
def movIdxForward(PTlst, Idx, sp):
    tempIdx = list(Idx)
    tempIdx[1] += sp
    if sp > 0 and tempIdx[1] >= len(PTlst[tempIdx[0]].leaves()):
        tempIdx[0] += 1
        tempIdx[1] = 0
    elif sp < 0 and tempIdx[1] < 0:
        tempIdx[0] -= 1
        if tempIdx[0] >= 0:
            tempIdx[1] = len(PTlst[tempIdx[0]].leaves())-1
    return tuple(tempIdx)


### ---- Find the SubPT list in PTlst that between index_span (SL, EL) ---- 
def SubPTinSpan(PTlst,SL,EL,sp):
    ### if the span is not correct, showing error "MaxPTinSpan: The leave index span is not correct!":
    if not checkLvsIdx(PTlst, [SL,EL], sp):
        raise IndexError('The Parser Tree span [SL,EL] of PTlst is not correct!')
        return None, SL, EL

    SubPTlst  = []  ### SubPTlst store the SubParserTree in span [SL,EL]
    curPTIdx = SL[0]  ### curPTIdx store the current visit ParserTree Index in ParserTree list PTlst;
    curLvsIdx = SL[1]  ### curLvsIdx store the started current Leave Index in PTlst[curPTIdx] that we need to build a subPT
    
    ### ---- if (curPTIdx,curLvsIdx) still in leaves index span (SL,EL), continue build subPT ----
    while (curPTIdx*sp < EL[0]*sp) or ((curPTIdx == EL[0]) and curLvsIdx*sp <= EL[1]*sp):
        ### curSubPT_loc: the position of curLvsIdx_th leaves in PTlst[curPTIdx]
        curSubPT_loc = list(PTlst[curPTIdx].leaf_treeposition(curLvsIdx))

        ### ---- if get curSubPT's parent -> curParentPT has no leaves beyond span [(curPTIdx,curLvsIdx),EL] ----
        ### ---- then backtrack, i.e. curSubPT = curParentPT ---- 
        while True:
            ### ---- if curSubPT_loc is empty list, means curSubPT point to the ROOT of PTlst[curPTIdx], cannot continue backtrack ----  
            if curSubPT_loc == []:  
                break
            ### ---- get curParentPT_loc: the current Parent Parser Tree location; curParentPT: the current Parent Parser Tree----
            curParentPT_loc = curSubPT_loc[0:-1]
            if curParentPT_loc == []:
                curParentPT = PTlst[curPTIdx]
            else:
                curParentPT = PTlst[curPTIdx][curParentPT_loc]

            ### ---- check whether curParentPT has child that beyond span [(curPTIdx,curLvsIdx),EL] ----
            ### ---- if such a child is not exist, continue backtrack: curSubPT_loc = curParentPT_loc ----
            
            sibIdx = curSubPT_loc[-1] - sp  ### sibIdx: the sibling index of curSubPT in curParentPT at -sp direction
            ### ---- if such a sibling is not exist ----
            if sibIdx < 0 or sibIdx >= len(curParentPT): 
                ### ---- check whether curSubPT has leaves beyond EL ----
                (tempPTIdx,tempLvsIdx) = movIdxForward(PTlst,(curPTIdx,curLvsIdx), (len(curParentPT.leaves())-1)*sp)
                if (tempPTIdx == EL[0]) and tempLvsIdx*sp > EL[1]*sp: ### if it has leaves beyond EL, stop backtracking
                    break
                else:  ### if its leaves all in span [(curPTIdx,curLvsIdx),EL], continue backtrack
                    curSubPT_loc = curParentPT_loc
                    ### ---- if such a sibling exist, then stop backtracking ----
            else:
                break
        ### ---- Get final curSubPT, add it into SubPTlst ----
        if curSubPT_loc == []:
            curSubPT = PTlst[curPTIdx]
        else:
            curSubPT = PTlst[curPTIdx][curSubPT_loc]
        SubPTlst.append(curSubPT)
        ### ---- Get next start subPT leave index (curPTIdx,curLvsIdx) ---- 
        if isinstance(curSubPT,Tree):
            (curPTIdx,curLvsIdx) = movIdxForward(PTlst,(curPTIdx,curLvsIdx), len(curSubPT.leaves())*sp)
        else:
            (curPTIdx,curLvsIdx) = movIdxForward(PTlst,(curPTIdx,curLvsIdx), sp)
            ### ---- If there is only one SubPT in SubPTlst, return it; else build a new ParserTree Tree('ROOT',subPTlst) ----
    if len(SubPTlst) == 1:
        return SubPTlst[0]
    elif sp < 0:
        return Tree('ROOT',SubPTlst[::-1])
    else:
        return Tree('ROOT',SubPTlst)


# sentPTlst = [];
for sentence in sentences:
    sentence.draw()
    #   sentPTlst.append(sentence.next());
# SubPT = SubPTinSpan(sentPTlst, (0,11), (1,12), 1);
# SubPT.draw();
# SubPT = parser.raw_parse(' '.join(SubPT.leaves())).next();
# SubPT.draw();
    
    #print sentence
#     while isinstance(sentence, Tree) and len(sentence) == 1: 
#             sentence = sentence[0];
#     sentence[:] = sentence[::-1];
    #print sentence.pos();
    #for subPT in sentence[0]:
    #    print subPT;
    #SubPT = SubPTinSpan([sentence], (0,12), (0,0), -1);
    #print SubPT
#     for subPT in SubPTlst:
#         print subPT;
#         print
#    