# Energy Data Anlysis

### Introduction

This is a series of process showing the effort to manage energy more efficiently through analyzing data from certatin buildings  

##### < Conceptual Scheme >
 <img src="https://raw.githubusercontent.com/jhyun0919/EnergyData_jhyun/master/docs/images/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202016-06-01%20%EC%98%A4%ED%9B%84%204.58.48.jpg" alt="Drawing" style="width: 800px;"/> 

---
### Background
 
 * 건물의 높은 에너지 소비
 * 낭비하는 에너지 high --> 낮추고 싶음
 * 건물에서 사용하는 에너지를 정확하고 효율적인 방법으로 추적 & 분석할 수 있는 방법이 필요함
 * 분석된 data를 바탕으로 아래 과정을 통애 **energy efficiency를 개선**할 수 있음
  - **data 간 dependncy** 분석을 통해 **energy usage pattern을 파악**할 수 있음
  - **abnormal detection**으로 낭비되는 energy를 줄일 수 있음
    - 과거와는 다른 energy pattern를 감지
    - 같은 종류의 senor data에서 다른 energy pattern을 감지  
 
---
### Methods of Analysis

 * Data Preprocess
  - [Data Preprocessing](https://github.com/jhyun0919/EnergyData_jhyun/blob/master/docs/01_01.%20Data%20Preprocessing.ipynb)
  - [Save Preprocessed Data](https://github.com/jhyun0919/EnergyData_jhyun/blob/master/docs/01_02.%20Save%20Preprocessed%20Data.ipynb)
 * Build Simialrity Matrix & Write Similarity Report
  - [Build Similarity Model](https://github.com/jhyun0919/EnergyData_jhyun/blob/master/docs/02_01.%20Build%20Similarity%20Model.ipynb)
  - [Write Simialrity Report](https://github.com/jhyun0919/EnergyData_jhyun/blob/master/docs/02_02.%20Write%20Similarity%20Report.ipynb)
 * Visualize into Weighted-Graph (Network)
  - [Show Similarity Weighted-Graph](https://github.com/jhyun0919/EnergyData_jhyun/blob/master/docs/02_03.%20Show%20Similarity%20Weighted-Graph.ipynb)
 

---
### Future Works

 * **Energy usage pattern**를 정확하고 효율적으로 파악하는 것이 완료된 후, 분석 모델에서 나아가 **실시간 요금제(Real Time Pricing)**가 **OpenADR**과 같은 인터페이스를 통해 연계된다면, **Machine Learning**을 바탕으로 **가격의 효율 개선(price efficiency)**을 노릴 수 있을 것으로도 전망됨
 * 
 
---
### References

 * 



