import math
import numpy as np
import matplotlib.pyplot as plt
import sys
#import time
from random import random

miu0 = 4*np.pi*10**-7
sign = lambda x: 1 if x>=0 else -1
coth = lambda x: (math.cosh(x)/math.sinh(x)) if 0<np.abs(x)<=10 else np.inf if x==0 else 1.0*sign(x)

class JAModel():
    a, k, alpha, c, Ms = 0.0,0.0,0.0,0.0,0.0
    scale = np.array([10**3,10**3,10**-4,10**-2,10**3])
    Ht, Mt = 0.0, 0.0

    def __init__(self, theta=None):
        """
        if inner parameters a, k, alpha, c, Ms are known, load them
         into model as an iterable list:
        >>> theta = [a, k, alpha, c, Ms]
        >>> material = JAModel(theta)
        otherwise:
        >>> material = JAModel()
        """
        self.a, self.k, self.alpha, self.c, self.Ms = (
            theta or 5*self.scale*np.array([random() for i in range(5)])
        )
        
    def __str__(self):
        return("a:\t%f\nk:\t%f\nalpha:\t%f\nc:\t%f\nMs:\t%f\n" % 
            (self.a,self.k,self.alpha,self.c,self.Ms))
    def __repr__(self):
        return self.__str__()
        
    def startPoint(self, H,M):
        """
        By default, start point reside at zero point. Change it by calling:
        >>> metal.startPoint(H, M)
        """
        self.Ht, self.M = H, M
    def paraScale(self, scale):
        """
        Choose approperate model parameters scale for the physical dimension 
        you are using.
        ea. by default the scale of a, k, alpha, c, Ms is:
        >>> material.scale
        np.array([10**3,10**3,10**-4,10**-2,10**4])
        # change scale by calling
        >>> material.paraScale([the scale you choose])
        """
        self.scale = np.array(scale)
        self.__init__()
        
    def _Man(self, H, M, a, k, alpha, c, Ms): 
        return(0 if H==0 and M==0 else
            Ms*(coth((H+alpha*M)/a)-a/(H+alpha*M))
        )
    def _DManHe(self, H, M, a, k, alpha, c, Ms):
        return(Ms/a if H==0 and M==0 else
            (Ms/a)*(1-coth((H+alpha*M)/a)**2+(a/(H+alpha*M))**2)
        )
    def _f(self, Ht, Mt, H, a, k, alpha, c, Ms):
        fMan = self._Man(Ht, Mt, a, k, alpha, c, Ms)
        fDManHe = self._DManHe(Ht, Mt, a, k, alpha, c, Ms)
        return (
            ((fMan-Mt)/(k*sign(H-Ht)-alpha*(fMan-Mt)/(1-c))+c*fDManHe)
            *(1/(1-alpha*c*fDManHe))
        )   
    def _predict(self, Ht, Mt, H, a, k, alpha, c, Ms):
        return Mt+self._f(Ht, Mt, H, a, k, alpha, c, Ms)*(H-Ht)
        
    def fit(self, H_data, M_data, 
            step = 0.1, k = 100, iterate = 20, draw = False, autoscale = True):
        """
        Back-propagation through time algorithm
        Expermiental data is depicted with time interval t(ms), set model to \
        fit data by typing:
        >>> material.fit(H_data, M_data)
        if you are not satisfied with the result, you could consider to change\
        the following option to increase the fiting result:(ps.result of last \
        fit proccess remain effective)
        \tstep:\tcontrol speed of fiting, the smaller the step is, the slower \
        the fiting will perform but more accurate the result could be.
        \titerate:\tcontrol how many time the training data will be used.
        \tdraw:\tit's False by default, if setted to be true, a image of \
        training data M-t and predicted M-t will be drawn for every iteration.
        \tautoscale:\tcompute search dimension automatically if set True(\
        default), if set to False, you need to set it by yourself by \
        calling JAModel.paraScale([scale you set]).
        """
        if autoscale is True:
            hmax = max(H_data)
            mmax = max(M_data)
            self.paraScale([hmax/10.0,hmax/10.0,0.01*hmax/mmax,0.1,0.1*mmax])
        step_a,step_k,step_alpha,step_c,step_Ms = step*self.scale
        scaleVec = self.scale
        def Dga(Ht,Mt,H):
            return (self._predict(Ht,Mt, H, self.a+step_a, self.k, self.alpha, self.c, self.Ms)
                -self._predict(Ht,Mt, H, self.a-step_a, self.k, self.alpha, self.c, self.Ms))/(2*step_a)
        def Dgk(Ht,Mt,H):
            return (self._predict(Ht,Mt, H, self.a, self.k+step_k, self.alpha, self.c, self.Ms)
                -self._predict(Ht,Mt, H, self.a, self.k-step_k, self.alpha, self.c, self.Ms))/(2*step_k)
        def Dgalpha(Ht,Mt,H):
            return (self._predict(Ht,Mt, H, self.a, self.k, self.alpha+step_alpha, self.c, self.Ms)
                -self._predict(Ht,Mt, H, self.a, self.k, self.alpha-step_alpha, self.c, self.Ms))/(2*step_alpha)
        def Dgc(Ht,Mt,H):
            return (self._predict(Ht,Mt, H, self.a, self.k, self.alpha, self.c+step_c, self.Ms)
                -self._predict(Ht,Mt, H, self.a, self.k, self.alpha, self.c-step_c, self.Ms))/(2*step_c)
        def DgMs(Ht,Mt,H):
            return (self._predict(Ht,Mt, H, self.a, self.k, self.alpha, self.c, self.Ms+step_Ms)
            -self._predict(Ht,Mt, H, self.a, self.k, self.alpha, self.c, self.Ms-step_Ms))/(2*step_Ms)
        for ite in range(iterate):
            preM = [0.0]*len(H_data)
            for t in range(0,len(H_data)-1-k,k):
                #forward propagation
                for i in range(k):
                    preM[t+i+1]=self._predict(H_data[t+i],preM[t+i],H_data[t+i+1],self.a, self.k, self.alpha, self.c, self.Ms)
            
                #back-propagation
                grad = (1/float(k))*sum(
                    [scaleVec*((-2*(M_data[t+k-i]-preM[t+k-i])
                        *np.array([Dga(H_data[t+k-i-1],preM[t+k-i-1],H_data[t+k-i]),
                                   Dgk(H_data[t+k-i-1],preM[t+k-i-1],H_data[t+k-i]),
                                   Dgalpha(H_data[t+k-i-1],preM[t+k-i-1],H_data[t+k-i]),
                                   Dgc(H_data[t+k-i-1],preM[t+k-i-1],H_data[t+k-i]),
                                   DgMs(H_data[t+k-i-1],preM[t+k-i-1],H_data[t+k-i])])
                    )) for i in range(k)]
                )
                if np.linalg.norm(grad,2)>=1:
                    grad /= np.linalg.norm(grad,2) 
                self.a -= step_a*grad[0]
                if self.a<0:self.a=self.scale[0]*random()
                self.k -= step_k*grad[1]
                if self.k<0.1*self.scale[1]:self.k=self.scale[1]*random()
                self.alpha -= step_alpha*grad[2]
                if self.alpha<0:self.alpha=self.scale[2]*random()
                self.c -= step_c*grad[3]
                if self.c<0 or self.c >1:self.c=self.scale[3]*random()
                self.Ms -= step_Ms*grad[4]
                if self.Ms<0:self.Ms=self.scale[4]*random()

            if draw:
                preM_data = self.predict(H_data)
                sys.stdout.flush()
                #plt.scatter(H_data, M_data)
                #plt.scatter(H_data, preM_data)
                plt.plot(M_data)
                plt.plot(preM_data)
                #plt.savefig("fit_%d.png"%(ite))
                plt.show()
            print("iterate:\t%d\n%s" % (ite, self.__str__()))
            cost = sum([math.sqrt((M-pM)**2) for M,pM in zip(M_data,preM)])/(len(H_data)-1)
            print("average difference of M between predict and actual:\t"+str(cost))
            #time.sleep(0.5)

    def predict(self, H_data, debug = False):
        M_data = []
        for H in H_data:
            M = self._predict(self.Ht, self.Mt, H, 
                              self.a, self.k, self.alpha, self.c, self.Ms)
            if debug: print("M=%f\tH=%f\n"%(M,H))
            self.Ht, self.Mt = H,M
            M_data.append(M)
        self.Ht, self.Mt = 0.0, 0.0
        return M_data

def readcsv(filename):
    with open(filename) as f:
        H_data = np.array(map(float, f.readline().split(",")))
        M_data = np.array(map(float, f.readline().split(",")))
    return H_data, M_data
    
print("\
#============================JAModel.py Manual=================================\n\
# Given model parameters a, k, alpha, c, Ms, create model by typing:\n\
# >>> material = JAModel([a, k, alpha, c, Ms])\n\
# Instead, given H-M data to find unkown model parameters, \n\
# first create an empty model and then fit the data:\n\
# >>> material = JAModel() \n\
# >>> material.fit(H_data, M_data)\n\
# be careful with physical dimension you choose, set the\n\
# scale of model parameters (a, k, alpha, c, Ms) to adjust dimension:\n\
# >>> material.paraScale([10**3,10**3,10**-4,10**-2,10**4])\n\
# predict M by typing:\n\
# >>> M_data = material.predict(H_data)\n\
# Draw single-line data (ea: M change by time):\n\
# >>> plt.plot(M_data)\n\
# Draw pairwised data (ea: H-M image):\n\
# >>> plt.scatter(H_data, M_data)\n\
# call help for any help:\n\
# >>> help(JAModel):\n\
#\n\
# read data like this:\n\
# >>> H_data, M_data = readcsv(filename)\n\
# supported csv format:\n\
# number,number,number,number,...,number\\n\\\\\number of H_data\n\
# number,number,number,number,...,number\\n\\\\\number of M_data\n\
#==============================================================================\n\
")

metal = JAModel()
#metal.paraScale([10**2,10**2,10**-4,10**-1,10**3])
#metal.__init__()