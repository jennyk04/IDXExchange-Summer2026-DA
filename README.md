# IDX Exchange Summer 2026 Data Analyst Internship

## Introduction

## Objectives

## Resources

## DA49 team information
introduction to the team, purpose of the team

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

1. Clone or download this repository:

   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:

   ```bash
   cd IDXExchange-Summer2026-DA
   ```

3. Place all monthly MLS CSV files in the `csv/` folder.

4. Verify that the project structure matches the following format:

   ```text
   IDXExchange-Summer2026-DA/
   ├── csv/
   │   ├── CRMLSListing202401.csv
   │   ├── CRMLSListing202402.csv
   │   ├── ...
   │   ├── CRMLSSold202401.csv
   │   ├── CRMLSSold202402.csv
   │   └── ...
   ├── py/
   │   ├── Listing.py
   │   └── ...
   └── README.md
   ```

5. Open the project folder in Visual Studio Code.

6. Run the Python scripts from the project root directory using:

   ```bash
   python3 py/Listing.py
   ```
