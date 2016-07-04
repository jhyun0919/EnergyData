# Energy Data Anlysis

### Introduction

This is a series of process showing the effort to manage energy more efficiently through analyzing sensor data from certatin buildings  

##### < Conceptual Scheme >
 <img src="https://raw.githubusercontent.com/jhyun0919/EnergyData_jhyun/master/docs/images/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202016-06-01%20%EC%98%A4%ED%9B%84%204.58.48.jpg" alt="Drawing" style="width: 800px;"/> 
 
---
### Background
 
 * 건물의 높은 에너지 소비
 * 건물에는 여러 종류의 수많은 sensor들이 설치되어 data를 수집하고 있음
 * 낭비하는 에너지가 많음 --> 낮추고 싶음
 *  

---
### Energy Data Analysis

 * 건물에서 사용하는 에너지의 효율성을 개선하려면 정확하고 효율적인 방법으로 에너지 사용을 추적 & 분석할 수 있는 방법이 필요함
 * 분석된 data를 바탕으로 아래 과정을 통애 **energy efficiency를 개선**할 수 있음
  - **sensor data 사이 dependncy** 분석을 통해 **energy usage pattern을 파악**할 수 있음
  - **abnormal detection**으로 낭비되는 energy를 줄일 수 있음
    - 과거와는 다른 energy pattern를 감지
    - 같은 종류의 senor data에서 다른 energy pattern을 감지  

##### < System Blue Print >
 <img src="https://raw.githubusercontent.com/jhyun0919/EnergyData_jhyun/master/docs/images/blueprint.jpg" alt="Drawing" style="width: 500px;"/> 

---
### Methods of Analysis

 * Preprocess Sensor Data
  - [Preprocess](https://github.com/jhyun0919/EnergyData_jhyun/blob/master/docs/01.%20Preprocess.ipynb)
 * Build Simialrity Model(Matrix)
  - [Similarity](https://github.com/jhyun0919/EnergyData_jhyun/blob/master/docs/02.%20Similarity.ipynb)
 * Visualize Sensor Data
  - [Visualization](https://github.com/jhyun0919/EnergyData_jhyun/blob/master/docs/03.%20Visualization.ipynb)
 * Detect Abnormal Situation
  - [Abnormal Detection](https://github.com/jhyun0919/EnergyData_jhyun/blob/master/docs/04.%20Abnormal%20Detection.ipynb)

---
### Future Works

-[] Visualize via HeatMap
-[] Visualize via Network
-[] Abnormal Detection
 
---
### References

 * 



