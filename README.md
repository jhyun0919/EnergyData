# Energy Data Anlysis

This is a series of process showing the effort to manage energy more efficiently through analyzing data from certatin buildings.

  * **Preprcessing**
    * Interpolation
    * Normalization
    * Vectorization
  
  * **Clustering** - unsing unsupervised learning algorithm  
      (_yet clusters are not verified, need to give valid and meaningful identities for each clusters_)
    * K-means
    * Affinity propagation
    * Baysesian network
    
  * **Abnormal detection**
    * Detect faults in the building system
    

### Getting started

* Prerequisites
 * [requirements.txt](https://github.com/jhyun0919/EnergyData_jhyun/blob/master/requirements.txt)  

* Setup the environment  
 *  how to setup
   ```
   $ git clone https://github.com/jhyun0919/EnergyData_jhyun.git  
   
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
   4. pickle vectors into bin file
  
    
 * Clustering   
   ```
   # input: vectors in binary file
   # output: clusters, (optional clustered graph figures)
   
   $ python VEC2CLUSTER.py <bin_file_path>
   ```
   
   1. parse bin file desigated by input argument
   2. return a cluster
   3. it also allows you to check the cluster through classified graph figures
   
   
 * (Optional) Visualuzation
   ```
   # input: directory path
   # output: binary files in graph figures
   
   $ python DATA2GRAPH.py <directory_path>
   ```
   
   1. parse bin files located in given **directory_path**
   2. create a "/graph" folder in given **directory_path**
   3. draw and save graph figures  
     
   
   ```
   # input: vectors in binary file
   # output: vectors in graph figures
   
   $ python VEC2GRAPH.py <directory_path>
   ```
  
   
   1. parse bin files located in given **directory_path**
   2. create a "/graph" folder in given **directory_path**
   3. draw and save graph figures
    

 * Abnormal detection   
   ```
   $ python ...
   ```
  
---
### Upcoming & Further Study
 - [x] Data Preprocessing
 - [x] Clustering
 - [ ] Baysesian network
 - [ ] Abnormal detection
 - [ ] Cluster Verification Strategies
  
  
  
