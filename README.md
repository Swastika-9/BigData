# Big Data Programming Coursework

## Distributed Processing and Predictive Analysis of UK Bus Timetable Data

### Overview

This project analyses UK Bus Open Data Service (BODS) timetable data using **Apache Spark (PySpark)**. XML timetable datasets were collected from the Bus Open Data Service, parsed into structured CSV files, stored in MySQL, and analysed using distributed data processing techniques.

The project demonstrates a complete big data pipeline including:

* Data collection and preprocessing
* XML parsing
* Distributed processing using Apache Spark
* Spark SQL analysis
* Data storage using MySQL
* Machine Learning using Spark MLlib
* Data visualisation
* Performance optimisation with caching, repartitioning and Parquet storage

The processed dataset contains **over 115,000 journey pattern records**, satisfying the coursework requirement of analysing a large-scale dataset.

---

# Project Structure

```text
BigDataProject/
│
├── analysis/
│   └── bus_analysis.py
│
├── preprocessing/
│   ├── xml_parser.py
│   └── checkdata.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── clean/
│   └── output/
│
├── notebooks/
│   └── BigData_Bus_Analysis.ipynb
│
├── outputs/
│   ├── figures/
│   ├── sample_results/
│   └── spark_ui/
│
├── sql/
│
├── documentation/
│
├── report/
│
├── requirements.txt
└── README.md
```

---

# Dataset

Source:

UK Department for Transport – Bus Open Data Service (BODS)

The project uses publicly available XML timetable files which are parsed into structured CSV datasets.

Generated datasets include:

* journey_pattern_links.csv
* vehicle_journeys.csv
* operators.csv
* routes.csv
* route_links.csv
* services.csv
* stops.csv

---

# Technologies Used

* Python 3.x
* Apache Spark (PySpark)
* Spark SQL
* Spark MLlib
* Pandas
* Matplotlib
* MySQL
* SQLAlchemy
* Jupyter Notebook

---

# Installation

Clone the repository

```bash
git clone https://github.com/Swastika-9/BigData.git

cd BigData
```

Install Python packages

```bash
pip install -r requirements.txt
```

Install Apache Spark.

Install MySQL Server.

Download the MySQL JDBC Connector and place the JAR file in the project directory (or update the Spark configuration with its location).

---

# Running the Project

### Step 1

Parse XML files

```bash
python preprocessing/xml_parser.py
```

---

### Step 2

(Optional)

Verify generated datasets

```bash
python preprocessing/checkdata.py
```

---

### Step 3

Run the analysis

Either execute

```bash
python analysis/bus_analysis.py
```

or open

```
notebooks/BigData_Bus_Analysis.ipynb
```

and run every notebook cell sequentially.

---

# Project Workflow

1. Download XML timetable data
2. Parse XML into CSV datasets
3. Load CSV files into Spark
4. Repartition and cache data
5. Perform Spark SQL analysis
6. Import processed datasets into MySQL
7. Execute analytical queries
8. Build Machine Learning models
9. Compare model performance
10. Export Parquet datasets

---

# Machine Learning

The project predicts scheduled bus run times using Spark MLlib.

Models implemented:

* Linear Regression
* Decision Tree Regression
* Random Forest Regression

Features include:

* Journey frequency
* Origin stop frequency
* Destination stop frequency

Performance is evaluated using:

* RMSE
* MAE
* R² Score

---

# Spark Optimisations

The project demonstrates several Spark optimisation techniques including:

* Data repartitioning
* Data caching
* Broadcast joins
* Parquet storage
* Spark SQL temporary views

---

# Outputs

The repository contains:

* Processed datasets
* Machine learning predictions
* Charts and visualisations
* Spark SQL query outputs
* Sample execution results
* Spark UI screenshots

---

# Database

The processed datasets are imported into MySQL.

Included components:

* SQL import scripts
* Sample SQL queries
* Database schema (documentation folder)

---

# Repository Contents

The repository includes:

* PySpark analysis scripts
* Jupyter notebook
* XML preprocessing scripts
* Processed datasets
* Requirements file
* Documentation
* Output figures
* Spark UI screenshots

---

# Author

Swastika Pokharel

Coventry University

Big Data Programming Coursework
