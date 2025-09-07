
# Polygon-StockApp

A **Streamlit web app** to explore stock data using the **Polygon.io API**. This app allows users to:

- View company details (name, ticker, market cap, homepage)
- Access key financial metrics (P/E ratio, EPS, dividend yield, revenue, net income, etc.)
- See historical stock data over the past 5 years
- Plot stock price trends using line charts

## Features

- **Search by stock symbol**: Enter any ticker (e.g., AAPL, TSLA) to get detailed information.
- **Financial dashboard**: Key metrics displayed using Streamlit’s metric widgets.
- **Historical data charts**: Interactive line charts showing price trends.
- **Secure API integration**: Polygon API key is required for access, kept safe via Streamlit sidebar input.

## Setup Instructions

1. **Clone this repository**:

```bash
git clone git@github.com:Daivik2605/Polygon-StockApp.git
cd Polygon-StockApp
````

2. **Create and activate a virtual environment**:

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# .\venv\Scripts\activate  # Windows
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Run the app**:

```bash
streamlit run main.py
```

5. **Enter your Polygon.io API key** in the sidebar to start fetching stock data.

---

## Dependencies

* [Streamlit](https://streamlit.io/) — for building interactive web apps
* [Polygon API client](https://pypi.org/project/polygon-api-client/) — to fetch stock and financial data
* [Plotly](https://plotly.com/python/) — for interactive charts
* [Pandas](https://pandas.pydata.org/) — for data manipulation
* setuptools — required for Polygon client

---

## Reference

This project is inspired by Polygon’s official tutorial:
[Build a Stock App with Polygon.io and Streamlit](https://polygon.io/blog/build-a-stock-app-with-polygon-io-and-streamlit)

---

## Notes

* Historical data may be limited based on the Polygon subscription plan.
* All prices are returned in USD.
* Make sure your `requirements.txt` is up-to-date before running the app.

---

## License

This project is released under the MIT License.
