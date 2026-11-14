from fractions import Fraction as F
import random
w=list(map(F,['0.227027','0.1945946','0.1216216','0.054054','0.016216']))
old=[(F(0),w[0])]+[(sign*F(3*i,2),w[i]) for i in range(1,5) for sign in [-1,1]]
a=w[2]+w[3]/2;b=w[3]/2+w[4]
new=[(F(0),w[0])]+[(sign*d,k) for d,k in [(F(3,2),w[1]),(F(3)+w[3]/2/a,a),(F(5)+w[4]/b,b)] for sign in [-1,1]]
def sample(v,x):
 lo=x.numerator//x.denominator;t=x-lo
 return v[max(0,min(len(v)-1,lo))]*(1-t)+v[max(0,min(len(v)-1,lo+1))]*t
random.seed(42);cases=0
for n in [1,2,3,4,5,6,7,8,17,64]:
 for rep in range(20):
  v=[F(random.randrange(0,100001),10000) for i in range(n)]
  for x in range(n):
   before=sum(k*sample(v,x+d) for d,k in old);after=sum(k*sample(v,x+d) for d,k in new)
   assert before==after;cases+=1
print('exact rational clamped cases:',cases)
print('positive grouped weight/offset:',[(str(k),str(d),float(d)) for d,k in [(F(3,2),w[1]),(F(3)+w[3]/2/a,a),(F(5)+w[4]/b,b)]])
print('sum kernel:',sum(k for d,k in old),'do not renormalize')
