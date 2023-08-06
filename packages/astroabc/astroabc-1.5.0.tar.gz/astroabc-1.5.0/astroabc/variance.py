import numpy as np
from sklearn.covariance import ledoit_wolf
from sklearn.neighbors import KDTree
import sys

class Variance(object):
        '''General variance class'''
        def __init__(self,nparam,start):
                '''
                Input: 
                nparam: parameter vector for all particles at iter t
                start: Boolean,  True if iteration 0, False otherwise
                '''
                self.nparam = nparam
                self.start=start

        def first_iter(self,t,params):
                '''
                On first iteration calculate the variance as either the standard deviation
                or covariance amongst the particles, depending on value chosen for pert_kernel
                Input: 
                t: Iteration number
                params: parameter vector for all particles
                '''
                self.start = False
                if self.pert_kernel ==1:
                        return np.diag([2.*np.std(params[:,ii])**2 for ii in range(self.nparam)])
                elif self.pert_kernel ==2:
                        return 2.*np.cov(params.T)

class TVZ(Variance):
        '''Simple variance estimate (Turner & Van Zandt 2012) '''
        def __init__(self,nparam,pert_kernel):
                ''' Input:
                nparam: parameter vector for all particles at iter t 
                pert_kernel: 1 component wise perturbation with local diag variance,
                        2 multivariate perturbation based on local covariance
                '''
                Variance.__init__(self,nparam,True)
                self.pert_kernel = pert_kernel

        def get_var(self,t,params):
                ''' Input:
                t: iteration level
                pms: parameter vector for all particles from previous iteration
                Returns:
                        pert_kernel =1:twice the diagonal variance
                        pert_kernel =2:twice the sample covariance 
                '''
                if self.start:
                        return self.first_iter(t,params)
                else:
                        if self.pert_kernel ==1:
                                return np.diag([2.*np.std(params[:,ii])**2 for ii in range(self.nparam)])
                        elif self.pert_kernel ==2:
                                return 2.*np.cov(params.T)

class nearest_neighbour(Variance):
        ''' Local weighted covariance matrix class using k nearest neighbours'''
        def __init__(self,nparam,npart,pert_kernel):
                ''' 
                Input: 
                nparam: parameter vector for all particles at iter t and t-1
                npart: number of particles
                pert_kernel: 1 component wise perturbation with local diag variance,
                        2 multivariate perturbation based on local covariance
                '''

                Variance.__init__(self,nparam,True)
                self.npart=npart
                self.pert_kernel = pert_kernel

        def get_var(self,t,pms,wgt,k_near):                                                     
                '''Method to calculate the local weighted particle covariance matrix using k nn
                https://en.wikipedia.org/wiki/Weighted_arithmetic_mean#Weighted_sample_covariance
                Input:
                t: iteration level
                pms: parameter vector for all particles from previous iteration
                wgt: weights from previous iteration
                k_near: number of nearest neighbours to use in calculation
                Returns:
                        Twice the local weighted particle covariance
                '''
                tm1 = t-1
                if  k_near > self.npart:
                                print(("\t Too many nearest neighbours requested for the number of particles: k_near=%d npart=%d") % (k_near,self.npart))
                                print("\t exiting...")
                                sys.exit(0)
                elif k_near < 2:
                                print(("\t k_near too small: k_near=%d.  Please choose k_near>=2") % (k_near))
                                print("\t exiting...")
                                sys.exit(0)
                if t==0:
                        return self.first_iter(t,pms)
                else:
                        var_particles = np.zeros((self.npart,self.nparam,self.nparam))
                        leaf = 0.2*self.npart
                        tree = KDTree(pms,leaf_size = leaf)
                        for ll in range(self.npart):
                                #for each particle, find the k_near nearest neighbours and return their particle id
                                ind = tree.query(pms[ll].reshape(1,-1),k_near,sort_results=True,return_distance=False)
                                coeff = wgt[ind][0].sum() / (wgt[ind][0].sum()**2 - (wgt[ind][0]**2).sum())
                                wgt_mean = np.average(pms[ind][0], axis=0, weights=wgt[ind][0])
                                var = np.diag(np.zeros(self.nparam))
                                if self.pert_kernel ==1:
                                        for kk in range(self.nparam):
                                                var[kk][kk] = coeff*np.sum(wgt[ind][0] * (pms[ind,kk] - wgt_mean[kk])**2)
                                elif self.pert_kernel ==2:
                                        for kk in range(self.nparam):
                                                for jj in range(self.nparam):
                                                        var[kk,jj] = coeff*np.sum(wgt[ind][0]*(pms[ind,kk] - wgt_mean[kk])*(pms[ind,jj] - wgt_mean[jj]))
                                                        if kk == jj and var[kk,jj]==0: #delta function for one parameter
                                                                var[kk,jj] = 1.E-10
                                var_particles[ll] = 2*var

                        return var_particles


class Filippi(Variance):
        '''Filippi et al 2012, eq 12 & 13'''
        def __init__(self,nparam,npart,pert_kernel):
                ''' Input:
                nparam: parameter vector for all particles at iter t
                npart: number of particles
                pert_kernel: 1 component wise perturbation with local diag variance,
                        2 multivariate perturbation based on local covariance
                '''
                Variance.__init__(self,nparam,True)
                self.npart=npart
                self.pert_kernel = pert_kernel

        def get_var(self,t,pms,delta,tol,wgt):
                ''' Input:
                t: iteration level
                pms: parameter vector for all particles from previous iteration
                delta: distances at t-1
                tol: epsilon at t
                wgt: particle weights at t-1
                Returns:
                        pert_kernel =1:component wise perturbation with local diag variance (Filippi et al 2012 Eq. 11 and 12)
                        pert_kernel =2:multivariate perturbation based on local covariance 
                '''
                tm1 = t-1
                if t==0:
                        return self.first_iter(t,pms)
                else:
                        #find subsample at t-1 which pass tolerance at t
                        ind = np.where(delta <= tol)[0]
                        n0 = len(ind)
                        t_n0 = pms[ind]
                        w_n0 = wgt[ind]
                        var = np.diag(np.zeros(self.nparam))
                        if n0 ==0:
                                return self.first_iter(t,pms)
                        else:
                                w_n0 = w_n0/np.sum(w_n0) # normalise

                                if self.pert_kernel ==1:
                                        #var = np.zeros(self.nparam)
                                        for kk in range(self.nparam):
                                                var[kk][kk] = np.sum([np.sum(wgt[ii]*w_n0*(pms[ii][kk] - t_n0[:,kk])**2 ) for ii in range(self.npart)])
                                elif self.pert_kernel ==2:
                                        part_test = np.diag(np.zeros(self.npart))
                                        for kk in range(self.nparam):
                                                for jj in range(self.nparam):
                                                        var[kk,jj] = np.sum([np.sum(wgt[ii]*w_n0*(t_n0[:,kk]-pms[ii][kk])*(t_n0[:,jj]-pms[ii][jj]) ) for ii in range(self.npart)])
                                return var



class weighted_cov(Variance):
        ''' Weighted covariance matrix class''' 
        def __init__(self,nparam,npart,pert_kernel):
                '''
                Input:
                nparam: parameter vector for all particles at iter t and t-1
                npart: number of particles
                pert_kernel: 1 component wise perturbation with local diag variance,
                        2 multivariate perturbation based on local covariance
                '''

                Variance.__init__(self,nparam,True)
                self.npart=npart
                self.pert_kernel = pert_kernel

        def get_var(self,t,pms,wgt):
                '''Method to calculate the weighted particle covariance matrix
                https://en.wikipedia.org/wiki/Weighted_arithmetic_mean#Weighted_sample_covariance
                Input:
                t: iteration level
                pms: parameter vector for all particles from previous iteration
                wgt: weights from previous iteration
                Returns:
                        Twice the weighted particle covariance (Beaumont et al 2009)
                '''
                tm1 = t-1
                if t==0:
                        return self.first_iter(t,pms)
                else:
                        coeff = wgt.sum() / (wgt.sum()**2 - (wgt**2).sum())
                        wgt_mean = np.average(pms, axis=0, weights=wgt)
                        var = np.diag(np.zeros(self.nparam))
                        if self.pert_kernel ==1:
                                for kk in range(self.nparam):
                                        var[kk][kk] = coeff*np.sum(wgt * (pms[:,kk] - wgt_mean[kk])**2)
                        elif self.pert_kernel ==2:
                                for kk in range(self.nparam):
                                        for jj in range(self.nparam):
                                                var[kk,jj] = coeff*np.sum(wgt*(pms[:,kk] - wgt_mean[kk])*(pms[:,jj] - wgt_mean[jj]))
                                                if kk == jj and var[kk,jj]==0: #delta function for one parameter
                                                        var[kk,jj] = 1.E-10
                        return 2*var



class Leodoit_Wolf(Variance):
        '''l2 shrinkage with the Ledoit-Wolf estimator'''
        def __init__(self,nparam,pert_kernel):
                ''' Input: 
                nparam: parameter vector for all particles at iter t 
                pert_kernel: 1 component wise perturbation with local diag variance,
                        2 multivariate perturbation based on local covariance
                '''
                Variance.__init__(self,nparam,True)
                self.pert_kernel = pert_kernel

        def get_var(self,t,params):
                ''' Input: 
                t: iteration level
                pms: parameter vector for all particles from previous iteration
                Returns:
                particle covariance with Ledoit-Wolf estimator
                '''
                if self.start:
                        return self.first_iter(t,params)
                else:
                    var, _  =  ledoit_wolf(params)
                return var


