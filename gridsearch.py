import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import KFold
from itertools import product
import matplotlib.pyplot as plt

# 4. generate matplotlib plots that will assist in identifying the optimal clf and parampters settings
# Recommend to be done before live class 4
# 5. Please set up your code to be run and save the results to the directory that its executed from
# 6. Investigate grid search function

def run(a_clf, data, clf_hyper={}):
  M, L, n_folds = data # unpack data container
  kf = KFold(n_splits=n_folds) # Establish the cross validation
  ret = {} # classic explication of results
  
  for ids, (train_index, test_index) in enumerate(kf.split(M, L)):
    clf = a_clf(**clf_hyper) # unpack parameters into clf

    clf.fit(M[train_index], L[train_index])

    pred = clf.predict(M[test_index])

    ret[ids]= {'clf': clf,
               'train_index': train_index,
               'test_index': test_index,
               'accuracy': accuracy_score(L[test_index], pred)}
  return ret

def getCLFwithParams(clfsWithParams):
  """
  This generator returns a classifier with hypers for each combination in the dictionary input
  """
  #Get all of the combinations of params possible from what is provided
  for clf, parameters in clfsWithParams.items():
    #For each clf, get the product of all the param sets
      allCombos = list(product(*parameters.values()))
      for paramSet in allCombos:
          #Finally, yield CLF:parameter tuples.
          yield (clf, dict(zip(parameters.keys(), paramSet)))


def hyper_search(classifiersWithParamsDict, data):
  """
  This consumes the generator getCLFwithParams, and returns a list of tuples with ((clf, hypers), results)
  """
  results = []
  for clf, parameters in getCLFwithParams(classifiersWithParamsDict):
    results.append(((clf, parameters), run(clf, data, parameters)))
  return results

def main():
  data = np.loadtxt('seeds_dataset.txt')
  #The seeds classification dataset is used here, from: https://archive.ics.uci.edu/ml/datasets/seeds
  #There are 7 attributes, with col 7 being the response.
  M = data[:, 0:7]
  L = data[:, 7]

  n_folds = 5

  data = (M, L, n_folds)

  clfsWithParams = {
    KNeighborsClassifier:{
      'n_neighbors': [2,4,6,8],
      'algorithm': ['ball_tree', 'kd_tree', 'brute'],
      'p': [1, 2, 3]
    },
    SVC:{
      'C': [0.1, 1, 2],
      'degree': [2,3,4],
      'decision_function_shape': ['ovo', 'ovr'],
    },
    RandomForestClassifier:{
      'n_estimators': [10, 20, 30],
      'class_weight': ['balanced', 'balanced_subsample'],
      'max_depth': [5,10,15]
    }
  }

  clfsAccuracy = hyper_search(clfsWithParams, data)
  
  clfsAccurarySum = [] #This sums up the classification accuracy scores similar to how David's code did, just without using a dict.
  for testCase, results in clfsAccuracy:
    testAccuracies = [x.get('accuracy') for x in results.values()] #Retain only the accuracy scores here
    clfsAccurarySum.append((testCase, testAccuracies)) #Testcase (unmodified) is (clf, hypers)

  filename_prefix = 'clf_Histograms_'

  # initialize the plot_num counter for incrementing in the loop below
  plot_num = 1

  # Adjust matplotlib subplots for easy terminal window viewing
  left  = 0.125  # the left side of the subplots of the figure
  right = 0.9    # the right side of the subplots of the figure
  bottom = 0.1   # the bottom of the subplots of the figure
  top = 0.6      # the top of the subplots of the figure
  wspace = 0.2   # the amount of width reserved for space between subplots,
                # expressed as a fraction of the average axis width
  hspace = 0.2   # the amount of height reserved for space between subplots,
                # expressed as a fraction of the average axis height
  n = 5

  #create the histograms
  #matplotlib is used to create the histograms: https://matplotlib.org/index.html
  for testcase, result in clfsAccurarySum:
      fig = plt.figure(figsize =(10,10)) # This dictates the size of our histograms
      ax  = fig.add_subplot(1, 1, 1) # As the ax subplot numbers increase here, the plot gets smaller
      plt.hist(result, facecolor='green', alpha=0.75) # create the histogram with the values
      ax.set_title(testcase[0].__name__+'\n'+str(testcase[1]), fontsize=25) # increase title fontsize for readability
      ax.set_xlabel('Classifer Accuracy (By K-Fold)', fontsize=25) # increase x-axis label fontsize for readability
      ax.set_ylabel('Frequency', fontsize=25) # increase y-axis label fontsize for readability
      ax.xaxis.set_ticks(np.arange(0, 1.1, 0.1)) # The accuracy can only be from 0 to 1 (e.g. 0 or 100%)
      ax.yaxis.set_ticks(np.arange(0, n+1, 1)) # n represents the number of k-folds
      ax.xaxis.set_tick_params(labelsize=20) # increase x-axis tick fontsize for readability
      ax.yaxis.set_tick_params(labelsize=20) # increase y-axis tick fontsize for readability
      # pass in subplot adjustments from above.
      plt.subplots_adjust(left=left, right=right, bottom=bottom, top=top, wspace=wspace, hspace=hspace)
      plot_num_str = str(plot_num) #convert plot number to string
      filename = filename_prefix + testcase[0].__name__ + plot_num_str # concatenate the filename prefix and the plot_num_str
      plt.savefig(filename, bbox_inches = 'tight') # save the plot to the user's working directory
      plot_num = plot_num+1 # increment the plot_num counter by 1


if __name__ == '__main__':
  main()
