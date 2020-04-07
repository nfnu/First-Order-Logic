# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 11:58:46 2019

@author: nisha
"""
import copy
import time
from collections import OrderedDict 

st_count=0
st_mult=1

class Predicate:
  def __init__(self, name, arguments, flag):
    self.name = name
    self.arg = arguments
    self.flag = flag

def ReadInput(text):
    for i in range(int(text[0])):
        flag=1
        name=text[1+i].split("(")[0].strip()
        arguments=text[1+i].split("(")[1].split(")")[0].split(",")
        arguments = [x.strip(' ') for x in arguments]
        arguments=StandardizeVariables_Query(arguments)
        if name[0]!="~":
            flag=0
        else:
            name=name[1:]
        Query[tuple([Predicate(name.strip(),arguments,flag)])]=1
        
    kb_count=int(text[2+i])
    for i in range(int(text[0])+2,int(text[0])+2+kb_count,1):
        t=text[i]
        rule=[]
        sentence = t.split("=>")
        unique_args=[]
        if "=>" in t:
            lhs = sentence[0].split("&")
            for pred in lhs:
                flag=1
                name=pred.split("(")[0].strip()
                arguments=pred.split("(")[1].split(")")[0].split(",")
                arguments = [x.strip(' ') for x in arguments]
                unique_args+=list(set(arguments))
                if name[0]!="~":
                    flag=0
                else:
                    name=name[1:]
                rule.append(Predicate(name,arguments,flag))                
            rhs = sentence[1].split("&")
            for pred in rhs:
                rule_rhs=[]
                unique_args_rhs=[]
                flag=1
                name=pred.split("(")[0].strip()
                arguments=pred.split("(")[1].split(")")[0].split(",")
                arguments = [x.strip(' ') for x in arguments]
                unique_args_rhs=unique_args+list(set(arguments))
                if name[0]=="~":
                    flag=0
                    name=name[1:]
                rule_rhs.append(Predicate(name,arguments,flag))
                new_rule=StandardizeVariables_KB(list(set(unique_args_rhs)),rule+rule_rhs)
                KB[tuple(new_rule)]=1
                #PrintPred(tuple(new_rule))
        else:
            lhs = sentence[0].split("&")
            for pred in lhs:
                flag=1
                name=pred.split("(")[0].strip()
                arguments=pred.split("(")[1].split(")")[0].split(",")
                arguments = [x.strip(' ') for x in arguments]
                unique_args=list(set(arguments))
                if name[0]=="~":
                    flag=0
                    name=name[1:]
                rule=[Predicate(name,arguments,flag)]  
                new_rule=StandardizeVariables_KB(list(set(unique_args)),rule)
                KB[tuple(new_rule)]=1
                singleKB[tuple([new_rule[0].name]+new_rule[0].arg)]=new_rule[0].flag
                #PrintPred(tuple(new_rule))

def StandardizeVariables_Query(args):
    new_arg={}
    global st_count,st_mult
    if st_count==26:
        st_count=0
        st_mult+=1
    for i in range(len(args)):
        if not(args[i][0]>='A' and args[i][0]<='Z'):
            if args[i] not in new_arg:
                new_arg[args[i]]=ch[st_count]*st_mult
                st_count+=1
                if st_count==26:
                    st_count=0
                    st_mult+=1
    newrule=[]
    for i in range(len(args)):
        if args[i][0]>='A' and args[i][0]<='Z':
            newrule.append(args[i])
        else:
            newrule.append(new_arg[args[i]])
            
    return newrule

def StandardizeVariables_KB(args,rule):
    new_arg={}
    global st_count,st_mult
    if st_count==26:
        st_count=0
        st_mult+=1
    for i in range(len(args)):
        if not(args[i][0]>='A' and args[i][0]<='Z'):
            if args[i] not in new_arg:
                new_arg[args[i]]=ch[st_count]*st_mult
                st_count+=1
                if st_count==26:
                    st_count=0
                    st_mult+=1
    newrule=[]
    for i in rule:
        j=copy.deepcopy(i)
        for k in range(len(j.arg)):
            if j.arg[k] in new_arg:
                j.arg[k]=new_arg[j.arg[k]]
        newrule.append(j)
    return newrule
'''                
def PrintPred(preds):
    for i in preds:
        print(i.name,i.arg,i.flag," ",end='')
    print()
'''
def Pred(li):
    li1=[]
    for i in li:
        li1+=[i.name]+i.arg+[i.flag]
    return li1

def CheckPred(li):
    li1=[]
    args=[]
    for i in li:
        args+=i.arg
    args=list(set(args))
    new_arg={}
    ch_count=0
    ch_mult=1
    for i in range(len(args)):
        if not(args[i][0]>='A' and args[i][0]<='Z'):
            if args[i] not in new_arg:
                new_arg[args[i]]=ch[ch_count]*ch_mult
                ch_count+=1
                if ch_count==26:
                    ch_count=0
                    ch_mult+=1
    for i in li:
        li1+=[i.name]
        for j in i.arg:
            if j[0]>='a' and j[0]<='z' and j in new_arg:
                li1+=[new_arg[j]]
            else:
                li1+=[j]
        li1+=[i.flag]
    return li1


def EquateArgs(i1,i2):
    i=0
    li1={}
    li2={}
    #print(i1.name,i1.arg)
    #print(i2.name,i2.arg)
    while i<len(i1.arg):
        if not(i1.arg[i][0]>='a' and i1.arg[i][0]<='z') and i2.arg[i][0]>='a' and i2.arg[i][0]<='z':
            
            if i2.arg[i] not in li1:
                li1[i2.arg[i]]=i1.arg[i]
            else:
                if not(li1[i2.arg[i]][0]>='a' and li1[i2.arg[i]][0]<='z') and li1[i2.arg[i]]!=i1.arg[i]:
                    #print(li1,li2)
                    return False,[],[]
            
            #li1[i2.arg[i]]=i1.arg[i]
        elif i1.arg[i][0]>='a' and i1.arg[i][0]<='z' and not(i2.arg[i][0]>='a' and i2.arg[i][0]<='z'):
            
            if i1.arg[i] not in li2:
                li2[i1.arg[i]]=i2.arg[i]
            else:
                if not(li2[i1.arg[i]][0]>='a' and li2[i1.arg[i]][0]<='z') and li2[i1.arg[i]]!=i2.arg[i]:
                    #print(li1,li2)
                    return False,[],[]
                
        elif not(i1.arg[i][0]>='a' and i1.arg[i][0]<='z' and i2.arg[i][0]>='a' and i2.arg[i][0]<='z') and i1.arg[i]!=i2.arg[i]:
            #print(li1,li2)
            return False,[],[]
        
        elif i1.arg[i][0]>='a' and i1.arg[i][0]<='z' and i2.arg[i][0]>='a' and i2.arg[i][0]<='z':
            if i1.arg[i] in li2 and i2.arg[i] in li1:
                if li2[i1.arg[i]]!=li1[i2.arg[i]]:
                    return False,[],[]
            elif i1.arg[i] in li2 and i2.arg[i] not in li1:
                li1[i2.arg[i]]=li2[i1.arg[i]]
            elif i1.arg[i] not in li2 and i2.arg[i] in li1:
                li2[i1.arg[i]]=li1[i2.arg[i]]
        
        i+=1   
    #print(li1,li2)
    i=0
    while i<len(i1.arg):
        
        if i1.arg[i] in li2: 
            if i2.arg[i] not in li1:
                if (i2.arg[i][0]>='a' and i2.arg[i][0]<='z') and not(li2[i1.arg[i]][0]>='a' and li2[i1.arg[i]][0]<='z'):
                    li1[i2.arg[i]]=li2[i1.arg[i]]
                elif not(i2.arg[i][0]>='a' and i2.arg[i][0]<='z') and i2.arg[i]!=li2[i1.arg[i]]:
                    return False,[],[]
            elif li1[i2.arg[i]]!=li2[i1.arg[i]]:
                return False,[],[]
        elif (i1.arg[i][0]>='a' and i1.arg[i][0]<='z'):
            if i2.arg[i] in li1:
                li2[i1.arg[i]]=li1[i2.arg[i]]
        elif not(i1.arg[i][0]>='a' and i1.arg[i][0]<='z'):
            if i2.arg[i] in li1 and i1.arg[i]!=li1[i2.arg[i]]:
                return False,[],[]
            elif i2.arg[i] not in li1:
                li1[i2.arg[i]]=i1.arg[i]
                
        i+=1
    #print(li1,li2)
    i=0
    a=copy.deepcopy(li1)
    b=copy.deepcopy(li2)
    flag=0
    while i<len(i1.arg):
    
        if i1.arg[i] in li2: 
            if i2.arg[i] not in li1:
                if (i2.arg[i][0]>='a' and i2.arg[i][0]<='z') and not(li2[i1.arg[i]][0]>='a' and li2[i1.arg[i]][0]<='z'):
                    li1[i2.arg[i]]=li2[i1.arg[i]]
                elif i2.arg[i]!=li2[i1.arg[i]]:
                    flag=1
                    break
                    #return False,[],[]
            elif li1[i2.arg[i]]!=li2[i1.arg[i]]:
                flag=1
                break
                #return False,[],[]
        elif (i1.arg[i][0]>='a' and i1.arg[i][0]<='z'):
            if i2.arg[i] in li1:
                li2[i1.arg[i]]=li1[i2.arg[i]]
            else:
                li2[i1.arg[i]]=i2.arg[i]
        #print(i,li1,li2)
        i+=1

    if flag==1:
        li1=a
        li2=b
        i=0
        while i<len(i1.arg):
    
            if i2.arg[i] in li1: 
                if i1.arg[i] not in li2:
                    if (i1.arg[i][0]>='a' and i1.arg[i][0]<='z') and not(li1[i2.arg[i]][0]>='a' and li1[i2.arg[i]][0]<='z'):
                        li2[i1.arg[i]]=li1[i2.arg[i]]
                    elif i1.arg[i]!=li1[i2.arg[i]]:
                        #flag=1
                        #break
                        return False,[],[]
                elif li2[i1.arg[i]]!=li1[i2.arg[i]]:
                    #flag=1
                    #break
                    return False,[],[]
            elif (i2.arg[i][0]>='a' and i2.arg[i][0]<='z'):
                if i1.arg[i] in li2:
                    li1[i2.arg[i]]=li2[i1.arg[i]]
                else:
                    li1[i2.arg[i]]=i1.arg[i]
            #print(i,li1,li2)
            i+=1
    return True,li1,li2
    
def FOLFn(stack,q,val,stack_dict):
    newKB=copy.deepcopy(KB)
    newKB[q]=1
    kb_list=list(newKB)
    resolved={}
    pred_resolved_upto={}
    t0 = time.time()
    while stack:
        z=stack.pop(0)
        s=z[0]
        k_val=z[1]
        done_pred=tuple(Pred(s))
        done_k_pred=len(kb_list)
        start=0
        if done_pred in pred_resolved_upto:
            start=pred_resolved_upto[done_pred]
        #PrintPred(s)
        if start<len(kb_list):
            for knowledge in range(start,len(kb_list)):
                p_pred=tuple(Pred(s)+[knowledge])
                if knowledge!=k_val and p_pred not in resolved:
                    for i in s:
                        for k in kb_list[knowledge]:
                            list1=[]
                            putin=0
                            if i.name==k.name and i.flag!=k.flag:
                                #print("Hi")
                                flag,li1,li2=EquateArgs(i,k)
                                if flag:
                                    '''
                                    print("Query ",end='')
                                    PrintPred(s)
                                    print("Unify with ",end='')
                                    PrintPred(kb_list[knowledge])
                                    '''
                                    unified={}
                                    for j in s:
                                        if i!=j:
                                            p=copy.deepcopy(j)
                                            p.arg=[li2[x] if (x in li2 and x[0]>='a' and x[0]<='z') else x for x in j.arg]
                                            if tuple([p.name]+p.arg) not in unified:
                                                unified[tuple([p.name]+p.arg)]=p.flag
                                                list1.append(p)
                                            elif unified[tuple([p.name]+p.arg)]!=p.flag:
                                                putin=1
                                                break                                
                                    for j in kb_list[knowledge]:
                                        if j!=k:
                                            p=copy.deepcopy(j)
                                            p.arg=[li1[x] if (x in li1 and x[0]>='a' and x[0]<='z')  else x for x in j.arg]
                                            if tuple([p.name]+p.arg) not in unified:
                                                unified[tuple([p.name]+p.arg)]=p.flag
                                                list1.append(p)
                                            elif unified[tuple([p.name]+p.arg)]!=p.flag:
                                                putin=1
                                                break
                                    #print(unified)
                                    len_list1=len(list1)
                                    ind=0
                                    while ind<len_list1 and putin==0:
                                        if tuple([list1[ind].name]+list1[ind].arg) in single_KB and single_KB[tuple([list1[ind].name]+list1[ind].arg)]!=list1[ind].flag:
                                            list1.pop(ind)
                                            len_list1-=1
                                        else:
                                            ind+=1
                                    if not list1 and putin==0:
                                        #print("True ",  val.name,val.arg,time.time()-t0,len(newKB))
                                        return "TRUE"
                                    if (len(list1)==1 and list1[0].name==val.name and list1[0].arg==val.arg and putin==0):
                                        if list1[0].flag!=val.flag:
                                            #PrintPred(tuple(list1))
                                            #print("True ", val.name,val.arg,time.time()-t0,len(newKB))
                                            return "TRUE" 
                                    if len(list1)==1 and putin==0:
                                        single_KB[tuple([list1[0].name]+list1[0].arg)]=list1[0].flag
                                        #print(single_KB)
                                    if (tuple(CheckPred(list1))) not in stack_dict and putin==0:
                                        if len(kb_list[knowledge])!=1:
                                            stack_dict[tuple(CheckPred(list1))]=knowledge
                                            stack.append((tuple(list1),knowledge))
                                        else:
                                            stack_dict[tuple(CheckPred(list1))]=knowledge
                                            stack.append((tuple(list1),-1))
                                        #PrintPred(tuple(list1))
                                        #print()
                                        newKB[tuple(list1)]=1
                                        resolved[p_pred]=1
                                    #else:
                                        #print("Didn't Resolve.")
                                        #PrintPred(tuple(list1))
                                    if len(newKB)>=10000:
                                        #print("False (timeout)", time.time()-t0)
                                        return "FALSE"
                                        
                                        
            pred_resolved_upto[done_pred]=done_k_pred
        
    #print("False ",  val.name,val.arg,time.time()-t0)
    return "FALSE"

#t1=time.time()
KB={}
single_KB={}
singleKB={}
Query=OrderedDict()
ch=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
path = "input.txt"
f= open("output.txt","w+")
input_file = open(path,'r')
text = input_file.read().split("\n")
ReadInput(text)   
count_query=0
for q in Query:
    single_KB=copy.deepcopy(singleKB)
    stack=[(q,-1)]
    stack_dict={}
    stack_dict[tuple(CheckPred(q))]=-1
    p=Predicate(q[0].name,q[0].arg,q[0].flag)
    val=FOLFn(stack,q,p,stack_dict)
    f.write(val)
    if count_query!=int(text[0])-1:
        f.write("\n")
    count_query+=1

f.close()
#print(time.time()-t1)