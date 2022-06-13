#from matplotlib import rc
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
#rc('text', usetex=True)

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import numpy as n

fig = plt.figure(figsize=(1.5*10,1.5*6.4),facecolor='white')
ax1 = fig.add_subplot(1,1,1)
plt.axis('off')    


# y[t] = sum_{k=0}^{L-1} h[k]x[t-k]
def conv(x,h,t):
    N=len(x)
    L=len(h)
    y=n.zeros(len(x))
    hd=n.zeros(len(x))
    hr=h[::-1]
    for ti in range(t):
        for k in range(L):
            if (ti-k) > -1 and (ti-k) < N:
                y[ti]+=x[ti-k]*h[k]
    for k in range(L):
        if (t+k-L) > -1 and (t+k-L) < N:
            hd[t+k-L]=hr[k]
    return([y,hd])

def animate(i,x,h,scale=1.0):
#    print(i)

    ax1.clear()
    N=len(x)

    L=len(h)
    idx = i%N

    r=conv(x,h,idx)
    t = n.arange(N)
    y=r[0]
    hd=r[1]

    nidx=n.repeat(0,N)
    ax1.vlines(t[0:idx],nidx[0:idx],y[0:idx]*0.8*scale,color="black")
    ax1.scatter(t[0:idx],y[0:idx]*0.8*scale,facecolor="black")
    plt.text(N-3,0.5,"$y[n]$",size=20)
    plt.plot([0,N],[0,0],color="black")    
    
    ax1.vlines(t,n.repeat(2,N),x*0.8+2,color="black")
    ax1.scatter(t,x*0.8+2,facecolor="black")
    plt.text(N-3,2.5,"$x[k]$",size=20)
    plt.plot([0,N],[2,2],color="black")
    
    hidx=n.arange(n.max([0,idx-L]),n.min([idx,N]))

    hdc=n.repeat(4,L)                  
    ax1.vlines(t[hidx],hdc[0:len(hidx)],hd[hidx]*0.8+4,color="black")
    ax1.scatter(t[hidx],hd[hidx]*0.8+4,facecolor="black")
    plt.text(N-3,4.5,"$h[%d-k]$"%(i),size=20)    

    nz_idx = n.where( (n.abs(x)!=0) & (n.abs(hd)!=0))[0]
    for nzi  in nz_idx:
        ax1.plot([t[nzi],t[nzi]],[1,1000],color="lightblue",zorder=-1)
    ax1.quiver(idx-1,1,0,-1,color="grey",zorder=-1,width=0.0022)
    ax1.text(idx-1+1,1,"$y[%d]=\sum_{k=-\infty}^{\infty}x[k]h[%d-k]$"%(i,i),size=20,zorder=-1)            
    
    plt.plot([0,N],[4,4],color="black")
    plt.axis('off')    
    plt.ylim([-1,5])

    plt.title("$n=%d$"%(idx),size=20)


def ex1():
    N=100
    # kroenecker delta
    x = n.zeros(N)
    x[int(N/2):int(N/2+10)]=n.random.rand(10)-0.5
    
    # boxcar
    h = n.zeros(1)
    h[0]=1.0
    return(x,h)

def ex2():
    N=100
    # kroenecker delta
    x = n.zeros(N)
    x[int(N/2)]=1.0
    
    # boxcar
    h = n.zeros(10)
    h[0:10]=n.random.rand(10)-0.5

    return(x,h)

def ex3():
    N=100
    # random x
    x = n.zeros(N)
    x[int(N/2):int(N/2+10)]=n.random.rand(10)-0.5    
    
    # boxcar
    h = n.zeros(10)
    h[0:10]=1.0/5.0
    return(x,h)

def ex4():
    N=100
    # random x
    x = n.zeros(N)
    x[0:N]=n.random.rand(N)-0.5    
    
    # boxcar
    h = n.zeros(20)
    h[0:20]=1.0/5.0
    return(x,h)

def ex5():
    N=100
    # random x
    x = n.zeros(N)
    x[int(N/2):int(N/2+10)]=1.0
    
    # boxcar
    h = n.zeros(10)
    h[0:10]=1.0/5.0
    return(x,h)

def ex6():
    N=100
    # random x
    x = n.zeros(N)
    x[int(N/2):int(N/2+10)]=1.0
    
    # boxcar
    h = n.zeros(2)
    h[0]=1.0
    h[1]=-1.0
    return(x,h)

def ex7():
    N=100
    # random x
    x = n.zeros(N)
    x=n.sin(2.0*n.pi*1.0/10.0*n.arange(N))
    
    # boxcar
    h = n.zeros(5)
    h[4]=1.0
    return(x,h)


def numerical_derivative():
    N=100
    # random x
    x = n.zeros(N)
    x[int(-N/2-10):int(-N/2+10)]=1.0
    
    # numerical derivative
    h = n.zeros(2)
    h[0]=0.5
    h[1]=-0.5
    return(x,h)

def diff2():
    N=100
    # random x
    x = n.zeros(N)
    x[:]=1.0
    x[int(N/2)-10]=0.0
    x[int(N/2)+10]=2.0
    
    # numerical derivative
    h = n.zeros(3)
    h[0]=0.5
    h[1]=-1.0
    h[2]=0.5
    return(x,h)


def ex8():
    N=100
    # random x
    x = n.zeros(N)
    x=n.sin(2.0*n.pi*1.0/4.0*n.arange(N))
    
    # boxcar
    h = n.zeros(3)
    h[0]=1/4.0
    h[1]=1.0/2.0
    h[2]=1.0/4.0
    return(x,h)


def ex9():
    N=100
    # random x
    x = n.zeros(N)
    x=n.sin(2.0*n.pi*1.0/20.0*n.arange(N))
    
    # boxcar
    h = n.zeros(3)
    h[0]=1/4.0
    h[1]=1.0/2.0
    h[2]=1.0/4.0
    return(x,h)

def ex10():
    N=100
    # random x
    x = n.zeros(N)
    x[50]=2.0
    x[51]=1.0
    x[52]=3.0
    
    # boxcar
    h = n.zeros(2)
    h[0]=1
    h[1]=-1.0

    return(x,h)


def ex11():
    N=100
    # random x
    x = n.zeros(N)
    rs=n.array([1,1,1,1,1,-1,-1,1,1,-1.0,1,-1,1])
    L=len(rs)
    x[int(N/2):int(N/2+L)]=rs
    
    # boxcar
    h = rs[::-1] #n.zeros(20)
    return(x,h)

def ex12():
    N=100
    # random x
    x = n.zeros(N)
    rs=n.array([1,1,1,1,1,-1,-1,1,1,-1.0,1,-1,1])
    L=len(rs)
    x[int(N/2-20):int(N/2+L-20)]=rs

    # truncated inverse filter
    h = n.fft.fftshift(n.fft.ifft(1.0/n.fft.fft(rs,1024)).real)
    h = h[(512-40):(512+40)]*3.0

    return(x,h)

def create_animation(x,h,file_name="example"):
    # scale signals
    x=x/n.max(n.abs(x))
    h=h/n.max(n.abs(h))
    y=n.convolve(x,h)
    # scale the output signal in such a way that the largest
    # value has amplitude 1.0
    scale=1.0/n.max(n.abs(y))
    ani = animation.FuncAnimation(fig, animate, interval=100, fargs=(x,h,scale))
    ani.save("%s.gif"%(file_name), writer='imagemagick', fps=5)
    
funs = [diff2,numerical_derivative,ex3,ex12,ex1,ex2,ex4,ex5,ex7,ex8,ex9,ex10,ex11]

for f in funs:
    print("Creating %s.gif"%(f.__name__))
    x,h=f()
    create_animation(x,h,file_name=f.__name__)
