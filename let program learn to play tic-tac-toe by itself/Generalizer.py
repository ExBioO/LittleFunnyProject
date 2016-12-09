"""
feed in m pairs of <x=(1,x1,x2,x3,x4,x5,x6), s>
return a vector a = (a0,a1,a2,a3,a4,a5,a6)
so that x*a approximate s
"""
import numpy as np

def generalizer1(a, data):
    """ linear regression """
    m = np.size(data, 0)
    X = np.vstack([np.ones(m), data[:,0:-1].T]).T
    Y = data[:,-1]
    a = np.linalg.lstsq(X, Y)[0]
    return a

def generalizer2(a, data, ratio = 0.01):
    """ stochastic gradient desent """
    for sample in data:
        x = [1]+list(sample[:-1])
        a = np.add(
            a, ratio*np.dot(
                sample[-1]-np.dot(x, a), x
                )
            )
    return a
    
def test():
    from random import gauss, shuffle
    from time import clock
    n = 10000
    a = np.array([1, 0.5])
    x = np.linspace(1,10,n)
    y = np.dot(np.vstack([np.ones(n), x]).T, a)
    y += np.array([gauss(0,1) for i in range(n)])
    data = list(np.vstack([x, y]).T)
    shuffle(data)
    data = np.vstack(data)
    t1 = clock()
    a2 = generalizer1(data)
    print(a2)
    t2 = clock()
    a3 = generalizer2([0,0], data)
    print(a3)
    t3 = clock()
    print("g1 get %f with %fs" 
        % (np.mean((a-a2)**2)**0.5, t2-t1))
    print("g2 get %f with %fs" 
        % (np.mean((a-a3)**2)**0.5, t3-t2))
        
if __name__ == '__main__':
    test()