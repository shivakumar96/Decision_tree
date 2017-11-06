from dataset import dataset,att_name,att_type,lables_dict,types_lables,list_of_att_indx
from sorting import mergesort

class Question :
   def __init__(self,indx =-1,value=[],discrete=True):
       self.indx = indx
       self.value = value
       self.discrete = discrete

class Leafnode :
    def __init__(self,label):
        #lable of the leaf node.
        self.lable = label

class DecisionNode :
    def __init__(self):
        #these are the list for multi way splitting
        self.testQuestion = None ;
        self.nextPointers = [] ;


def discreteGini(column,itsLabels) :
    allvales =  {}
    for x in column :
        allvales[x] = {}
        for y in types_lables :
            allvales[x][y] = 0
    i = 0
    while i < len(column) :
        allvales[column[i]][itsLabels[i]] = allvales[column[i]].get(itsLabels[i],0) + 1
        i = i+1

    dis_in_col = {}
    dis_all = {}

    for x in allvales :
        dis_all[x] = sum(allvales[x].values())

    for x in allvales :
        sum_x = 0.0
        if sum(allvales[x].values()) != 0 :
            for y in allvales[x] :
                sum_x = sum_x + pow(float(allvales[x][y])/float(sum(allvales[x].values())),2)
            sum_x = 1 - sum_x
        dis_in_col[x] = sum_x

    for x in dis_in_col :
        dis_in_col[x] = dis_in_col[x]*(float(dis_all[x])/float(len(column)))

    giniVal = round(sum(dis_in_col.values()),4)
    #print allvales
    #print  dis_all
    #print dis_in_col
    #print giniVal
    split_val = dis_in_col.keys()
    return  giniVal,split_val

def continousGini(column,itsLabel) :
    a = column[:]
    l = itsLabel[:]
    mergesort(a,l)
    avg_gini =  {}
    avg_gini[a[0]] = {}
    i = 0
    #print a
    while i < len(a) -1:
        avg_gini[ int((a[i]+a[i+1])/2)] = {}
        i = i+1

    avg_gini[a[len(a)-1]] = {}

    avg_gini_cont = {}

    for x in avg_gini :
        avg_gini_cont[x] = {}
        avg_gini_cont[x]['yes'] = 0
        avg_gini_cont[x]['no'] = 0
        avg_gini[x]['yes'] = 0
        avg_gini[x]['no'] = 0

        for y in avg_gini[x] :
            avg_gini[x][y] = {}
            for z in types_lables :
                avg_gini[x][y][z] = 0

    i = 0
    while i < len(a) :
        for x in avg_gini :
            if  a[i] <= x :
                avg_gini[x]['yes'][l[i]] = avg_gini[x]['yes'].get(l[i],0) + 1
            else:
                avg_gini[x]['no'][l[i]] = avg_gini[x]['no'].get(l[i],0) + 1
        i = i+ 1

    for x in avg_gini :
        avg_gini_cont[x]['yes'] = sum(avg_gini[x]['yes'].values())
        avg_gini_cont[x]['no'] = sum(avg_gini[x]['no'].values())

    avg_gini_val = {}



    for x in avg_gini :
        yes_dic = avg_gini[x]['yes']
        no_dic = avg_gini[x]['no']
        yes_tot = 0.0
        no_tot = 0.0
        for y in types_lables :
            yes_tot+= yes_dic[y]
            no_tot+=no_dic[y]
        yes_psum = 0.0
        no_psum = 0.0
        for y in types_lables :
            if yes_tot != 0 :
                yes_psum+= pow(float(yes_dic[y])/float(yes_tot),2)
            if no_tot != 0 :
                no_psum+= pow(float(no_dic[y])/float(no_tot),2)

        if yes_psum != 0 :
            yes_psum = round(1.0- yes_psum,4)
        if no_psum != 0 :
            no_psum = round(1.0 - no_psum,4)
        total_sum = 0.0
        total_sum = yes_psum*(float(avg_gini_cont[x]['yes'])/(float(len(a)))) + \
                    no_psum*(float(avg_gini_cont[x]['no'])/(float(len(a))))
        avg_gini_val[x] = round(total_sum,4)
    #print avg_gini_cont
    #print  avg_gini
    #print  avg_gini_val
    #print len(avg_gini)
    min_gini = min(avg_gini_val.values())
    split_value = avg_gini_val.keys()[avg_gini_val.values().index(min_gini)]
    #print min_gini,split_value
    return min_gini,split_value

def gini(Minidata , list_att_indx) :
    i = 0
    giniOfAll = {}
    att_split = {}
    while i < len(list_att_indx)  :
        if att_type[list_att_indx[i]] :
            giniOfAll[list_att_indx[i]], att_split[list_att_indx[i]] = discreteGini(Minidata[list_att_indx[i]],Minidata[len(Minidata)-1])
        else:
            giniOfAll[list_att_indx[i]] , att_split[list_att_indx[i]] = \
                continousGini(Minidata[list_att_indx[i]],Minidata[len(Minidata) -1])
        i = i+1
    #print  giniOfAll
    #print  att_split
    return giniOfAll,att_split

# stopping conditions are
# 1 . no record is prsent
# 2. if all the attributes have same value except the labels
# 3. if all the values in the label are same
def stop_condition (dataset,list_att_indx) :
    if len(list_att_indx) == 0 :
        return True
    if dataset == None or len(dataset) == 0 :
        return True
    lab = {}
    for x in dataset[len(dataset) -1] :
        lab[x] = lab.get(x,0)+1
    if( len(lab.keys()) == 1) :
        return True
    i = 0 ;
    Flag = True
    while i < len(dataset[0]) :
        j = i + 1
        while j < len(dataset[0]) :
            k = 0
            while k < len(dataset) :
                if dataset[k][i] != dataset[k][j] :
                    Flag = False
                    break
                k+=1
            j+=1
        if  not Flag :
            break

    if Flag :
        return True

    return False

def best_split_cond(dataset,list_attribute) :
    #print dataset
    #print list_attribute
    gini_values,split_cond = gini(dataset,list_attribute)
    #print gini_values
    val = min(gini_values.values())
    indx = gini_values.keys()[gini_values.values().index(val)]
    quest = split_cond[indx]
    disc = att_type[indx]

    return  indx,quest,disc


def split_data (dataset,indx, val) :
    #print "-----------------------------------------\n"
    #print indx,"----",val,"\n-------------------------------------\n"
    #print dataset
    #print "-----------------------------------------\n\n"
    s_data = []
    new_dataset = []
    i = 0
    while i < len(dataset) :
        new_dataset.append([])
        i+=1
    #print len(new_dataset)
    if att_type[indx] :
        i = 0
        k =0
        while i < len(dataset[0]) :
            if dataset[indx][i] == val :
                j = 0
                while j < len(dataset) :
                    new_dataset[j].insert(k,dataset[j][i])
                    j+=1

                k+=1
            i+=1
        s_data.append(new_dataset)
    else:
        dtrue = []
        dfalse = []
        i= 0
        while i < len(dataset) :
            dtrue.append([])
            dfalse.append([])
            i+=1
        i = 0
        k =0
        while i < len(dataset[0]) :
            if dataset[indx][i] <= val :
                j = 0
                while j < len(dataset) :
                    dtrue[j].insert(k,dataset[j][i])
                    j+=1
                k+=1
            else:
                j = 0
                while j < len(dataset) :
                    dfalse[j].insert(k,dataset[j][i])
                    j+=1
                k+=1
            i+=1
        s_data.append(dtrue)
        s_data.append(dfalse)

    #print s_data
    return s_data

def classify(Minidataset,attributes_indx) :
    label = {}
    for x in Minidataset[len(dataset) -1] :
        label[x] = label.get(x,0) + 1
    total_length = float(sum(label.values()))
    for x in label :
        label[x] = round(float(label[x])/total_length,4)
    return label ;


def createTree(dataset,list_attributes_indx):
    if stop_condition(dataset,list_attributes_indx) :
        leaflabel = classify(dataset,list_attributes_indx)
        leaf = Leafnode(leaflabel)
        return  leaf

    else:
        Root = DecisionNode()
        Aindx,split_val,desc = best_split_cond(dataset,list_attributes_indx)
        Root.testQuestion = Question(Aindx,split_val,desc)
        #list_attributes_indx.remove(Aindx)
        new_list_indx = list_attributes_indx[:]
        new_list_indx.remove(Aindx)
        if type(split_val) == int or type(split_val) == float :
            splitted_data = split_data(dataset,Aindx,split_val)
            child1 = createTree(splitted_data[0],new_list_indx)
            Root.nextPointers.append(child1)
            child2 = createTree(splitted_data[1],new_list_indx)
            Root.nextPointers.append(child2)
        else:
            for x in split_val :
                splitted_data = split_data(dataset,Aindx,x)
                child = createTree(splitted_data[0],new_list_indx)
                Root.nextPointers.append(child)

        return Root

#discreteGini(dataset[0],dataset[len(dataset)-1])



def print_tree(Root) :
    if Root.__class__ == DecisionNode:
        print Root.testQuestion.__dict__
        for x in Root.nextPointers  :
            print_tree(x)
    else:
        print Root.__dict__


def testARecord(Root,row) :
    if Root.__class__ == DecisionNode :
        tindx = Root.testQuestion.indx
        if Root.testQuestion.discrete :
            pointerindx = Root.testQuestion.value.index(row[tindx])
            testARecord(Root.nextPointers[pointerindx],row)
        else :
            if row[tindx] <= Root.testQuestion.value :
                testARecord(Root.nextPointers[0],row)
            else:
                testARecord(Root.nextPointers[1],row)
    else :
        print "-----------------------------\n"
        print "predicted label : ",Root.__dict__
        print " Actual label   : ",row[len(row) -1]
        print "-----------------------------\n"

def testAlldata(Root,testdatset) :
    i = 0
    while i< len(testdatset[0]) :
        row = []
        j = 0
        while j < len(testdatset) :
            row.insert(j,testdatset[j][i])
            j+=1
        i+=1
        testARecord(Root,row)


Root = createTree(dataset,list_of_att_indx)

#print_tree(Root)

testAlldata(Root,dataset)


