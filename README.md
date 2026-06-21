# Global Stock Market Analysis Dashboard

Welcome to my first software development project!

I am an Electrical Engineering student at North Carolina A&T State University with a passion for technology, data analysis, and problem-solving. This project was created to explore global stock market data through an interactive dashboard built with Python.

The application allows users to analyze stock performance, visualize historical trends, and interact with financial data through dynamic charts and tables. From data cleaning and preprocessing to dashboard development and version control, this project represents my first complete software engineering project and an important step in expanding my technical skillset beyond traditional engineering coursework.

## Technologies Used
- Python
- Pandas
- Streamlit
- Plotly
- Git & GitHub

## Skills Demonstrated
- Data Cleaning and Preprocessing
- Data Visualization
- Interactive Dashboard Development
- Version Control with Git
- Financial Data Analysis
- Software Development Fundamentals

## Project Features
- Interactive stock ticker selector
- Country, industry, and date range filters
- Key metrics including latest close, daily change, 52-week high, 52-week low, total return, and volatility
- Closing price chart with 20-day and 50-day moving averages
- Trading volume chart
- Daily return distribution chart
- Open, high, low, and close price chart
- Multi-stock closing price comparison
- Recent data table
- Download button for the selected stock data

## How to Run

1. Clone this repository:

```bash
git clone https://github.com/agyaboaten/stock-dashboard.git
cd stock-dashboard
```

2. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit dashboard:

```bash
streamlit run stock_dashboard.py
```

The dashboard uses `cleaned_stock_data.csv`, so that file should stay in the same folder as `stock_dashboard.py`.

## Repository Files
- `stock_dashboard.py` - Main Streamlit dashboard application
- `Dataset Understanding.ipynb` - Notebook used for data understanding and cleaning
- `World-Stock-Prices-Dataset.csv` - Original dataset
- `cleaned_stock_data.csv` - Cleaned dataset used by the dashboard
- `requirements.txt` - Python libraries needed to run the project
- `.gitignore` - Files and folders Git should ignore

## What I Learned
- How to clean and prepare a dataset using Pandas
- How to build an interactive dashboard with Streamlit
- How to create charts with Plotly
- How to organize a first software project with Git and GitHub
- How to improve a project with documentation and reusable setup instructions

## Future Improvements
- Deploy the dashboard with Streamlit Community Cloud
- Add more advanced stock comparison tools
- Add country and industry overview pages
- Add candlestick charts
- Move large datasets to Git LFS or a separate data release if the project grows

This project marks the beginning of my journey at the intersection of engineering, software development, and data analytics, and I look forward to building increasingly sophisticated tools and applications in the future.
