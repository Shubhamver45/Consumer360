import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def run_market_basket_analysis(df: pd.DataFrame, min_support=0.01, min_lift=1.2):
    """
    Performs Association Rule Mining to uncover purchase patterns (e.g. Bread -> Butter).
    Utilizes mlxtend Apriori algorithm.
    """
    # Prevent RAM explosions on 500k row datasets by limiting exactly to the top 150 most-linked items 
    top_products = df['description'].value_counts().nlargest(150).index
    df_filtered = df[df['description'].isin(top_products)]

    # Limit exactly to 10,000 invoices for memory safety (representative sample is sufficient for apriori)
    unique_invoices = df_filtered['invoice_no'].unique()
    if len(unique_invoices) > 10000:
        import numpy as np
        np.random.seed(42)
        sampled = np.random.choice(unique_invoices, 10000, replace=False)
        df_filtered = df_filtered[df_filtered['invoice_no'].isin(sampled)]

    # Group by invoice and product description, count items
    basket = (df_filtered.groupby(['invoice_no', 'description'])['quantity']
              .sum().unstack().reset_index().fillna(0)
              .set_index('invoice_no'))
    
    # Convert quantities to discrete binary attributes (1 if purchased, 0 if not)
    # Using simple boolean mapping for maximum compatibility across pandas versions
    basket_sets = (basket > 0).astype(int)
    
    # Filter out invoices with only 1 item to improve performance and relevance
    # Meaningless to perform association rules on single-item purchases
    basket_sets = basket_sets[(basket_sets > 0).sum(axis=1) >= 2]
    
    if basket_sets.empty:
        return pd.DataFrame()
        
    # Generate frequent itemsets via Apriori algorithm
    frequent_itemsets = apriori(basket_sets, min_support=min_support, use_colnames=True)
    
    if frequent_itemsets.empty:
        return pd.DataFrame()
        
    # Extract rules utilizing 'lift' metric to establish definitive combinations
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_lift, num_itemsets=len(basket_sets))
    
    # Sort for best insights (Highest Confidence & Lift)
    rules = rules.sort_values(['confidence', 'lift'], ascending=[False, False])
    
    # Convert frozensets to lists for easier output writing
    rules['antecedents'] = rules['antecedents'].apply(lambda x: list(x))
    rules['consequents'] = rules['consequents'].apply(lambda x: list(x))
    
    return rules
