# 🎨 Power BI UI Replication Guide: The "Consumer360 Green Theme"

Follow these exact steps to pixel-perfectly replicate the gorgeous, green-themed "Sales Overview Dashboard" from your screenshot.

---

## 🏗️ Prelude: The New DAX Measures
Your selected UI requires a few new specific metrics (like Net Profit, Churn percentages, and Share %). 
Go to the **Data** tab on the far right, right-click your tables, and create these new measures:

**1. Simulated Net Profit (Assuming a 20% margin):**
```dax
Net Profit = [Total Revenue] * 0.20
```
**2. Segment Counters:**
```dax
Total Customers Value = DISTINCTCOUNT(fact_sales[customer_id])

Champions Count = CALCULATE(DISTINCTCOUNT(rfm_scores[customer_id]), rfm_scores[Segment] = "Champions")
Champions % of Base = DIVIDE([Champions Count], [Total Customers Value], 0)

Churn Risks Count = CALCULATE(DISTINCTCOUNT(rfm_scores[customer_id]), rfm_scores[Segment] IN {"Lost", "Hibernating", "Can't Lose Them"})
Churn Risks % of Base = DIVIDE([Churn Risks Count], [Total Customers Value], 0)
```
**3. Revenue Share % (for the bottom right table):**
```dax
Revenue Share % = DIVIDE([Total Revenue], CALCULATE([Total Revenue], REMOVEFILTERS(dim_customer)), 0)
```

---

## 🖌️ Step 1: Canvas & Background Setup
1. Click anywhere on the blank white background of your report.
2. Go to the **Format your report page** pane (the paintbrush icon).
3. Expand **Canvas background**.
4. Click **Color** -> **More colors** -> Type exactly: `#F4F6F4` (This gives that very faint, premium grey/green off-white background).
5. Set Transparency to `0%`.

---

## 🟩 Step 2: The Top Header Menu
1. Go to the top ribbon -> **Insert** -> **Shape** -> **Rectangle**.
2. Draw it across the entire top edge of the screen.
3. In its formatting, set Fill color to **White**, and turn **Border off**.
4. **The Reactive Tabs (Page Navigator):** Power BI has a built-in feature to automatically create clickable, dynamic, color-changing tabs!
   - Make sure you have created blank pages at the bottom of Power BI named exactly: `Overview & Sales`, `RFM Segmentation`, `CLV & Cohort`, and `Market Basket`.
   - On the top ribbon, go to **Insert** -> **Buttons** -> **Navigator** -> **Page navigator**.
   - A single horizontal bar containing buttons for every single page in your report will instantly appear!
5. **Formatting the Navigator (Making it match the image perfectly):**
   - Click your new Page Navigator visual. Go to your **Format** pane on the right.
   - Expand **Shape** -> Set it to **Rectangle**.
   - Expand **Style**. You'll see an "Apply settings to" dropdown immediately below it. 
   - **For Default State (Inactive Tabs):** Make sure the dropdown says "Default". Set Font Color to `#9FD171` (Light Green). Turn **Fill** to OFF (or 100% transparent).
   - **For Selected State (The active page):** Change the dropdown from "Default" to **"Selected"**. Set Font Color to **White** and Bold. Turn **Fill** ON and set it to `#478726` (Forest Green).
   - *Result:* Now, whenever you physically click a tab (Requires `Ctrl + Click` while editing in Desktop, but just a single left-click once published online), it will instantly navigate to that page, and the solid green highlight will automatically jump to whichever tab is active!
6. Add your "Consumer360" title on the top left.

---

## 🗂️ Step 3: The 5 KPI Scorecards
We will use the modern **Card (New)** visual so it matches the aesthetic perfectly.

1. Click the **Card (New)** visual. (Usually has a lightning bolt or looks like a split card in newer PBI versions. If you don't have it, use the standard "Card" visual).
2. Create 5 separate cards and drag these fields into them:
   - `Total Revenue`
   - `Net Profit`
   - `Total Customers Value`
   - `Champions Count`
   - `Churn Risks Count`
3. **Formatting every card (to match the screenshot):**
   - **Callout Value Color:** Dark Green `#478726`. *(Exception: Make the Churn Risks number Red `#D9534F`)*.
   - **Card Background:** Light Green Fill `#EAF2EA`.
   - **Border:** Solid, 1px, Color: `#CCDCCC`.
   - Add a smaller **Text Box** inside/under each card for the secondary numbers (e.g. type `+12% from last month` in green text, or `↓ 18.6% of base` in red text).

---

## 📈 Step 4: Monthly Revenue Trend (Combo Chart)
1. Select the **Line and clustered column chart** visual.
2. **X-axis:** Drag in your Months.
3. **Column Y-axis:** `Total Revenue`.
4. **Line Y-axis:** `MoM Growth`.
5. **Formatting:**
   - **Columns Color:** Extremely light green `#DCEABF`.
   - **Line Color:** Dark Green `#478726`.
   - **Line Style:** Set to **Dashed** with a stroke width of 2.
   - **Markers:** Turn ON. Choose the Triangle shape if available, or circles.
   - **Data Labels:** Turn ON, but apply it *only* to the Line series so the percentages show above the triangles.

---

## 📊 Step 5: Top Products by Revenue
1. Select the **Clustered bar chart** visual.
2. **Y-axis:** `description` (Product names).
3. **X-axis:** `Total Revenue`.
4. **Formatting (The Multi-Green Gradient):**
   - Go to Bars -> Color.
   - Click the little **`fx`** (Conditional Formatting) button next to the color.
   - Select Format style: **Gradient**.
   - What field should we base this on?: `Total Revenue`.
   - **Minimum Color:** `#C1E1A6` (Pale Green).
   - **Maximum Color:** `#478726` (Dark Forest Green).
5. Turn **Data labels** ON. Set position to "Outside end" and display units to "Millions".

---

## 🍩 Step 6: Revenue by Region
1. Select the **Donut chart** visual.
2. **Legend:** `country`.
3. **Values:** `Total Revenue`.
4. **Formatting the specific Slices:**
   - Expand Slices. You must manually color them to match the image precisely:
     - United Kingdom: `#1A4314` (Near Black-Green)
     - Germany: `#2E5B25` (Dark Green)
     - France: `#59A14F` (Mid Green)
     - Australia / USA / Others: `#9FD171` to `#DCEABF`.
5. **Data labels:** Set Label contents to "Percent of total".

---

## 📉 Step 7: Transaction Volume (Area chart)
1. Select the **Area chart** visual.
2. **X-axis:** Months.
3. **Y-axis:** Drag in `invoice_no` from `fact_sales`. Right-click it and select **Count (Distinct)**.
4. **Formatting:**
   - **Line Color:** `#478726`.
   - **Shade/Area Fill:** `#DCEABF` with Transparency set to `50%`.
   - **Markers:** Turn ON. Solid green dots.

---

## 📋 Step 8: Segment Revenue Breakdown
1. Select the standard **Table** visual.
2. **Columns:** Drag in `Segment`, `Total Revenue`, and `Revenue Share %`.
3. **Formatting the Colored Dots:**
   - On the Visualizations pane, right-click the `Segment` field -> **Conditional formatting** -> **Icons**.
   - Icon Layout: **Left of data**.
   - Icon Alignment: **Middle**.
   - Style: Colored Circles.
   - **Rules:** 
     - If value is strictly "Champions" -> Assign a Green Circle.
     - If value is strictly "Lost" -> Assign a Red Circle.
     - (Fill out the rest of the circles matching the shades in the image!)
4. **Values Formatting:** Click `Revenue Share %` in your Data pane and click the `%` button on the top ribbon so it formats as a clean percentage!

You are finished! By strictly setting these exact hex codes and toggles, your dashboard will absolutely identically mirror the UI screenshot provided.
