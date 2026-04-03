import pandas as pd
import numpy as np

def calculate_rfm_scores(df: pd.DataFrame, snapshot_date=None) -> pd.DataFrame:
    """
    Calculates RFM scores for each customer.
    Args:
        df: DataFrame containing ['customer_id', 'transaction_date', 'total_amount', 'invoice_no']
        snapshot_date: The date to calculate recency against (default is max date + 1 day)
    """
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    
    if snapshot_date is None:
        snapshot_date = df['transaction_date'].max() + pd.Timedelta(days=1)
        
    # Calculate R, F, M metrics
    rfm = df.groupby('customer_id').agg({
        'transaction_date': lambda x: (snapshot_date - x.max()).days,
        'invoice_no': 'nunique',
        'total_amount': 'sum'
    }).reset_index()
    
    rfm.rename(columns={
        'transaction_date': 'Recency',
        'invoice_no': 'Frequency',
        'total_amount': 'Monetary'
    }, inplace=True)
    
    # Calculate Quintiles (1-5 scale)
    # Recency: Lower days = Better (Score 5)
    rfm['R_score'] = pd.qcut(rfm['Recency'], q=5, labels=[5, 4, 3, 2, 1], duplicates='drop')
    
    # Frequency: Higher count = Better (Score 5)
    rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5])
    
    # Monetary: Higher spend = Better (Score 5)
    rfm['M_score'] = pd.qcut(rfm['Monetary'], q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')
    
    for col in ['R_score', 'F_score', 'M_score']:
        rfm[col] = pd.to_numeric(rfm[col])
        
    # Combined Frequency & Monetary Score
    rfm['FM_score'] = np.round((rfm['F_score'] + rfm['M_score']) / 2).astype(int)
    
    return rfm

def segment_customers(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    Assigns segments based on the predictive segments grid from the project requirements.
    R_score (1-5), FM_score (1-5)
    """
    def assign_segment(row):
        r = row['R_score']
        fm = row['FM_score']
        
        # Rigorous mapping mapped to the precise visualization required
        if r >= 4 and fm >= 4:
            return 'Champions'
        elif r == 3 and fm >= 4:
            return 'Loyal Customers'
        elif r <= 2 and fm >= 4:
            return "Can't Lose Them"
        elif r >= 4 and fm == 3:
            return 'Potential Loyalist'
        elif r >= 4 and fm == 2:
            return 'Recent Users'
        elif r >= 4 and fm <= 1:
            return 'Price Sensitive'
        elif r == 3 and fm == 3:
            return 'Needs Attention'
        elif r == 3 and fm <= 2:
            return 'Promising'
        elif r <= 2 and fm == 3:
            return 'Hibernating'
        elif r == 2 and fm <= 2:
            return 'About To Sleep'
        elif r <= 1 and fm <= 2:
            return 'Lost'
        else:
            return 'Hibernating' # Catch-all fallback
            
    rfm['Segment'] = rfm.apply(assign_segment, axis=1)
    return rfm
