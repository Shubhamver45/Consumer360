# 🎨 Power BI UI Replication Guide: Page 3 (Predictive CLV & Cohort)

This guide provides the exact click-by-click instructions to perfectly replicate the highly analytical "CLV & Cohort" page from your screenshot.

---

## 🏗️ Prelude: The DAX Measures
Before formatting the visuals, you need a few calculations to power the KPI cards.
Right-click your `clv_predictions` table (or whichever table holds your data) and create these Measures:

**1. Mean Predicted CLV:**
```dax
Mean Predicted CLV = AVERAGE(clv_predictions[Predicted_CLV])
```
**2. Max Predicted CLV:**
```dax
Max Predicted CLV = MAX(clv_predictions[Predicted_CLV])
```
**3. Customers Modelled:**
```dax
Customers Modelled = COUNTROWS(clv_predictions)
```

*(Optional) Create this in your `cohort_analysis` table:*
**4. Avg M1 Retention:**
```dax
Avg M1 Retention = AVERAGE(cohort_analysis[1])
```

---

## 🖌️ Step 1: Initial Page Setup
1. At the bottom of Power BI, click the `+` to add a new page (name it `CLV & Cohort`).
2. **The Header:** Copy/paste the green header block and the Page Navigator from Page 2. 
   - It will naturally update so the `CLV & Cohort` tab is now active and solid green.
3. Change the sub-title text below the navigator to `Predictive CLV & Cohort Retention`.

---

## 🟩 Step 2: Top 5 KPI Scorecards
Using the **Card (New)** visual, create 5 cards across the top:
1. **Mean Predicted CLV**: Drag in your new `Mean Predicted CLV` measure. Format as Currency ($).
2. **Max Predicted CLV**: Drag in your `Max Predicted CLV` measure.
3. **Predicted Purchases**: Drag in `predicted_purchases` from your CLV table and set it to **Average**.
4. **Avg M1 Retention**: Drag in your `Avg M1 Retention` measure.
5. **Customers Modelled**: Drag in your `Customers Modelled` measure.
*(Add your small text boxes underneath each reading exactly what the screenshot says: "Per customer | BG/NBD model", "↑ Top customer", etc.)*

---

## 📊 Step 3: CLV Distribution Histogram (Top Left)
1. Select the **Clustered Column Chart** visual.
2. **X-axis:** Drag in `Predicted_CLV`. 
   - *Crucial step:* Right-click it in the axis box and select **New Group**. Set "Bin Size" to `50` or `100` so it creates physical histogram buckets!
3. **Y-axis:** Drag in `customer_id` and set to **Count Distinct**.
4. **Formatting:**
   - **Data Colors:** Click the `fx` button next to Default Color. Format Style: Gradient (Based on Count of customer_id). Low = pale green, High = Dark forest green.
   - **Adding the Mean Line:** Go to the Analytics pane (Magnifying glass). Add an **X-Axis Constant Line**. Click `fx` and choose your `Mean Predicted CLV` measure. Make it a dashed black/dark green line.

---

## 🟢 Step 4: Prob. Alive vs Predicted CLV (Top Middle)
1. Select the **Scatter Chart** visual.
2. **X-axis:** `prob_alive` (Make sure it's set to "Don't summarize").
3. **Y-axis:** `Predicted_CLV` (Don't summarize).
4. **Legend:** Drag your `Segment` name column securely into the Legend bucket.
5. **Formatting:** Power BI will automatically color the dots. Change the dot transparency to `30%` or `50%` so overlapping dots are visible!

---

## 📉 Step 5: Avg CLV by Segment (Top Right)
1. Select the **Clustered Bar Chart**.
2. **Y-axis:** `Segment`.
3. **X-axis:** `Predicted_CLV` (Change aggregation to Average).
4. **Formatting:**
   - Go to Bars -> Color -> Click `fx` -> Rules.
   - Apply specific colors based on the screenshot: `Lost` = Red (`#D9534F`), `Can't Lose Them` = Red (`#D9534F`), `Needs Attention` = Orange/Yellow, and the rest your standard green palette.
   - Turn Data Labels ON and format them as Currency.

---

## 🗂️ Step 6: Cohort Retention Heatmap (%) (Bottom Area)
This is the most critical visual on the page.

Since your Python script already outputs `cohort_retention.csv` in a perfect matrix shape, we DO NOT use a Power BI Matrix visual—we use a flat **Table** visual!

1. Select the standard **Table** visual.
2. **Columns Bucket:** Drag in `CohortMonth` first. (Make sure it doesn't summarize).
3. After `CohortMonth`, sequentially drag in the numbered columns from the table: `0`, `1`, `2`, `3`, `4`, etc., up to `12`.
4. Click on these number columns in your Data pane and format them as a **Percentage (%)** from the top ribbon.
5. **The Heatmap Colors:** 
   - In the Visualizations pane, right-click the `0` column -> Conditional Formatting -> **Background Color**.
   - Format Style: **Gradient**.
   - Set the lowest number to White, and the highest to Dark Forest Green (`#1A4314`).
   - Also turn on **Font Color** conditional formatting so that dark backgrounds get White text!
   - Repeat this conditional formatting for columns `1`, `2`, etc. to complete the heatmap!
