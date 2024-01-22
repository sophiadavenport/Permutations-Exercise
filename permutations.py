import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

def finding_N(control_p=[0.5, 0.5], treated_p=[0.9, 0.1]): 
    N = 10 #initializing sample size to be 10 since range should fall between 10-30
    repeats=1000 #set arbitrarily
    outcomes=np.array([0, 1])
    list_sig_pvals = [] #initializing list of significant p-vals
    stopper = 0 #limit for while loop
    probs_dict = {} #initializing dictionary to keep track of probabilities
    
    stop = control_p[0]
    
    while stopper < stop:
        total_pvals = []
        for i in range(repeats): 
            control=np.random.choice(outcomes,size=(N),p=control_p)
            control_means=np.mean(control)

            treated=np.random.choice(outcomes,size=(N),p=treated_p)
            treated_means=np.mean(treated)

            #Fisher permutations 
            all_together=np.concatenate((treated, control))
    
            number_of_splits=1000
            differences=np.zeros(number_of_splits)
            all_copy=all_together
            for i in range(number_of_splits):
                np.random.shuffle(all_copy) #Shuffle it
                fake_treated=all_copy[:len(treated)]
                fake_control=all_copy[len(treated):]
                differences[i]=fake_treated.mean()-fake_control.mean()
    
            observed_difference=treated_means.mean()-control_means.mean()
            p_val = np.sum(np.abs(differences) >= np.abs(observed_difference)) / differences.size
            
            total_pvals.append(p_val) #list of all p-values for the simulation
            if p_val < 0.05:
                list_sig_pvals.append(p_val) #adding significant p-value to list
            else:
                continue
            
        current_prob = len(list_sig_pvals)/repeats #gives percentage of trials that had significant 
        probs_dict[N] = current_prob
        if current_prob >= 0.9:
            stopper = 1
        else:
            N +=1 #changing sample size for the next round
            list_sig_pvals = [] #setting back to empty for next round
            continue

    return("sample size:", N, "average p-value:", np.mean(total_pvals), "probability of success:", current_prob, probs_dict)