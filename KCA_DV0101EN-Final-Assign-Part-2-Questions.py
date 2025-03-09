import dash  # Import Dash framework for building web applications
import pandas as pd  # Import pandas for data handling and analysis
import plotly.express as px  # Import Plotly Express for easy graphing
import plotly.graph_objects as go  # Import Plotly Graph Objects for advanced graphing
from dash import Dash, Input, Output, callback, dcc, html, no_update  # Import necessary Dash components

# Load dataset from a URL
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
df = pd.read_csv(URL)  # Read CSV file from the URL and load into a pandas DataFrame
print("Data downloaded and read into a dataframe!")  # Print confirmation message

# Create a filtered DataFrame containing only recession period data
df_rec = df[df["Recession"] == 1]  # Select rows where the 'Recession' column value is 1

# Define dictionaries for formatting and renaming labels
vehicle_type_names = {  # Dictionary mapping incorrect vehicle type names to proper names
    "Supperminicar": "Super Mini Car",
    "Mediumfamilycar": "Medium Family Car",
    "Smallfamiliycar": "Small Family Car",
    "Sports": "Sports Car",
    "Executivecar": "Executive Car",
}
label_names = {  # Dictionary for renaming labels used in graphs
    "Automobile_Sales": "Automobile Sales",
    "Vehicle_Type": "Vehicle Type",
    "Advertising_Expenditure": "Advertising Expenditure",
    "unemployment_rate": "Unemployment Rate",
}
month_order = [  # List defining the order of months for consistency in plots
    "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

# Initialize Dash application
external_scripts = [{"src": "https://cdn.tailwindcss.com"}]  # External script for styling (Tailwind CSS)
app = Dash(
    __name__,  # Name of the application
    external_scripts=external_scripts,  # Load external styling scripts
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],  # Make responsive for mobile devices
)
# Prevent layout exceptions before callbacks execute
app.config.suppress_callback_exceptions = True  # Allows defining callbacks for components not yet in the layout

# Task 2.1: Define the layout of the dashboard
app.layout = html.Main(
    children=[
        html.H1(
            "Automobile Sales Statistics Dashboard",  # Title of the dashboard
            className="mt-8 text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl",  # Tailwind CSS classes for styling
        ),

        # Task 2.2: Create dropdowns for user input
        html.Div(
            [
                html.Label(
                    "Select Report Type:",  # Label for report type dropdown
                    className="text-base font-semibold text-gray-900",  # Styling
                    htmlFor="input-report",  # Associate label with dropdown
                ),
                html.P(
                    "Which report would you like to display, yearly or recession?",  # Instructional text
                    className="text-sm text-gray-500",  # Styling
                ),
                dcc.Dropdown(
                    options=[  # Dropdown options for selecting report type
                        {"label": "Yearly Statistics", "value": "Yearly"},
                        {"label": "Recession Period Statistics", "value": "Recession"},
                    ],
                    value="Yearly",  # Default value
                    id="input-report",  # Unique identifier
                ),
            ],
            className="mt-4",  # Styling
        ),
        html.Div(
            [
                html.Label(
                    "Year:",  # Label for year dropdown
                    className="text-base font-semibold text-gray-900",
                    htmlFor="input-year",
                ),
                html.P(
                    "Which year would you like to display for the yearly report?",  # Instructional text
                    className="text-sm text-gray-500",
                ),
                dcc.Dropdown(
                    sorted(df.Year.unique()),  # Populate dropdown with unique years from dataset
                    value=2005,  # Default year selection
                    id="input-year",  # Unique identifier
                    disabled=True  # Initially disabled (only enabled when 'Yearly' report is selected)
                ),
            ],
            className="mt-4",  # Styling
        ),

        # Task 2.3: Define graph sections for visualization
        html.Section(
            [
                dcc.Graph(id="plot-1"),  # Placeholder for first graph
                dcc.Graph(id="plot-2"),  # Placeholder for second graph
                dcc.Graph(id="plot-3"),  # Placeholder for third graph
                dcc.Graph(id="plot-4"),  # Placeholder for fourth graph
            ],
            className="flex flex-wrap items-center justify-center",  # Styling for responsive layout
        ),
    ],
    className="flex flex-col items-center",  # Center align main layout
)

# Task 2.4: Callback to enable/disable year dropdown based on report type
@callback(Output("input-year", "disabled"), Input("input-report", "value"))
def disable_year(report_value):
    if report_value == "Recession":  # If recession report is selected, disable year dropdown
        return True
    else:
        return False  # Enable year dropdown if yearly report is selected

@callback(
    [
        Output("plot-1", "figure"),  # First graph output
        Output("plot-2", "figure"),  # Second graph output
        Output("plot-3", "figure"),  # Third graph output
        Output("plot-4", "figure"),  # Fourth graph output
    ],
    [
        Input("input-report", "value"),  # Input for report type
        Input("input-year", "value"),  # Input for selected year
    ],
)
def display_graphs(report_value, entered_year):
    if report_value == "Recession":
        return recession_graphs()  # Generate graphs for recession periods
    else:
        return year_graphs(entered_year)  # Generate graphs for selected year

# Task 2.5: Generate graphs for recession period analysis
def recession_graphs():
    # Line Graph: Average Automobile Sales by Year during Recession Periods
    fig_line = px.line(
        df_rec[["Year", "Automobile_Sales"]].groupby("Year").mean().reset_index(),  # Group by year and compute mean sales
        x="Year",  # X-axis represents the year
        y="Automobile_Sales",  # Y-axis represents average automobile sales
        title="Average Automobile Sales by Year during Recession Periods",
        color_discrete_sequence=["#C45A9A"],  # Set line color
        labels=label_names,  # Apply custom labels
    )
    
    # Bar Graph: Average Sales by Vehicle Type during Recession Periods
    bar_df = (
        df_rec[["Vehicle_Type", "Automobile_Sales"]]
        .groupby("Vehicle_Type")
        .mean()
        .reset_index()
    )
    bar_df["Vehicle_Type"] = bar_df["Vehicle_Type"].map(vehicle_type_names)  # Map vehicle type names
    fig_bar_1 = px.bar(
        bar_df,
        x="Vehicle_Type",  # X-axis represents vehicle type
        y="Automobile_Sales",  # Y-axis represents average automobile sales
        title="Average Automobile Sales by Vehicle Type during Recession Periods",
        color_discrete_sequence=["#C45A9A"],
        labels=label_names,
    )
    
    # Pie Graph: Total Advertising Expenditure by Vehicle Type during Recession Periods
    pie_df = (
        df_rec[["Vehicle_Type", "Advertising_Expenditure"]]
        .groupby("Vehicle_Type")
        .sum()
        .reset_index()
    )
    pie_df["Vehicle_Type"] = pie_df["Vehicle_Type"].map(vehicle_type_names)
    fig_pie = px.pie(
        pie_df,
        values="Advertising_Expenditure",  # Values represent total ad expenditure
        names="Vehicle_Type",  # Categories are vehicle types
        title="Total Advertising Expenditure by Vehicle Type during Recession Periods",
        labels=label_names,
    )
    
    # Bar Graph: Automobile Sales by Vehicle Type Per Unemployment Rate during Recession Periods
    bar2_df = (
        df_rec[["unemployment_rate", "Vehicle_Type", "Automobile_Sales"]]
        .groupby(["Vehicle_Type", "unemployment_rate"])
        .sum()
        .reset_index()
    )
    fig_bar_2 = px.bar(
        bar2_df,
        x="unemployment_rate",  # X-axis represents unemployment rate
        y="Automobile_Sales",  # Y-axis represents total automobile sales
        color="Vehicle_Type",  # Color represents vehicle type
        labels=label_names,
        title="Automobile Sales by Vehicle Type Per Unemployment Rate during Recession Periods",
    )
    
    # Format legend and hover text for vehicle type
    fig_bar_2.for_each_trace(
        lambda t: t.update(
            name=vehicle_type_names[t.name],
            legendgroup=vehicle_type_names[t.name],
            hovertemplate=t.hovertemplate.replace(t.name, vehicle_type_names[t.name]),
        )
    )
    
    return [fig_line, fig_bar_1, fig_pie, fig_bar_2]  # Return all figures

# Task 2.6: Generate graphs for a selected year
def year_graphs(entered_year):
    # Filter DataFrame for the selected year
    df_year = df[df["Year"] == entered_year]
    
    # Line Graph: Yearly Average Automobile Sales
    df_line = df[["Year", "Automobile_Sales"]].groupby("Year").mean()
    fig_line = px.line(
        df_line,
        y="Automobile_Sales",  # Y-axis represents average sales
        labels=label_names,
        title="Yearly Average Automobile Sales",
        color_discrete_sequence=["#C45A9A"],
    )
    
    # Line Graph: Total Automobile Sales per Month in Selected Year
    fig_line_2 = px.line(
        df_year,
        x="Month",  # X-axis represents months
        y="Automobile_Sales",  # Y-axis represents sales
        labels=label_names,
        title=f"Total Automobile Sales per Month in {entered_year}",
        color_discrete_sequence=["#C45A9A"],
    )
    
    # Bar Chart: Average Monthly Automobile Sales by Vehicle Type in Selected Year
    df_bar = (
        df_year[["Vehicle_Type", "Automobile_Sales"]]
        .groupby("Vehicle_Type")
        .sum()
        .reset_index()
    )
    df_bar["Automobile_Sales"] = (
        df_bar["Automobile_Sales"] / 12  # Divide by 12 to compute monthly average
    )
    df_bar["Vehicle_Type"] = df_bar["Vehicle_Type"].map(vehicle_type_names)  # Map vehicle type names
    fig_bar = px.bar(
        df_bar,
        x="Vehicle_Type",  # X-axis represents vehicle type
        y="Automobile_Sales",  # Y-axis represents monthly sales
        labels=label_names,
        title=f"Average Monthly Automobile Sales by Vehicle Type in {entered_year}",
        color_discrete_sequence=["#C45A9A"],
    )
    
    # Pie Graph: Total Advertising Expenditure by Vehicle Type in Selected Year
    pie_df = (
        df_year[["Advertising_Expenditure", "Vehicle_Type"]]
        .groupby("Vehicle_Type")
        .sum()
        .reset_index()
    )
    pie_df["Vehicle_Type"] = pie_df["Vehicle_Type"].map(vehicle_type_names)
    fig_pie = px.pie(
        pie_df,
        values="Advertising_Expenditure",  # Values represent total ad expenditure
        names="Vehicle_Type",  # Categories are vehicle types
        labels=label_names,
        title=f"Total Advertising Expenditure by Vehicle Type in {entered_year}",
    )
    
    return [fig_line, fig_line_2, fig_bar, fig_pie]  # Return all figures

# Run the Dash application
if __name__ == "__main__":
    app.run_server()  # Start the web server to run the dashboard

#This python is references to rheera in github and added explanation. ONLY for practice project and will delete this soon to make my own.