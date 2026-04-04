import pandas as pd

def generate_cohorts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates an explicit Cohort Retention Matrix based directly on first purchase month.
    Visualized to observe customer drop-off over periods strictly matching Power BI matrices.
    """
    analysis_df = df.copy()
    
    # Establish transaction month
    analysis_df['transaction_date'] = pd.to_datetime(analysis_df['transaction_date'])
    analysis_df['InvoiceMonth'] = analysis_df['transaction_date'].dt.to_period('M')
    
    # Identify unique signup cohort grouping metric (first transaction ever)
    analysis_df['CohortMonth'] = analysis_df.groupby('customer_id')['transaction_date'].transform('min').dt.to_period('M')
    
    # Mathematical Cohort Index formulation
    def extract_month_int(series):
        return series.dt.year * 12 + series.dt.month
        
    invoice_month_int = extract_month_int(analysis_df['transaction_date'])
    # Need to convert back to timestamp to safely extract year/month
    cohort_month_int = extract_month_int(analysis_df['CohortMonth'].dt.to_timestamp())
    
    # Calculates elapsed months
    analysis_df['CohortIndex'] = invoice_month_int - cohort_month_int
    
    # Count unique customer identifiers per combination of cohort and progressive month
    cohort_data = analysis_df.groupby(['CohortMonth', 'CohortIndex'])['customer_id'].nunique().reset_index()
    
    # Dynamic pivot into standard retention matrix layout
    cohort_counts = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values='customer_id')
    
    # Absolute user counts transformed into relative retention percentages
    cohort_sizes = cohort_counts.iloc[:, 0]
    retention_matrix = cohort_counts.divide(cohort_sizes, axis=0) * 100
    
    # Round logic for clean frontend reporting
    return retention_matrix.round(2)
