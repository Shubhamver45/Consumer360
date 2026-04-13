# 🎨 Power BI UI Replication Guide: Page 4 (Market Basket Analysis)

This guide provides the exact click-by-click instructions to perfectly replicate the highly analytical "Market Basket" UI from your screenshot.

---

## 🏗️ Prelude: The DAX Measures & Columns
Right-click your `market_basket_rules` table and create these 5 **Measures**:

**1. Total Rules:**
```dax
Total Rules = COUNTROWS(market_basket_rules)
```
**2. Avg Rule Confidence:**
```dax
Avg Rule Confidence = AVERAGE(market_basket_rules[confidence])
```
**3. Avg Lift Score:**
```dax
Avg Lift Score = AVERAGE(market_basket_rules[lift])
```
**4. Avg Support:**
```dax
Avg Support = AVERAGE(market_basket_rules[support])
```
**5. Peak Confidence:**
```dax
Peak Confidence = MAX(market_basket_rules[confidence])
```

Now, create these 2 **Calculated Columns** (Used for the table at the bottom):

**6. Rule Rank:** *(To sort the top 10)*
```dax
Rule Rank = RANKX('market_basket_rules', 'market_basket_rules'[confidence], , DESC, Dense)
```
**7. Action Button Details:** *(For the faux pill-buttons)*
```dax
Action Button = "Bundle ➔"
```

---

## 🖌️ Step 1: Initial Page Setup
1. Click the `+` at the bottom of Power BI to add a new page and name it `Market Basket`.
2. **The Header:** Copy and paste the solid green header block and Page Navigator from Page 3. 
   - It will natively highlight the `Market Basket` tab.
   - Adjust the sub-title underneath to: `Market Basket Analysis — Association Rule Mining`.
3. Insert two small text boxes on the far right underneath the header for the model info: `Apriori Algorithm via mlxtend | Office/Tech Product Affinity`.

---

## 🟩 Step 2: The 5 KPI Scorecards
Using the **Card (New)** visual, create 5 boxes across the top matching your layout:
- **Total Rules Mined**: Drag in `Total Rules`
- **Avg Rule Confidence**: Drag in `Avg Rule Confidence`. Format as `%`.
- **Avg Lift Score**: Drag in `Avg Lift Score`. Format to two decimals, and append an `x` under the custom format string or type it natively.
- **Avg Support**: Drag in `Avg Support`. Format as `%`.
- **Peak Confidence**: Drag in `Peak Confidence`. Format as `%`.

*(Insert the smaller text boxes underneath each reading precisely what your screenshot shows, e.g., "↑ Item B given A", "↑ Top rules threshold", etc.)*

---

## 📊 Step 3: Confidence Distribution (Top Left)
1. Select the **Clustered Column Chart** visual.
2. **X-axis:** Right-click the `confidence` column in the Data pane -> **New Group**. Set grouping to **Bins** with a size of `0.05`. Drag this new Bins column into the X-axis.
3. **Y-axis:** Drag in `antecedents` and set the aggregation to **Count**.
4. **Formatting:**
   - **Color:** Set bars to a soft pale green (`#CDE394` or similar).
   - **Median Line:** Go to the Analytics pane (the Magnifying Glass icon). Add a **Median Line**. Make it black, dashed, with a stroke width of 2.

---

## 🟢 Step 4: Support vs Lift Scatter Chart (Top Middle)
1. Select the **Scatter Chart** visual.
2. **Values / Details:** Drag in `antecedents`. This forces Power BI to plot a distinct dot for every rule rather than aggregating them into 1 dot!
3. **X-axis:** `support` (Do not summarize). Format the axis labels to display as percentages.
4. **Y-axis:** `lift` (Do not summarize).
5. **Formatting:**
   - Go to Markers -> Color -> Click the `fx` button.
   - Format Style: **Gradient**. Based on Average of `confidence`.
   - Lowest color = Pale Yellow/White (`#F9FCE5`), Highest color = Dark Forest Green (`#1A4314`).

---

## 📉 Step 5: Most Frequent Consequents (Top Right)
1. Select the **Clustered Bar Chart** visual.
2. **Y-axis:** Drag in `consequents`.
3. **X-axis:** Drag in `antecedents` and change the aggregation to **Count**.
4. **Formatting:**
   - Go to Bars -> Color -> Click `fx` (Conditional Formatting). 
   - Apply a Dark Green gradient scale based on Count of `antecedents`.
   - Turn Data Labels **ON**, ensuring they're positioned at the "Outside End" of the bars!

---

## 📋 Step 6: Top 10 Association Rules Table (Bottom Area)
1. Select a standard **Table** visual.
2. Drag your columns into the Values bucket in exactly this order:
   - `Rule Rank` (Rename visual header to `#`)
   - `antecedents` (Rename visual header to `Antecedents (If customer bought...)`)
   - `consequents` (Rename visual header to `Consequent (-> also buys)`)
   - `support`
   - `confidence`
   - `lift`
   - `Action Button` (Rename visual header to `Action`)
3. **Sorting:** Click the column header for `#` to sort Ascending (so 1 is at the top).
4. **Filtering to Top 10:** Open the Filter Pane on the far right. Find `Rule Rank` under "Filters on this visual". Set it to "is less than or equal to 10".
5. **Formatting the Faux Button:**
   - In the Visualizations pane, right-click the `Action Button` field -> Conditional Formatting -> **Background Color**.
   - Simply choose a solid bright green (e.g., `#ADD14C`). Apply it.
   - Also, optionally set the Font Color conditionally to White! This makes it look exactly like the clickable "Bundle ->" pills in your UI design.
