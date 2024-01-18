import math as m
def calculator(input):
    ans=[]
    c=50
    h=30
    equation=lambda d: m.sqrt((2*c*d)/h)
    for d in input:
        result=equation(d)
        final=m.floor(result)
        ans.append((final))
    return ans
input=list(map(int,input().split(",")))
print(calculator(input))