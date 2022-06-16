import random, os

def split( src, shuffle=True, train=0.55, val=0.25):
    full_list = os.listdir(src + "/images") 

    n_total = len(full_list)
    offset = int(n_total * train)
    offset2 = int(n_total * val)
    if n_total==0 or offset<1:
        return [],full_list
    if shuffle:
        random.shuffle(full_list)

    sublist = full_list[:offset]
    with open( "src/MergedLabels/train.txt" , "w") as f:
        for ii in sublist:
            f.write( "src/MergedLabels/images/" + ii + "\n")  
    sublist = full_list[offset: offset+offset2 ] 
    with open( "src/MergedLabels/eval.txt" , "w") as f:
        for ii in sublist:
            f.write( "src/MergedLabels/images/" + ii + "\n")  
    sublist = full_list[ offset+offset2  :] 
    with open( "src/MergedLabels/test.txt" , "w") as f:
        for ii in sublist:
            f.write( "src/MergedLabels/images/" + ii + "\n") 
    print("MergedLabels split OK !")



    sublist = full_list[:offset]
    with open( "src/MultiLabels/train.txt" , "w") as f:
        for ii in sublist:
            f.write( "src/MultiLabels/images/" + ii + "\n")  
    sublist = full_list[offset: offset+offset2 ] 
    with open( "src/MultiLabels/eval.txt" , "w") as f:
        for ii in sublist:
            f.write( "src/MultiLabels/images/" + ii + "\n")  
    sublist = full_list[ offset+offset2  :] 
    with open( "src/MultiLabels/test.txt" , "w") as f:
        for ii in sublist:
            f.write( "src/MultiLabels/images/" + ii + "\n") 
    print("MultiLabels split OK !") 

    return


split( os.getcwd() )