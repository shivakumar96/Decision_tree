#merge sort program for sorting the attributes and class lables
#used in decision tree for sorting the continous attribute.

def merge(B,C,Att,lable_B,lable_C,lable_class) :
    p = len(B)
    q = len(C)
    i=0; j =0; k = 0;
    while i < p and j < q :
        if B[i] <= C[j] :
            Att[k] = B[i]
            lable_class[k] = lable_B[i]
            k+=1 ; i+=1
        else :
            Att[k] = C[j]
            lable_class[k] = lable_C[j]
            k+=1 ; j+=1
    if i == p :
        while j < q :
            Att[k] = C[j]
            lable_class[k] = lable_C[j]
            k+=1 ; j+=1
    else :
        while i < p :
            Att[k] = B[i]
            lable_class[k] = lable_B[i]
            k+=1 ; i+=1 ;

    return




def mergesort( Att , lable_class) :
    if(len(Att) > 1) :
        n_half = len(Att)/2
        B = Att[0:n_half]
        C = Att[n_half:]
        lable_B = lable_class[0:n_half]
        lable_C = lable_class[n_half:]
        mergesort(B,lable_B)
        mergesort(C,lable_C)
        merge(B,C,Att,lable_B,lable_C,lable_class)

    return





#to test
#a = [5,6,9,1,3,2,8,0]
#b = ["A","B","A","A","B","B","A","B"]
#print a
#print b
#mergesort(a,b)
#print a
#print b

