#!/usr/bin/env python
# coding: utf-8

# ## Import

# In[1]:


import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from tqdm.notebook import trange, tqdm
import random
from scipy.stats import norm
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests


# ## Functions:

# In[2]:


# T-statistic vector = [T^1_1, T^2_1, ... , T^m_1, T^1_2, T^2_2, ..., T^m_2, ..., T^1_K, T^2_K, ..., T^m_K]
# The original matrix is mXK shape. so here we have m time statistics of each size nk. 

def cov_matrix(K, m, sig):
    '''
    Generate the complex covariance matrix of T-statistics from the Group sequential Multiple hypothesis structure 
    ------------
    param:
    K: int
        Number of looks
    m: int 
        Number of multiple hypothesis
    sig: Numpy array 
        List of variances values of size m+1, such that the first value represent the variance of the control group. 
        
    ------------
    Return:
    Covariance matrix from shape m x K
    '''
    # Generate the correct order of T statistics index.  
    index, index_k, index_m = [], [], []
    for i in range(1,K+1): 
        for j in range(1,m+1):
            index.append((i,j))
            index_k.append(i)
            index_m.append(j)

    # Caulculate the sigmas (Multiple hypothesis) part in the correct order 
    sigmas_m = np.identity(len(index_m))
    for i in range(len(index_m)):
        for j in range(i, len(index_m)):
            if index_m[i] == index_m[j]:
                sigmas_m[i-1,j-1] = 1
                sigmas_m[j-1,i-1] = 1
            else:
                sigmas_m[i-1,j-1] = sig[0]/np.sqrt((sig[index_m[i]]+sig[0])*(sig[index_m[j]]+sig[0]))
                sigmas_m[j-1,i-1] = sig[0]/np.sqrt((sig[index_m[i]]+sig[0])*(sig[index_m[j]]+sig[0]))


    # Calculate the GS part in the correct order  
    kl = np.identity(len(index_k))
    for i in range(m*K):
        for j in range(m*K):
            if index_k[i] == index_k[j] :
                kl[i][j] = 1
            else:
                kl[i][j] = np.sqrt(index_k[j]/(index_k[i]))
                kl[j][i] = np.sqrt(index_k[j]/(index_k[i]))

    return kl * sigmas_m

def generate_T_stat(m, K, increment, pai0, sigma, PRDS = True):
    '''
    Generate the T statistics of the Group sequential multiple hypothesis test 
    when we compare each test group to the control such that there is a positive dependency between all hypothesis.
    
    ------------
    Parameters:
    m: int 
        Number of multiple hypothesis
    K: int
        Number of looks
    increment: int
        Diff between the test to control group when H1 is true  
    pai0: float
        Ratio of true null hypothesis
    Sigma: Numpy array 
        List of variances values of size m+1, such that the first value represent the variance of the control group. 
        
    Return:
    ------------
    Data Frame that containes all the T statistics by hypothesis and look.
    
    '''
    mu_vector = ([0]*int(round(pai0*m,0)) + [increment] * int(round(m-pai0*m,0))) *K
    covariance = cov_matrix(K, m, sigma)

    if PRDS == False:
        mid = mid = K*m//2
        idx1, idx2 = int((mid)/2), int(K*m - mid/2)
        covariance[idx1:idx2, idx1:idx2] = covariance[idx1:idx2, idx1:idx2] * (np.eye(mid)*2 -1)
        
    data = np.random.multivariate_normal(mu_vector, covariance)
    T_stat = pd.DataFrame(data.reshape(K, m),
                          columns = ['m'+str(i) for i in range(1,m+1)],
                          index = [i for i in range(1,K+1)])
    return T_stat


def preform_GSBH(stats, m, K, C1, C2):
    '''    
    Preform GSBH procedure on a set of statistics. 
    
    Parameters:
    ------------
    stats: Numpy array
        The cumulative standardized sample mean of each hypothesis 
    m: int 
        Numer of nultiple hypothesis
    K: int
        Number of total stages
    C1: float 
    C2: float
 
    Return:
    ------------
    reject_res: DataFrame
        Contained the test rejection and acceptence results of each hypothesis at each K stage  
    '''    

    alpha_spen = np.diff(np.insert(1-norm.cdf([C1*np.sqrt(K/k) for k in range(1,K+1)]),0,0))
    beta_spen = norm.cdf(np.diff(np.insert([(C1+C2)*np.sqrt(k/K) - C2*np.sqrt(K/k) for k in range(1,K+1)],K,0)))


    m_name = np.array(stats.columns.to_list()) # Hypothesis names 
    results = pd.DataFrame(index = m_name) # Results dataframe 

    
    for i in range(K):
        if m !=0:
            if i ==0:
                pvals=1-norm.cdf(stats.iloc[i])
            else:
                pvals=1-norm.cdf(stats.iloc[i][~np.array(reject_sort+accept_sort)])

                # Filter the Non-Active hypothesis 
                m_name = m_name[~np.array(reject_sort+accept_sort)] 
                stats = stats.loc[:, ~np.array(reject_sort+accept_sort)]
            
            org_sort = np.argsort(pvals)
            pvals_sort, midx  = np.take(pvals, org_sort), np.take(stats.columns, org_sort)
            ecdffactor = np.arange(1,len(pvals)+1)/float(len(pvals))
            
            reject = (pvals_sort/ecdffactor) <= alpha_spen[i]
            if reject.any():
                R_max = max(np.nonzero(reject)[0])
                reject[:R_max] = True
            reject_sort = np.empty_like(reject)
            reject_sort[org_sort] = reject
    
            accept = (pvals_sort/ecdffactor)[::-1] >= beta_spen[i]
            if accept.any():
                A_max = max(np.nonzero(accept)[0])
                accept[:A_max] = True   
            accept = accept[::-1]
            accept_sort = np.empty_like(accept[::-1])
            accept_sort[org_sort] = accept

          # Filter the Non-Active hypothesis 
            if i != (K-1):
                Res = np.where(reject_sort, 'R', np.where(accept_sort, 'A', ''))
            elif i == (K-1):
                Res = np.where(reject_sort, 'R', 'A')
            
            results = results.merge(pd.DataFrame(index = m_name, data = Res, columns=['k'+str(i+1)]), how = 'left', left_index=True, right_index=True)
            m = m-(reject+accept).sum()        
    return results


# ## Simulation

# In[3]:


pai0_values = np.linspace(0.1,0.9,9)
iter = 500

K_lst = [4,10]
m_lst = [600]

for m in tqdm(m_lst):
    for K in tqdm(K_lst):

        sigma2_vec = np.repeat(1,m+1) # Variances =1
        increment = 2

        if K == 1:
            C1, C2 = 1.645, 0.842
        elif K == 4:
            C1, C2 = 1.656, 0.999
        elif K == 10:
            C1, C2 = 1.688, 1.057

        print('K=',K, 'm=',m)
        PRDS_res = pd.DataFrame(columns=['pai0', 'FNR', 'FDR', 'POWER', 'Saved_sample']) # Initialize variables
        for pai0 in tqdm(pai0_values):

            avg_sample_size, FDP, FNP, power = [], [], [], []
            for _ in tqdm(range(iter)):

                T_stats = generate_T_stat(m, K, increment, pai0, sigma2_vec)
                PRDS = preform_GSBH(T_stats, m, K, C1, C2)

                Under_H0, Under_H1 = PRDS[:int(m*pai0)], PRDS[int(m*pai0):]
                TN = np.where(Under_H0 == 'A', True, False).sum()
                FP = np.where(Under_H0 == 'R', True, False).sum()
                FN = np.where(Under_H1 == 'A', True, False).sum()
                TP = np.where(Under_H1 == 'R', True, False).sum()
                sample_size = (np.where((PRDS == 'A')|(PRDS == 'R') , True, False)*range(1,PRDS.shape[1]+1) / K).sum(axis=1)

                FDP.append(FP / np.max([FP + TP,1]))
                FNP.append(FN / np.max([np.sum(FN+TN),1]))
                power.append(TP / len(Under_H1))
                avg_sample_size.append(np.mean(sample_size))

            # Append results to the dataframe
            PRDS_res = pd.concat([PRDS_res, pd.DataFrame([{'pai0': pai0, 'FNR': np.mean(FNP), 'FDR': np.mean(FDP), 'POWER': np.mean(power), 'Saved_sample': 1 - np.mean(avg_sample_size)}])], ignore_index=True)
            PRDS_res.to_excel('PRDS_m{}_K{}.xlsx'.format(m,K))
#         display(PRDS_res)


        Non_PRDS_res = pd.DataFrame(columns=['pai0', 'FNR', 'FDR', 'POWER', 'Saved_sample']) # Initialize variables
        for pai0 in tqdm(pai0_values):

            avg_sample_size, FDP, FNP, power = [], [], [], []
            for _ in tqdm(range(iter)):

                T_stats = generate_T_stat(m, K, increment, pai0, sigma2_vec, PRDS =False)
                Non_PRDS = preform_GSBH(T_stats, m, K, C1, C2)

                Under_H0, Under_H1 = Non_PRDS[:int(m*pai0)], Non_PRDS[int(m*pai0):]
                TN = np.where(Under_H0 == 'A', True, False).sum()
                FP = np.where(Under_H0 == 'R', True, False).sum()
                FN = np.where(Under_H1 == 'A', True, False).sum()
                TP = np.where(Under_H1 == 'R', True, False).sum()
                sample_size = (np.where((Non_PRDS == 'A')|(Non_PRDS == 'R') , True, False)*range(1,Non_PRDS.shape[1]+1) / K).sum(axis=1)

                FDP.append(FP / np.max([FP + TP,1]))
                FNP.append(FN / np.max([np.sum(FN+TN),1]))
                power.append(TP / len(Under_H1))
                avg_sample_size.append(np.mean(sample_size))

            # Append results to the dataframe
            Non_PRDS_res = pd.concat([Non_PRDS_res, pd.DataFrame([{'pai0': pai0, 'FNR': np.mean(FNP), 'FDR': np.mean(FDP), 'POWER': np.mean(power), 'Saved_sample': 1 - np.mean(avg_sample_size)}])], ignore_index=True)
            Non_PRDS_res.to_excel('Non_PRDS_m{}_K{}.xlsx'.format(m,K))
#         display(Non_PRDS_res)

