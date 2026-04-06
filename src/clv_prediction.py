import pandas as pd
from lifetimes import BetaGeoFitter, GammaGammaFitter
from lifetimes.utils import summary_data_from_transaction_data

def predict_clv(df: pd.DataFrame, time_in_months: int = 6) -> pd.DataFrame:
    """
    Uses the Lifetimes library to mathematically predict Future Customer Value 
    and Churn "Probability Alive" leveraging the established BG/NBD models.
    """
    summary = summary_data_from_transaction_data(
        df, 
        customer_id_col='customer_id', 
        datetime_col='transaction_date', 
        monetary_value_col='total_amount',
        observation_period_end=df['transaction_date'].max()
    )
    
    summary_positive = summary[summary['frequency'] > 0]
    
    if len(summary_positive) < 50:
        print("Warning: Insufficient historical repeat-customer data. Returning basic data.")
        return summary.reset_index()
        
    try:
        # ==========================================
        # 1. Fit BG/NBD Model (Predicts Churn risk / Future Frequency)
        # ==========================================
        bgf = BetaGeoFitter(penalizer_coef=0.1)
        bgf.fit(summary['frequency'], summary['recency'], summary['T'])
        
        summary['prob_alive'] = bgf.conditional_probability_alive(
            summary['frequency'], summary['recency'], summary['T']
        )
        t_days = time_in_months * 30
        summary['predicted_purchases'] = bgf.conditional_expected_number_of_purchases_up_to_time(
            t_days, summary['frequency'], summary['recency'], summary['T']
        )
        
        # ==========================================
        # 2. Fit Gamma-Gamma Model (Predicts Monetary Value limits)
        # ==========================================
        ggf = GammaGammaFitter(penalizer_coef=0.1)
        ggf.fit(summary_positive['frequency'], summary_positive['monetary_value'])
        
        predicted_clv = ggf.customer_lifetime_value(
            bgf,
            summary.index,
            summary['frequency'],
            summary['recency'],
            summary['T'],
            summary['monetary_value'],
            time=time_in_months,
            discount_rate=0.01 
        )
        
        summary['Predicted_CLV'] = predicted_clv
    except Exception as e:
        print(f"Warning: CLV Models failed to converge (often happens with purely synthetic/randomized testing data). Returning raw matrix. Details: {str(e)}")
        summary['prob_alive'] = 1.0 # Default fallback
        summary['Predicted_CLV'] = summary['monetary_value'] # Default fallback
        
    return summary.reset_index()
