from sorting import mergesort
att_type = [True,True,False]  #check i attribute is discrete or not
att_name = {0:'Home_owner',1:'martial_status',2:'Annual_Income',3:'class_lable'}
dataset = [
    ['Yes','No','No','Yes','No','No','Yes','No','No','No' ],
    ['single','married','single','married','divorced','married','divorced','single','married','single'],
    [125,100,70,120,95,60,220,85,75,90],
    ['No','No','No','No','Yes','No','No','Yes','No','Yes']
]

lables_dict = {}
types_lables = []
list_of_att_indx = [0,1,2]
for x in  dataset[len(dataset)-1] :
    lables_dict[x] = lables_dict.get(x,0) +1 ;

types_lables = lables_dict.keys();

#print lables_dict
#print  types_lables
#dd = {}
#for x in  a :
#    dd[x] = dd.get(x,0) +1 ;
#print  dd



