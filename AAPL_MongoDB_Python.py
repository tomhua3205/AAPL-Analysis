import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pymongo import MongoClient

# Replace <password> with your actual MongoDB password
connection_string = "mongodb+srv://tomhua3205:Eg3402945@cluster0.jwjueqf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a MongoClient object
client = MongoClient(connection_string)

# Test the connection
try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("MongoDB connection successful!")
except Exception as e:
    print(f"Error: {e}")

# Connect to the 'Apple' database and the 'AAPL' collection
db = client['Apple']
collection = db['AAPL']

# Retrieve all documents from the collection
data = list(collection.find())

# Convert the data to a pandas DataFrame
df1 = pd.DataFrame(data)

# Ensure 'Date' is in datetime format
df1['Date'] = pd.to_datetime(df1['Date'])

# Sort the DataFrame by 'Date'
df1 = df1.sort_values('Date')

report_dates = [
    '2023-08-03',  # financial report release 23 q3
    '2023-11-02',  # financial report release 23 q4
    '2024-02-03',  # financial report release 24 q1
    '2024-05-03'   # financial report release 24 q2
]

product_dates = [
    '2023-06-13',  # mac studio, mac pro, macbook air
    '2023-09-22',  # apple watch 9 and ultr 2, iphone 15 family, airpods 2, earpods
    '2023-11-07',  # imac 24, macbook pro M3
    '2024-02-02',  # vision pro
    '2024-03-08',  # macbook air m3
    '2024-05-15'   # ipad air M2, ipad pro M4
]
report_dates = pd.to_datetime(report_dates)
product_dates = pd.to_datetime(product_dates)

# Create the main plot
fig = go.Figure()

fig.add_trace(go.Scatter(x=df1['Date'], y=df1['Close'], mode='lines', name='Close Price'))

# Add vertical lines for report dates
for vline_date in report_dates:
    fig.add_vline(x=vline_date, line=dict(color='blue', dash='dash'))
    fig.add_annotation(
        x=vline_date, 
        y=max(df1['Close']), 
        text='Report Date', 
        showarrow=True, 
        arrowhead=1, 
        ax=40,  # Move text to the right
        ay=-40,
        textangle=-90  # Rotate text to vertical
    )

# Add vertical lines for product dates
for vline_date in product_dates:
    fig.add_vline(x=vline_date, line=dict(color='red', dash='dash'))
    fig.add_annotation(
        x=vline_date, 
        y=max(df1['Close']), 
        text='Product Date', 
        showarrow=True, 
        arrowhead=1, 
        ax=-40,  # Move text to the left
        ay=-40,
        textangle=-90  # Rotate text to vertical
    )

# Customize the layout to make the plot bigger
fig.update_layout(
    title='AAPL Close Price Over Time',
    xaxis_title='Date',
    yaxis_title='Close Price',
    xaxis=dict(tickmode='array', tickvals=df1['Date'][::7], tickangle=45),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=20, r=20, t=40, b=20),
    template='plotly_white',
    width=900,  # Adjust the width
    height=600  # Adjust the height
)

# Save the plot as an HTML div string
plot_div = pio.to_html(fig, full_html=False)

##-----------------------------------------------------------------------##
# Smart Phone Market Last Year Plot
# Data for 2022 and 2023
data_2022 = {
    "Apple": 18.8,
    "Samsung": 21.7,
    "Xiaomi": 12.7,
    "OPPO": 9.5,
    "Transsion": 6.0
}
data_2023 = {
    "Apple": 20.1,
    "Samsung": 19.4,
    "Xiaomi": 12.5,
    "OPPO": 8.8,
    "Transsion": 8.1
}

# Calculate 'Other' percentages
data_2022['Other'] = 100 - sum(data_2022.values())
data_2023['Other'] = 100 - sum(data_2023.values())

# Labels and sizes
labels_2022 = list(data_2022.keys())
sizes_2022 = list(data_2022.values())

labels_2023 = list(data_2023.keys())
sizes_2023 = list(data_2023.values())

# Colors
colors = ['red', 'blue', 'green', 'orange', 'purple', 'grey']

# Create subplots for pie charts
fig_market = make_subplots(rows=1, cols=2, subplot_titles=("Smartphone Market Share 2022", "Smartphone Market Share 2023"), specs=[[{'type':'domain'}, {'type':'domain'}]])

# Plot 2022 data
fig_market.add_trace(go.Pie(labels=labels_2022, values=sizes_2022, marker=dict(colors=colors), name="2022"), 1, 1)

# Plot 2023 data
fig_market.add_trace(go.Pie(labels=labels_2023, values=sizes_2023, marker=dict(colors=colors), name="2023"), 1, 2)

# Update layout
fig_market.update_layout(
    title_text="Smartphone Market Share Comparison 2022 vs 2023",
    annotations=[dict(text='2022', x=0.18, y=0.5, font_size=20, showarrow=False),
                 dict(text='2023', x=0.82, y=0.5, font_size=20, showarrow=False)]
)
plot_market = pio.to_html(fig_market, full_html=False)

##-----------------------------------------------------------------------##
#Apple Revenue by Region Plot_Line
# Step 1: Import and read the CSV file
file_path = "apple_revenue.csv"
df = pd.read_csv(file_path)

# Step 2 and 3: Create 4 line charts, each area using a different color, with value on y-axis and time on x-axis
fig_RRLine = go.Figure()

# Plotting each region's revenue
for region in df["Region"]:
    fig_RRLine.add_trace(go.Scatter(x=df.columns[1:], y=df[df["Region"] == region].values[0][1:], mode='lines', name=region))

# Adding labels and title
fig_RRLine.update_layout(
    title='Apple Revenue by Region Over Time',
    xaxis_title='Time',
    yaxis_title='Revenue (in thousands)',
    xaxis=dict(tickmode='array', tickvals=df.columns[1:], tickangle=45),
    legend_title='Region',
    template='plotly_white'
)

# Show the plot
plot_RRLine = pio.to_html(fig_RRLine, full_html=False)

##-----------------------------------------------------------------------##
#Apple Revenue by Region_Pi
# Data for each quarter
quarters = ["2023 Q2", "2023 Q3", "2023 Q4", "2024 Q1"]

# Define colors for each region
colors = {
    "North America": "orange",
    "Europe": "red",
    "Japan": "green",
    "Greater China": "pink",
    "Rest of Asia Pacific": "blue"
}

# Step 1: Import and read the CSV file
file_path = "apple_revenue.csv"
df = pd.read_csv(file_path)

# Create subplots for pie charts
fig_RRPi = make_subplots(rows=2, cols=2, subplot_titles=[f'{quarter}' for quarter in quarters],
                    specs=[[{'type':'domain'}, {'type':'domain'}], [{'type':'domain'}, {'type':'domain'}]])

# Plot pie charts for each quarter
for i, quarter in enumerate(quarters):
    sizes = df[quarter].values
    labels = df["Region"].values
    color_list = [colors[label] for label in labels]

    # Determine the subplot position
    row = i // 2 + 1
    col = i % 2 + 1

    # Plot pie chart
    fig_RRPi.add_trace(go.Pie(labels=labels, values=sizes, marker=dict(colors=color_list), name=quarter), row, col)

# Update layout
fig_RRPi.update_layout(
    title_text="Apple Revenue Distribution by Region",
    showlegend=True
)

# Show the plot
plot_RRPi = pio.to_html(fig_RRPi, full_html=False)

##-----------------------------------------------------------------------##
# Apple Product Revenue_Line
# Read the CSV file
file_path = "apple_product_revenue.csv"
df = pd.read_csv(file_path)

# Create the figure
fig_PRLine = go.Figure()

# Plotting each product's revenue share over time
for product in df["Product"]:
    fig_PRLine.add_trace(go.Scatter(x=df.columns[1:], y=df[df["Product"] == product].values[0][1:], mode='lines', name=product))

# Adding labels and title
fig_PRLine.update_layout(
    title='Apple Product Revenue Share Over Time',
    xaxis_title='Time',
    yaxis_title='Revenue Share (%)',
    xaxis=dict(tickmode='array', tickvals=df.columns[1:], tickangle=45),
    legend_title='Product',
    template='plotly_white'
)

# Show the plot
plot_PRLine = pio.to_html(fig_PRLine, full_html=False)

##-----------------------------------------------------------------------##
#Apple Product Revenue_Pi
# Define colors for each product
colors = {
    "iPhone": "blue",
    "iPad": "green",
    "Mac": "red",
    "Services": "pink",
    "Wearables, Home and Accessories": "brown"
}

# Assuming the data is loaded into df
file_path = "apple_product_revenue.csv"
df = pd.read_csv(file_path)

# Data for each quarter
quarters = df.columns[1:]

# Create subplots for pie charts
fig_PRPi = make_subplots(rows=2, cols=2, subplot_titles=[f'{quarter}' for quarter in quarters],
                    specs=[[{'type':'domain'}, {'type':'domain'}], [{'type':'domain'}, {'type':'domain'}]])

# Plot pie charts for each quarter
for i, quarter in enumerate(quarters):
    sizes = df[quarter].values
    labels = df["Product"].values
    color_list = [colors[label] for label in labels]

    # Determine the subplot position
    row = i // 2 + 1
    col = i % 2 + 1

    # Plot pie chart
    fig_PRPi.add_trace(go.Pie(labels=labels, values=sizes, marker=dict(colors=color_list), name=quarter), row, col)

# Update layout
fig_PRPi.update_layout(
    title_text="Apple Product Revenue Share by Quarter",
    showlegend=True
)

# Show the plot
plot_PRPi = pio.to_html(fig_PRPi, full_html=False)

##-----------------------------------------------------------------------##
# HTML content with embedded plot
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apple Financial Data and News</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            
            margin: 0;
            padding: 0;
        }}
        header {{
            background-color: #f8f8f8;
            padding: 20px 0;
            text-align: center;
        }}
        header h1 {{
            margin: 0;
            font-size: 36px;
        }}
        nav {{
            display: flex;
            justify-content: center;
            background-color: #f0f0f0;
            padding: 10px 0;
        }}
        nav button {{
            margin: 0 5px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            border: 1px solid #ccc;
            background-color: white;
        }}
        main {{
            padding: 20px;
            border-top: 1px solid #ccc;
        }}
        main h2 {{
            font-size: 24px;
        }}
        main p {{
            font-size: 18px;
        }}
        .plot-container {{
            display: flex;
            justify-content: center;
            width: 100%;
            overflow-x: auto;
        }}
    </style>
    <script>
        function showContent(contentId) {{
            var contents = document.querySelectorAll('.content');
            contents.forEach(function(content) {{
                content.style.display = 'none';
            }});
            document.getElementById(contentId).style.display = 'block';
        }}
    </script>
</head>
<body>
    <header>
        <h1>Apple Financial Data and News</h1>
    </header>
    <nav>
        <button onclick="showContent('introduction')">Introduction</button>
        <button onclick="showContent('stock')">Stock Last 1 Year</button>
        <button onclick="showContent('smartphone')">Smart Phone Market Last Year</button>
        <button onclick="showContent('revenue-region')">Apple Revenue by Region</button>
        <button onclick="showContent('product-revenue')">Apple Product Revenue</button>
        <button onclick="showContent('conclusion')">Insights and Analysis From ChatGPT</button>
    </nav>
    <main>
        <div id="introduction" class="content" style="display: block;">
            <h2 align="center">Introduction</h2>
            <p>Welcome to this website, designed to analyze Apple's financial 
            performance over the past year. We provide insights using data on 
            stock prices, regional revenue, and product revenue share. Our 
            visualizations include stock price trends with key event markers, 
            quarterly regional revenue graphs, and product revenue 
            distributions. These analyses offer a clear understanding of how 
            product launches and financial reports impact Apple's market 
            performance, helping investors and enthusiasts make informed 
            decisions.</p>
        </div>
        <div id="stock" class="content" style="display: none;">
            <h2 align="center">Stock Last 1 Year</h2>
            <p></p>
            <div class="plot-container">{plot_div}</div> <!-- Embedding Plotly plot here -->
        </div>
        <div id="smartphone" class="content" style="display: none;">
            <h2 align="center">Smart Phone Market Last Year</h2>
            <p></p>
            <div class="plot-container">{plot_market}</div> <!-- Embedding Plotly plot here -->
        </div>
        <div id="revenue-region" class="content" style="display: none;">
            <h2 align="center">Apple Revenue by Region</h2>
            <p></p>
            <div class="plot-container">{plot_RRLine}</div> <!-- Embedding Plotly plot here -->
            <div class="plot-container">{plot_RRPi}</div> <!-- Embedding Plotly plot here -->
        </div>
        <div id="product-revenue" class="content" style="display: none;">
            <h2 align="center">Apple Product Revenue</h2>
            <p></p>
            <div class="plot-container">{plot_PRLine}</div> <!-- Embedding Plotly plot here -->
            <div class="plot-container">{plot_PRPi}</div> <!-- Embedding Plotly plot here -->
        </div>
         <div id="conclusion" class="content" style="display: none;">
            <h1 align="center">Insights and Analysis from ChatGPT</h1>

    <h2>1. Stock Price Trends:</h2>
    <ul>
        <li>The stock price shows significant volatility over the year.</li>
        <li>There's a notable peak around early August 2023, reaching above $195.</li>
        <li>A downward trend is visible from September 2023 to December 2023.</li>
        <li>The stock price dips significantly in January 2024 but starts to recover by March 2024.</li>
    </ul>

    <h2>2. Impact of Product Releases:</h2>
    <ul>
        <li>Early June 2023: Following a product release, there’s a sharp increase in the stock price, suggesting positive market reception.</li>
        <li>Early September 2023: Another product release coincides with the peak in stock price, indicating that new product launches generally boost investor confidence.</li>
        <li>Early January 2024: A product release during this period seems to have a minimal positive impact, as the price continues to fall.</li>
    </ul>

    <h2>3. Impact of Financial Reports:</h2>
    <ul>
        <li>Late July 2023: Following a financial report, the stock price continues to rise, indicating strong financial performance.</li>
        <li>Late October 2023: Another financial report coincides with the end of the stock's peak, followed by a decline, possibly due to market corrections or unmet expectations.</li>
        <li>Late January 2024: The stock price remains volatile, with a downward trend indicating possible negative reception of the financial report.</li>
        <li>Late April 2024: The latest financial report seems to have a positive impact, with a noticeable uptick in stock price.</li>
    </ul>

    <h2>4. Regional Revenue Trends:</h2>
    <ul>
        <li>North America consistently generates the highest revenue, peaking in Q4 2023 and then declining slightly in Q1 2024.</li>
        <li>Europe follows a similar pattern with increasing revenue up to Q4 2023 before a minor drop.</li>
        <li>Greater China shows steady revenue, peaking in Q4 2023 but remains relatively stable compared to other regions.</li>
        <li>Japan and the Rest of Asia Pacific contribute the least to total revenue, with minimal fluctuations over the quarters.</li>
    </ul>

    <h2>5. Revenue Distribution by Region:</h2>
    <ul>
        <li>North America contributes the largest share of Apple's total revenue, ranging from about 42% to nearly 45%.</li>
        <li>Europe is the second-largest revenue contributor, holding a consistent share of around 25%.</li>
        <li>Greater China's share fluctuates between 17% and 19%, showing a steady but significant contribution.</li>
        <li>Japan and the Rest of Asia Pacific have smaller shares, typically below 10%, indicating lower but stable market performance.</li>
    </ul>

    <h2>6. Product Revenue Share:</h2>
    <ul>
        <li>iPhone remains the dominant product, consistently contributing around 50% of total revenue, peaking at 58.3% in Q4 2023.</li>
        <li>Services are the second-largest revenue source, with a steady share around 25%, indicating a significant and growing part of Apple's business model.</li>
        <li>Wearables, Home, and Accessories show a consistent contribution around 10%, indicating a stable but secondary revenue source.</li>
        <li>Mac and iPad have the smallest shares, around 6-9%, with little variation, highlighting their role as supplementary products rather than core revenue drivers.</li>
    </ul>

    <h1 align="center">Conclusions from ChatGPT</h1>

    <h2>1. Market Sensitivity to Events:</h2>
    <ul>
        <li>Apple’s stock price is highly sensitive to both product releases and financial reports.</li>
        <li>Positive receptions to new products and strong financial results generally lead to stock price increases.</li>
    </ul>

    <h2>2. Investor Sentiment:</h2>
    <ul>
        <li>Product launches are critical for maintaining investor confidence, often leading to price surges.</li>
        <li>Financial reports have mixed impacts; while they can boost prices when results exceed expectations, they can also lead to corrections or declines if results are disappointing or if market expectations are not met.</li>
    </ul>

    <h2>3. Volatility:</h2>
    <ul>
        <li>The plot indicates high volatility in Apple's stock price, influenced by external events and internal company milestones.</li>
        <li>Investors should be prepared for significant fluctuations around these key dates.</li>
    </ul>

    <h2>4. Seasonal and Event-Based Impact:</h2>
    <ul>
        <li>There are notable revenue peaks in Q4 2023, likely due to seasonal factors such as holiday sales and new product launches, followed by a typical decline in Q1 2024.</li>
        <li>The pattern suggests that Apple's revenue is highly influenced by product release cycles and seasonal buying trends, which are crucial for planning and forecasting.</li>
    </ul>

    <h2>5. Strategic Insights:</h2>
    <ul>
        <li>Maintaining innovation in the iPhone segment is crucial for sustaining high revenue levels.</li>
        <li>Continued growth in Services is essential for diversification and stability.</li>
        <li>Expanding market share in regions outside North America and Europe could help mitigate risks associated with over-reliance on these markets.</li>
    </ul>
        </div>
    </main>
</body>
</html>
"""

# Save the HTML content to a file
#with open("AAPL_MongoDB.html", "w") as file:
#    file.write(html_content)

