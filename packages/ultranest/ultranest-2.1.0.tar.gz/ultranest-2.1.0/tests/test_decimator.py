import numpy as np
from ultranest.decimator import decimate

def test_decimator():

    def loglike2(z):
        a = np.array([-0.5 * sum([((xi - 0.83456 + i*0.1)/0.0000005)**2 for i, xi in enumerate(x)]) for x in z])
        b = np.array([-0.5 * sum([((xi - 0.43456 - i*0.1)/0.0005)**2 for i, xi in enumerate(x)]) for x in z])
        loglike2.ncalls += len(a)
        return np.logaddexp(a, b)
    loglike2.ncalls = 0
    
    def loglike(z):
        return np.array([-0.5 * sum([((xi - 0.5)/0.1**(i*0.1+1))**2 for i, xi in enumerate(x)]) for x in z])

    def transform2(x):
        return 10. * x - 5.
    def transform(x):
        return x
    
    lo, hi = decimate(50, transform, loglike)
    assert (lo >= 0).all()
    assert (hi <= 1).all()

    
if __name__ == '__main__':
    test_decimator()
