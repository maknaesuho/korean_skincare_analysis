# 🧴 Demystifying K-Beauty: Market Analytics & Routine Matcher
**Live Dashboard:** [Korean Routine Finder](https://korean-routine-finder.streamlit.app/)  
**Ironhack Data Analytics Final Project**  
**Author:** Sofija Šarafejeva ([@maknaesuho](https://github.com/maknaesuho))

## 📌 Project Overview
Germany accounts for approximately 38% of the global K-beauty market share, making it one of Europe's top destinations for premium beauty brands. While consumers prioritize high-quality, scientifically supported formulations with safe, natural ingredients, the market is overwhelmingly saturated. 

**The Problem (The Paradox of Choice):** With thousands of competing products, complex ingredient lists, and systematically inflated retail ratings, consumers struggle to identify truly safe formulas versus marketing noise.

**The Solution:** This project utilizes web scraping, extensive data engineering, and interactive visualization to cut through the noise. The final product is a **Streamlit-powered Skincare Routine Matcher** that filters products based on verifiable ingredient safety, authentic consumer demand, and multi-criteria value scoring.

---

## 🛠️ Methodology: Data Pipeline

### 1. Web Scraping & Data Sourcing
* **Tool:** Selenium
* **Source:** Scraped 2,700+ products from `korean-skincare.de`.
* **Process:** Adapted UK URLs to extract standardized English product descriptions, ingredient lists, and consumer reviews into the foundational dataset (`korean_skincare_master.csv`).

### 2. Data Cleaning
* Cleaned and filtered the dataset to strictly skincare items (2,000+ products).
* Separated and categorized target variables: Ingredients, Skin Types, Concerns, and Skin Irritants.
* Standardized product categories and handled missing values/null anomalies.

### 3. Feature Engineering
* **`Safe_Formula_Flag`:** Built an algorithmic scanner to detect and exclude common irritants (e.g., drying alcohols found in 10.3% of the catalog, synthetic fragrances in 21.4%, and essential oils).
* **Hero Actives:** Created Boolean flags (`Has_<Active>`) to track trending beneficial ingredients like Centella Asiatica, Niacinamide, and Hyaluronic Acid.
* **Volume-Thresholding:** Implemented a rating threshold to filter out 1-review anomalies, ensuring recommendations are backed by authentic consumer adoption.

---

## 📊 Key Market Insights (EDA & Tableau)

Through extensive Exploratory Data Analysis (EDA) and Tableau dashboarding, several key market myths were busted:

* **The Price vs. Quality Myth:** There is a measurable **zero correlation** (r = -0.038) between product price and customer review ratings. The median satisfaction remains identical across budget and premium tiers (4.56), but budget segments drive significantly higher engagement (4x the review volume).
* **Rating Inflation:** Retail store ratings are systematically inflated by +0.99 to +1.14 stars and compressed into an artificial ceiling (4.65–4.90) compared to independent platforms (SkinSort), hiding true product irritation penalties.
* **Category Reliability:** Foundational steps like moisturizers and toners are "crowd pleasers" with high satisfaction and low variance. Conversely, sunscreens suffer from lower medians (4.38), and chemical exfoliants/treatments are highly polarizing.
* **Discounts:** Serums carry the deepest peak discounts in the market (up to 74.4%), followed closely by sunscreens.

---

## 💻 The Product: Streamlit Routine Matcher

The culmination of this data analysis is an interactive web dashboard built with Streamlit and Altair.

**Core Features:**
1. **Dynamic Filtering:** Users can filter the database by Skin Type, Specific Skin Concerns (Acne, Aging, Redness), and Budget.
2. **Safety First:** A strict toggle utilizes the `Safe_Formula_Flag` to hide products containing drying alcohols, harsh surfactants, and synthetic fragrances.
3. **Multi-Criteria Scoring Algorithm:** Products aren't just ranked by a simple 5-star average. The app balances:
   * Customer Rating (50%)
   * Log-normalized Review Volume (30%)
   * Price-Value Efficiency (20%)
4. **Visual Insights:** Embedded Altair charts providing real-time views of brand dominance and category breakdowns based on the user's selected filters.

---

## 🚀 Tech Stack
* **Languages:** Python
* **Data Manipulation:** Pandas, NumPy
* **Data Collection:** Selenium, BeautifulSoup
* **Data Visualization:** Tableau, Altair, Matplotlib / Seaborn
* **Web App Framework:** Streamlit

---

## 🔮 Future Implementations
* **Real-time Pipeline:** Implement scheduled web scraping pipelines to track real-time price drops and dynamically update the Streamlit app.
* **Machine Learning:** Deploy a collaborative filtering or content-based Machine Learning recommendation model to suggest holistic, multi-step routines rather than isolated products.

---

*This project was completed as the Final Project for the Ironhack Data Analytics Bootcamp.*
