def dict_manupulation(input):
    dict={}
    for num in range(1,input+1):
        dict[num]=num*num
    return dict

input=int(input())
print(dict_manupulation(input))
