#  :camera: SpectroPhone: Enabling Material Surface Sensing with RearCamera and Flashlight LEDs

![Teaser Image](/Spectrophone_Logo.png)


This repository provides our code used for the paper: 
[`SpectroPhone: Enabling Material Surface Sensing with RearCamera and Flashlight LEDs`](https://dx.doi.org/10.1145/3411763.3451753)

Our contribution includes:
- **Dataset**
- **Application**

The repository is licensed under MIT licsense.



### Repository Structure

- Dataset: includes the recorded data
- Android App: Application for communicating with server, camera and additional hardware for controlling the LED
- Arduino: Software for the external RN2040 bluetooth connection
- Hardware: Eagle files for the board
- Phone case: case for the Huawei P20 smartphone
- Python Software: Server software for classifying images, training SVM models and viewing spectograms. Simply start main.py

## Dataset
Our dataset includes:
<details>
  <summary>30 different materials</summary>
  <p>prepared .csv files with calculated spectroscopic features</p>
</details>

![Teaser Image](/Spectrophone_Classes.png)



## Citation
If you use our app and/or dataset in your projects, please use the following BibTeX citation:
```
@inproceedings{10.1145/3411763.3451753,
author = {Schrapel, Maximilian and Etgeton, Philipp and Rohs, Michael},
title = {SpectroPhone: Enabling Material Surface Sensing with RearCamera and Flashlight LEDs},
year = {2021},
isbn = {978-1-4503-8095-9/21/05},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3411763.3451753 },
doi = {10.1145/3411763.3451753},
booktitle = {Extended Abstracts of the 2021 CHI Conference on Human Factors in Computing Systems},
articleno = {5},
numpages = {5},
keywords = {Material sensing, Pattern recognition, Mobile Interaction},
location = {Yokohama, Japan},
series = {CHI EA '21}
}
```

##
![HCI Group](/Institute.png)

This repository is provided by the Human-Computer Interaction Group at the University Hannover, Germany. The code was mainly developed by Philipp Etgeton during his masters thesis. For additional details, see our [CHI'21 Extended Abstract](https://dx.doi.org/10.1145/3411763.3451753). 
The dataset and code is licsened under MIT license. For inquiries, please contact maximilian.schrapel@hci.uni-hannover.de
<br>:camera: :heavy_plus_sign: :iphone: :arrow_right: :bar_chart:
