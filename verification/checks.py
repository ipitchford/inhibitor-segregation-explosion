#!/usr/bin/env python3
"""Independent finite algebra checks; the written proofs establish explosion."""
from fractions import Fraction as F
from math import comb, log, exp
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent

def padd(a,b):
    out=[F(0)]*max(len(a),len(b))
    for j,v in enumerate(a): out[j]+=v
    for j,v in enumerate(b): out[j]+=v
    return out

def pmul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for j,x in enumerate(a):
        for k,y in enumerate(b): out[j+k]+=x*y
    return out

def ppow(a,n):
    out=[F(1)]
    for _ in range(n): out=pmul(out,a)
    return out

def peval(a,s):
    value=F(0)
    for v in reversed(a): value=value*s+v
    return value

def birth_step(N,D,r):
    # Substitute the Yule PGF r*s/[1-(1-r)*s] into N(s)/D(s).
    k=max(len(N),len(D))-1
    h=[F(1),r-1]
    def transform(poly):
        out=[F(0)]
        for j,a in enumerate(poly):
            term=pmul([F(0)]*j+[r**j*a],ppow(h,k-j))
            out=padd(out,term)
        return out
    return transform(N),transform(D)

def loss_step(N,D):
    # Exact PGF of max(Z-1,0): F(0)+(F(s)-F(0))/s.
    f0=N[0]/D[0]
    residual=padd(N,[-f0*x for x in D])
    require(residual[0]==0,'PGF removable zero')
    return padd(residual[1:],[f0*x for x in D]),D

def require(ok, message):
    if not ok:
        raise AssertionError(message)

def binomial(i, p):
    return [(k, F(comb(i,k))*p**k*(1-p)**(i-k)) for k in range(i+1)]

def chemical_rates(model, s, i, b, c, d):
    if model == 'catalytic':
        return [(s+1,i,b*s*(s-1)),(s,i+1,c*s),(s-1,i,d*i*s*(s-1))]
    return [(s+1,i,b*s*(s-1)),(s,i+1,c*s),(s-1,i+1,d*i*s)]

def apply_physical(model, f, s, i, C, b,c,d,lam,p):
    ans = sum(rate*(f(ss,ii,C)-f(s,i,C))
              for ss,ii,rate in chemical_rates(model,s,i,b,c,d) if rate)
    ans += lam*s*sum(prob*(f(s,k,C+1)-f(s,i,C)) for k,prob in binomial(i,p))
    return ans

def apply_operational(model, g, z,i,C,b,c,d,lam,p):
    ans=b*z*(g(z+1,i,C)-g(z,i,C))+c*(g(z,i+1,C)-g(z,i,C))
    if model=='catalytic':
        if z:
            ans+=d*i*z*(g(z-1,i,C)-g(z,i,C))
    else:
        if i:
            ans+=d*i*(g(z-1,i+1,C)-g(z,i,C))
    ans+=lam*sum(prob*(g(z,k,C+1)-g(z,i,C)) for k,prob in binomial(i,p))
    return ans

def run():
    count=0
    p_values=[F(0),F(1,10),F(1,2),F(9,10),F(1)]
    for i in range(13):
        for p in p_values:
            law=binomial(i,p)
            require(sum(prob for _,prob in law)==1,'binomial normalisation')
            require(sum(k*prob for k,prob in law)==p*i,'binomial mean')
            require(sum(k*(k-1)*prob for k,prob in law)==p*p*i*(i-1),'binomial pair moment')
            for k,prob in law:
                require(k+(i-k)==i and prob>=0,'fragmentation conservation')
                count+=1
    tests=[lambda z,i,C:F(z),lambda z,i,C:F(i),lambda z,i,C:F(C),
           lambda z,i,C:F(z*z+i*C),lambda z,i,C:F(1,z+3)+F(1,i+2)+F(C)]
    fingerprints=[]
    for model in ['catalytic','conversion']:
        b,c,d,lam=map(F,[2,1,1,3])
        for s in range(1,9):
            for i in range(9):
                for p in p_values:
                    for g in tests:
                        physical=apply_physical(model,lambda ss,ii,CC:g(ss-1,ii,CC),s,i,2,b,c,d,lam,p)
                        operational=apply_operational(model,g,s-1,i,2,b,c,d,lam,p)
                        require(physical==s*operational,'clock identity '+model)
                        count+=1
        for s,i in [(2,0),(2,1),(3,2),(4,3)]:
            rates=[r for _,_,r in chemical_rates(model,s,i,b,c,d)]
            fingerprints.append(dict(model=model,state=[s,i],physical=[str(r) for r in rates],operational=[str(r/s) for r in rates]))
    # Check the classical PGF equation directly at independent rational inputs.
    for a in [F(1,5),F(1),F(3)]:
        for B in [F(1,3),F(1),F(4)]:
            for s in [F(0),F(1,7),F(2,3),F(1)]:
                b,death=F(2),F(5,3)
                x=1-s
                denominator=a+B*x
                a_prime=(death-b)*a
                B_prime=b*a
                time_derivative=x*(a_prime+B_prime*x)/denominator**2
                space_derivative=a/denominator**2
                require(time_derivative==(s-1)*(b*s-death)*space_derivative,'PGF forward equation')
                count+=1
    # Compare two independent exact calculations of the scheduled-removal law:
    # rational PGF evolution versus the Poisson-binomial/Gamma-family formula.
    schedules=[[],[F(1,2)],[F(1,2),F(1,3)],
               [F(3,4),F(1,2),F(2,3)],[F(3,5),F(4,5),F(1,2),F(3,4)]]
    scheduled_checks=0
    for z0 in [1,2,3,5]:
        for schedule in schedules:
            N,D=[F(0)]*z0+[F(1)],[F(1)]
            q=F(1)
            weights=[F(1)]
            for r in schedule:
                N,D=birth_step(N,D,r)
                N,D=loss_step(N,D)
                q*=r
                weights=pmul(weights,[1-q,q])
            N,D=birth_step(N,D,F(2,3))
            q*=F(2,3)
            for s in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
                g=q*s/(1-(1-q)*s)
                mixture=sum(w*g**max(z0-k,0) for k,w in enumerate(weights))
                require(peval(N,s)/peval(D,s)==mixture,'scheduled-removal distribution')
                scheduled_checks+=1
                count+=1
    # Environment means from event enumeration, including self-catastrophes.
    for i in range(12):
        for p in p_values:
            c,d,lam=F(1),F(2),F(3)
            jump_mean=sum(prob*(k-i) for k,prob in binomial(i,p))
            require(c+lam*jump_mean==c-lam*(1-p)*i,'catalytic environment drift')
            require(c+d*i+lam*jump_mean==c+(d-lam*(1-p))*i,'conversion environment drift')
            count+=2
    b,c,d,lam,p,z,i0=F(1),F(1),F(2),F(3),F(0),F(2),F(0)
    Delta=b+lam*(1-p)-d
    K=d*(i0+c/b)/Delta
    lower=1-K/z
    older_lower=(z-K)**2/(z*z+z)
    require((Delta,K,lower,older_lower)==(F(2),F(1),F(1,2),F(1,6)),'explicit probability certificates')
    # Deliberately perturb the object under check and require the same invariant
    # to reject it. These are negative controls, not proofs of the theorem.
    def rejects(fn):
        try:
            fn()
        except AssertionError:
            return True
        return False
    pg=lambda z,i,C:F(z)
    physical=apply_physical('catalytic',lambda ss,ii,CC:pg(ss-1,ii,CC),3,0,1,F(2),F(1),F(1),F(3),F(1,2))
    operational=apply_operational('catalytic',pg,2,0,1,F(2),F(1),F(1),F(3),F(1,2))
    corrupt_law=[(k,prob*2) for k,prob in binomial(4,F(1,3))]
    wrong_mean_loss=F(1)-F(3)*F(1,10)*F(4)
    enumerated_mean=F(1)+F(3)*sum(prob*(k-4) for k,prob in binomial(4,F(1,10)))
    wrong_probability=(z-K)**2/(z*z)
    mutants={
        'divide_by_S_minus_one':rejects(lambda:require(physical/(3-1)==operational,'clock identity')),
        'double_fragmentation_probabilities':rejects(lambda:require(sum(prob for _,prob in corrupt_law)==1,'kernel normalisation')),
        'retention_used_as_loss_probability':rejects(lambda:require(wrong_mean_loss==enumerated_mean,'environment drift')),
        'omit_Yule_variance_term':rejects(lambda:require(wrong_probability==F(1,6),'explicit probability certificate')),
    }
    require(all(mutants.values()),'negative controls must be rejected')
    # These inequalities merely check the illustrative random-retention example.
    gamma_fixed=2+log(.5)
    gamma_random=2+.5*(log(.1)+log(.9))
    require(gamma_random<1<gamma_fixed,'random retention contrast')
    result={
        'status':'PASS','exact_checks':count,'scheduled_removal_pgf_checks':scheduled_checks,'negative_controls_rejected':mutants,
        'fingerprints':fingerprints,
        'explicit_bound':{'Delta':str(Delta),'K':str(K),'probability_lower_bound':str(lower),'auxiliary_second_moment_bound':str(older_lower)},
        'random_retention_example':{'mean_both':.5,'gamma_fixed':gamma_fixed,'gamma_random':gamma_random,'b':1},
        'scope':'Finite algebra and constants only. The code does not prove explosion, critical extinction, or historical novelty.'
    }
    (ROOT/'verification'/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    run()
