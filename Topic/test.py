
import numpy as np
import matplotlib.pyplot as plt

n_dots = 20
n_order = 3

x=np.linspace(0,1,n_dots)

print(x)
y=np.sqrt(x)+0.2*np.random.rand(n_dots)
print(y)
p=np.poly1d(np.polyfit(x,y,2))
print(np.polyfit(x,y,2))
print(p.coeffs)

t=np.linspace(0,1,200)
plt.plot(x,y,'ro',t,p(t),"-")
plt.show()