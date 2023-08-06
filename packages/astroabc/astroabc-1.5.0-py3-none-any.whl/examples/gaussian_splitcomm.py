#simple example script for multiGaussian data
#try:
#	import astroabc
#except ImportError:
#	raise ImportError("Please install the astroABC package to use the sampler\n" +
#                            "$> pip install astroabc")

#import sys
#sys.path.append("../astroabc")
from astroabc.abc_class import *

from examples.parse_params import *
import os
ROOT_dir = os.path.split(os.path.abspath(__file__))[0]
param_file = os.path.join(ROOT_dir,'gaussian_splitcomm_params.ini')


def dist_metric(d,x):
        '''Distance metric: rho'''
        return np.sum(np.abs(np.mean(x,axis=0) - np.mean(d,axis=0)))

def simulation(param, pool=None):
        #add code here to simulate data given parameters
        #below is simple simulation which draws 1000 random samples from a multiGaussian;
        #we map the make_mock method to the pool and divide up the work of simulating the data
        cov =np.array([0.009,0.005,0.005,0.1])
        if pool:
                num_sim = pool.size - 1   #number of processors available to simulation
                pool_outputs = pool.map(Model("normal",500).make_mock, zip([param]*2,[cov]*2) )
                sim_output = np.concatenate(pool_outputs)
                return sim_output
        else:
                return Model("normal",1000).make_mock(param,cov)



def main():

        param = np.array([true_p0,true_p1])
        #print "\t True param value:", param

        #make some fake data
        data = Model(model_type,nsamples).make_mock(param, np.array([0.009,0.005,0.005,0.1]))

        #Create an instance of the ABC class
        sampler = ABC_class(nparam,npart,data,tlevels,niter,prior,**prop)

        #specify the simulation method
        #model_sim = astroabc.Model(model_type,nsamples).make_mock
        model_sim = simulation


        #Start sampling!
        sampler.sample(model_sim)




if __name__ == "__main__":

        pconfig = ParseParams(param_file)
        #if pconfig.verbose: print "parameters in file: ",  vars(pconfig)
        
        datafile =pconfig.datafile
        model_type = pconfig.model_type
        nsamples = pconfig.nsamples
        true_p0 = pconfig.true_p0
        true_p1 = pconfig.true_p1
        #########
        #Parameters of abc run, these are global
        ########
        nparam =pconfig.nparam
        npart = pconfig.npart
        niter = pconfig.niter
        tlevels = pconfig.tlevels
        out_prefix = pconfig.outfile
        re_prefix = pconfig.restart
        outF = out_prefix+"_"+str(npart)+"part_"+str(niter)+"iter_"+str(nparam)+"nparam.txt"
        restartF = re_prefix+"_abc_"+str(npart)+"part_"+str(niter)+"iter_"+str(nparam)+"nparam.txt"

        if pconfig.num_proc == 1:
            num_proc = None
        else:
            num_proc = pconfig.num_proc

        prop={'tol_type':pconfig.tol_type,"verbose":pconfig.verbose,'adapt_t':pconfig.adapt_t,\
        'threshold':pconfig.threshold,'pert_kernel':pconfig.pert_kernel,\
        'variance_method':pconfig.var_method, 'dist_type': pconfig.dist_type,'dfunc':dist_metric, 'restart':restartF,\
        'outfile':outF,'mpi':pconfig.mpi,'mp':pconfig.mp,'num_proc':num_proc, 'from_restart':pconfig.from_restart,\
         'mpi_splitcomm':pconfig.mpi_splitcomm, 'num_abc':pconfig.num_abc}

        ###########
        param_names = np.array(pconfig.pnames)
        priorname  = pconfig.priors
        hyperp = pconfig.hyperp
        prior = zip(priorname,hyperp)
        main()

