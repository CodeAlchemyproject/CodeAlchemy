n=int(input())
t=0
for i in range(2,n+1):
    t=(t+2)%i
print(t+1)  