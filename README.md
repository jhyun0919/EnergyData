# Energy Data Anlysis


This is a series of process showing the effort to manage energy more efficiently through analyzing data from certatin buildings.

  * **Preprcessing**
    * Interpolation
    * Normalization
    * Vectorization
  
  * **Clustering** - unsing unsupervised learning algorithm  
      (_yet clusters are not verified_)
    * K-means
    * Affinity propagation  
    
  * **Classifier**
    * Gaussian Naive-Bayesian

  * **Dependency modeling**
    * Nearest-neighbors
    * Bayesian Network

  * **Abnormal detection**
    * Detect faults in the building system
    

### Getting started

* Prerequisites
 * [requirements.txt](https://github.com/jhyun0919/EnergyData_jhyun/blob/master/requirements.txt)  

* Setup the environment  
 *  how to setup
   ```
   $ git clone https://github.com/jhyun0919/EnergyData_jhyun.git
   
   $ cd EnergyData_jhyun
   
   $ source energy_data_venv/bin/activate  
   
   $ pip install -r requirements.txt
   ```
  
### Running the codes
 * Preprocessing   
   ```
   # input: directory path
   # output: vectors in binary file
   
   $ python DATA2VEC.py <directory_path>
   ```
   
   1. parse bin files located in given **directory_path**
   2. unpickle bin data
   3. convert data into vectors
   4. pickle **vectors** into **bin file**
  
    
 * Clustering   
   ```
   # input: vectors in binary file
   # output: cluster_structure
   
   $ python VEC2CLUSTER.py <bin_file_path>
   ```
   
   1. parse **bin file** designated by input argument
   2. make and save **cluster_structure**
  
   ---

   ```
   # input: directory path
   # output: cluster_structure
   
   $ python DATA2CLUSTER.py <bin_file_path>
   ```
   
   1. parse bin files located in given **directory_path**
   2. unpickle bin data
   3. convert data into vectors
   4. make and save **cluster_structure**

  
   
 * (Optional) Visualuzation
   ```
   # input: directory path of energy data
   # output: graph figures of energy data
   
   $ python DATA2GRAPH.py <directory_path>
   ```
   
   1. parse bin files located in given **directory_path**
   2. create a "/graph" folder in given **directory_path**
   3. draw and save **graph figures**  
     
   --- 

   ```
   # input: binary file of vectors
   # output: graph figures of vectors
   
   $ python VEC2GRAPH.py <directory_path>
   ```
  
   1. parse **bin file** designated by input argument
   2. create a "/graph" folder in given **directory_path**
   3. draw and save **graph figures**
    
  ---

  ```
  # input: binary file of cluster structure
  # output: classified graph figures
  
  $ python CLUSTER2GRAPH.py <bin_file_path>
  ```

   1. parse **bin file** designated by input argument
   2. get cluster_structure from parsed data
   3. draws **graphs** and classifies into each folder  

 * Classifier
   ```
   # input: binary file of energy data
   # output: index of the cluster
   
   $ python CLASSIFIER.py <bin_file_path>
   ```
   
   1. parse **binary file** designated by input argument
   2. get energy data from parsed data
   3. **classify** the data with cluster_structure and return the **index of cluster**
   
 * Dependency modeling
   ```
   # input: binary file of cluster structure data
   # output: binary file of dependency model
   
   $python DEPENDENCY.py <bin_file_path>
   ```
   1. parse **binary file** designated by input argument
   2. get cluster_structure from parsed data
   3. make a **dependency model** in array format
   
 * Abnormal detection   
   ```
   # input:
   # output:
   
   $ python ...
   ```
  
========
### Upcoming & Further Study
 - [x] Data Preprocessing
 - [x] Clustering - affinity propagation
 - [x] Classifier - Gaussian Naive Bayesian
 - [x] Dependency modeling - nearest neighbors
 - [ ] Dependency modeling - baysesian network
 - [ ] Visualize cluster with t-SNE
 - [ ] Abnormal detection
 - [ ] Cluster Verification Strategies
  
  
  
