# IDX Exchange Summer 2026 Data Analyst Internship

## Objectives
A Multiple Listing Service (MLS) is a private, cooperative database operated by a regional association of real estate brokers. This internship works with datasets originating from CRMLS - the California Regional Multiple Listing Service - one of the largeset MLS systems in the United States, covering much of Southern California.

The primary goal of this internship is to build an end-to-end real estate data analytics workflow, mirroring production pipelines used at major real estate companies like Zillow and Redfin. By the end of the program, interns will be able to:

- *Understand MLS data structures:*  interpret key listing and transaction fields such as ListPrice, ClosePrice, PurchaseContractDate, DOM
- *Clean and transform raw data:* use Python to perform EDA for dataset structuring and validation
- *Analyze market dynamics:* aggregate listings dataset and sold dataset to produe metrics for price trends, inventory levels, and agent/brokerage performance
- *Visualize insights:* transform analysis-ready datasets to Tableau and build interactive dashboards for business communication

## Resources
**Real Estate Data Analyst Primer**
Internal company guide covering MLS data structure, transaction lifecycle, key metrics, and analytics workflow. Required reading prior to analysis.

**FileZilla Client**
Extract monthly CRMLS CSV files from January 2024 to May 2026 for listings and sold datasets.

**St.Louis Federal Reserve (FRED)**
The FRED MORTGAGE30US series is published weekly (every Thursday) by Freddie Mac via the St. Louis Federal Reserve. The data can be fetched directly from FRED as a CSV—no API key required

## Getting Started

### Dependencies
The following softwares are required prior to reproducing program.

* **Python IDE:** Visual Studio Code
  * **Python3 Libraries:** pandas
* Tableau Desktop Public Edition

### Installing


#### Visual Studio Code

1. Download and install Visual Studio Code from:
   https://code.visualstudio.com
2. Launch Visual Studio Code.
3. Install the Python extension published by Microsoft from the Extensions marketplace.

#### Python 3 and Pandas

1. Download and install Python 3 from:
   https://www.python.org/downloads/
2. Verify the installation by running:

   ```bash
   python3 --version
   ```

3. Install the required Python library:

   ```bash
   pip3 install pandas
   ```

4. Verify the installation by running:

   ```bash
   python3 -c "import pandas; print(pandas.__version__)"
   ```

#### Tableau Desktop Public Edition

1. Download Tableau Public from:
   https://tableau.com/products/public/download
2. Install Tableau Public following the installation instructions.
3. Create a free Tableau Public account and sign in to access Tableau Public features.

### Executing Program

1. Clone this repository:

   ```bash
   git clone https://github.com/jennyk04/IDXExchange-Summer2026-DA.git
   ```

2. Navigate to the project directory:

   ```bash
   cd IDXExchange-Summer2026-DA
   ```

3. Extract and place all monthly MLS CSV files in the `csv/` folder.

4. Verify that the project structure matches the following format:

   ```text
   IDXExchange-Summer2026-DA/
   ├── case study/
   │       ├── ...
   ├── csv/
       ├── monthly_listing
   │       ├── CRMLSListing202401.csv
   │       ├── CRMLSListing202402.csv
   │       ├── ...
       ├── monthly_sold
   │       ├── CRMLSSold202401.csv
   │       ├── CRMLSSold202402.csv
   │       └── ...
   ├── py/
   │   ├── crmls_listed.py
   │   └── ...
   ├── resources/
   │   ├── ...
   ├── .gitignore
   └── README.md
   ```

5. Open the project folder in Visual Studio Code.

6. Run the Python scripts from the project root directory using:

   ```bash
   python3 py/<script-name>
   ```

## DA49 team information
While the data analysis was performed independently, interns were placed in teams to encourage communication and team building. Team members shared about the different ways to analyze datasets and troubleshoot errors. 

**Team members:** Jenny Kim, Sai Korada, Wuxun Li, Hsiang-Ling, Kacy Liu, Vaishnavi Muchokota, Alain Shi, Ying Wu
**Coach:** Yoshika Ino
