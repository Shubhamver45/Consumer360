# 🎨 Power BI UI Replication Guide: Page 2 (RFM Segmentation Engine)

This guide provides the exact click-by-click instructions to perfectly replicate the "RFM Segmentation Engine" page from your screenshot.

---

## 🏗️ Prelude: The Missing DAX Measures
To populate the new KPI cards and charts on this page, you need two new specific metrics. 
Go to the **Data** tab on the far right, right-click your `rfm_scores` table, and create these new measures:

**1. Champion Avg LTV:**
```dax
Champion Avg LTV = 
CALCULATE(
    AVERAGE(rfm_scores[Monetary]), 
    rfm_scores[Segment] = "Champions"
)
```

**2. Network Avg Spend:**
```dax
Network Avg Spend = 
AVERAGE(rfm_scores[Monetary])
```

---

## 🖌️ Step 1: Initial Page Setup
1. At the bottom of Power BI, click the `+` to add a new page (or select your existing `RFM Segmentation` page).
2. **The Header:** Just copy/paste the entire green header block and the Page Navigator from Page 1!
   - Because you are using the native Page Navigator, it will naturally update so the `RFM Segmentation` tab is now the solid green active one.
3. Change the sub-title text below the navigator to `RFM Segmentation Engine`.

---

## 🟩 Step 2: Top 5 KPI Scorecards
Using the **Card (New)** visual, create 5 cards across the top just like Page 1:
1. **Champions**: Drag in `customer_id` from `rfm_scores`. Right-click it and set to "Count Distinct". Filter visual to `Segment = Champions`.
2. **Churn Risks**: Drag in `customer_id` (Count Distinct). In the Filter pane, filter this visual to `Segment` is `Lost`, `Hibernating`, and `Can't Lose Them`. (Format Callout Value Color to Red `#D9534F`).
3. **Champion Avg LTV**: Drag in the new `Champion Avg LTV` measure you just made.
4. **Network Avg Spend**: Drag in the new `Network Avg Spend` measure you just made.
5. **RFM Matrix**: Just insert a simple **Text Box** and type `5x5` in big green text (since this is a static project identifier).

---

## 🗂️ Step 3: The Giant 5x5 RFM Matrix (Left Side)
This beautiful heatmap is built using a fundamentally customized standard **Matrix** visual.

1. Select the **Matrix** visual from the visualizations pane.
2. **Rows:** Drag in `R_score`. (Click the drop-down arrow next to it in the box and ensure it says "Don't summarize").
3. **Columns:** Drag in `FM_score` (Don't summarize).
4. **Values:** Drag in `customer_id` (Set to "Count Distinct").
5. **Add the Segment Names to the boxes:** Drag the `Segment` field into the **Values** bucket directly *under* `customer_id`! Right-click it and choose **First**.
   - *Result: Now your matrix cells will display something like "396" on top and "Lost" directly underneath it!*
6. **The Heatmap Colors:** 
   - Click the Paintbrush icon (Format visual) -> **Cell elements** -> Turn **Background Color** ON.
   - Click the `fx` button. Format Style: **Gradient**. 
   - What field should we base this on?: Count of `customer_id`. 
   - Set the lowest number to pale green `#DCEABF` and the highest to Dark Forest green `#1A4314`.
   *(Note: Remember to reverse the Y-Axis Sorting from 5->1 by clicking the '...' on the top right of the visual so Recency 5 is at the top!)*

---

## 📊 Step 4: Customers per Segment (Top Right)
1. Select the **Clustered Bar Chart**.
2. **Y-axis:** `Segment`.
3. **X-axis:** `customer_id` (Count Distinct).
4. **Formatting (Specific Red/Green Rules):**
   - Go to Bars -> Color. You don't want a generic gradient here; you want explicit warning colors.
   - Click `fx` -> **Rules**.
   - Rule 1: If value = `Lost` -> Red (`#D9534F`).
   - Rule 2: If value = `Can't Lose Them` -> Red (`#D9534F`).
   - Leave the rest of the rules as varying shades of your green palette.

---

## 📉 Step 5: Avg Monetary Value per Segment (Middle Right)
1. Select the **Clustered Column Chart**.
2. **X-axis:** `Segment`.
3. **Y-axis:** `Monetary` (Change aggregation to Average).
4. **How to add that dashed "Avg" baseline:**
   - With the chart selected, click the **Magnifying Glass icon** (Analytics pane) next to the Paintbrush.
   - Open **Constant Line**. Click **Add line**.
   - Click the `fx` button next to Value and select your new `Network Avg Spend` measure! 
   - Set the visual line color to Dark Green/Dashed.

---

## ✅ Step 6: The "Validation Check Passed" Box (Bottom Left)
This is actually completely static! It's just a design element comparing your formulas for the client.
1. **Insert** -> **Shape** -> **Rectangle**. 
2. Change Shape to "Rounded Rectangle". Format the Fill color to very pale green (`#F4F9F4`) and the Border to bright green (`#8CC63F`).
3. **Insert** -> **Text box** and lay it perfectly on top of the shape.
4. Type in the validation statistics and color code the final output text green to explicitly highlight that the Champions segment accurately beats the network baseline.

---

## 📋 Step 7: Segment Action Priorities (Bottom Right)
Just like the validation box, this is a very clean **Text Box**.
Type out your business logic mappings (e.g. `Champions -> Premium Engagement`). Keep it simple, clean, remove all backgrounds to make it transparent, and use the font **Segoe UI** to match the rest of the layout seamlessly.
