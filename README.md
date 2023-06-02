# Evaluation of predictability of Turkish MP's affiliations using ML

This is a project for the CS 210 - Introduction to Data Science course @ Sabancı University. 

## Abstract

Politics in Türkiye is a very complex topic. Investigation of the overall ontribution of political parties to the law-making process is of upmost importance, since political process should not be stagnant. That is why we decided to create a dataset for the data of MP's from the 22th installment to the 27th installment of the TBMM to evaluate MP's performances. Various classifier models will be used to predict MP affiliation, such as being in support of the government or being in opposition, etc.

## Technical Information

* We use BeautifulSoup to parse the links of the MP's. this is handled by the save_mv_links.py folder.

* The ```save_my_jsons.py``` is a multi-threaded program. Therefore, it could get you IP-banned from TBMM servers. Use at your own discretion.

## Prerequisites and Dependencies

* This project requires Chrome 112 or above.
* Also, the ```chromedriver.exe``` that is suited for your Chrome version is required to be defined within the source codes. for this, refer to the [ChromeDriver](https://chromedriver.chromium.org/downloads) webpage.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies of this project.

```bash
pip install selenium
pip install requests
pip install bs4
pip install pandas
```

* The following Machine Learning libraries are also required.

```bash
pip install sklearn
pip install tensorflow
pip install keras
```

## Usage

These scripts are needed to be run in this exact order:
```bash
python save_mv_links.py
python save_my_jsons.py
python to_csv_file.py
```
* There is a Jupyter notebook present in this repository, that may be used for exploratory data analysis, trying different classifier models, etc.