import streamlit as st
import pandas as pd
import altair as alt

# 1. Configure Dashboard
st.set_page_config(page_title="K-Beauty Routine Matcher", layout="wide")
st.title("Korean Skincare Routine Matcher")

# --- DASHBOARD INTRO (ROUTINE STEPS) ---
st.markdown("### 🌸 The 5-Step K-Beauty Philosophy")
st.markdown("Not sure where to start? The Korean skincare method relies on layering products from thinnest to thickest to maximize hydration and target specific concerns.")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.info("**1. Cleanse 🫧**\n\nDouble cleanse: oil-based first to melt SPF/makeup, then water-based to clean pores.")
with col2:
    st.info("**2. Prep 💧**\n\nToners and essences balance pH and prep the skin to absorb active ingredients.")
with col3:
    st.info("**3. Treat 🧪**\n\nSerums and ampoules deliver concentrated ingredients for acne, redness, or aging.")
with col4:
    st.info("**4. Moisturize 🧴**\n\nLotions and creams lock in hydration and seal all the previous layers.")
with col5:
    st.info("**5. Protect 🛡️**\n\nSunscreen (AM only) is the non-negotiable final step to prevent skin damage.")


# 2. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('https://raw.githubusercontent.com/maknaesuho/korean_skincare_analysis/refs/heads/main/streamlit/korean_skincare_master.csv')
    
    # Recreate the Safe_Formula_Flag 
    irritators = ['alcohol denat', 'fragrance', 'parfum', 'essential oil', 'linalool', 'limonene']
    pattern = '|'.join(irritators)
    
    df['Safe_Formula_Flag'] = (~df['Ingredients'].str.contains(pattern, case=False, na=False)).astype(int)
    
    return df

df = load_data()

# 3. Helper Functions for Top 5
def get_top_rated(data):
    mean_reviews = data["Review_Count"].mean()
    reliable_data = data[data["Review_Count"] > mean_reviews].copy()
    reliable_data['Product_Link'] = reliable_data['URL']
    
    solution = reliable_data.sort_values(by="Rating", ascending=False).head(5)
    return solution

def get_top_popular(data):
    popular_data = data.copy()
    popular_data['Product_Link'] = popular_data['URL']
    
    solution = popular_data.sort_values(by="Review_Count", ascending=False).head(5)
    return solution


# --- SIDEBAR FILTERS ---
st.sidebar.header("🎛️ Filter Your Routine")

# Primary Filters (Always Visible)
category_list = ["All"] + sorted(df['Category_Standardized'].dropna().unique().tolist())
category = st.sidebar.selectbox("📦 Product Category", category_list)

skin_type = st.sidebar.selectbox("👤 Skin Type", ["All", "Combination", "Normal", "Dry", "Oily", "Sensitive"])

# Group secondary filters in an expander
with st.sidebar.expander("🧪 Advanced Formulation Filters"):
    concerns = st.multiselect("Skin Concern", ["Acne", "Hydration", "Brightening", "Aging", "Redness"])
    
    ingredient_mapping = {
        "Contains Centella": "Has_Centella",
        "Contains Retinol": "Has_Retinol",
        "Contains Niacinamide": "Has_Niacinamide",
        "Contains Hyaluronic Acid": "Has_Hyaluronic_Acid",
        "Contains Ceramides": "Has_Ceramides",
        "Contains BHA/AHA": "Has_BHA_AHA",
        "Contains Panthenol": "Has_Panthenol",
        "Contains Snail Mucin": "Has_Snail_Mucin",
        "Contains Vitamin C": "Has_Vitamin_C",
        "Contains Peptides": "Has_Peptides"
    }

    hero_ingredient = st.selectbox(
        "Hero Ingredient", 
        ["Any"] + list(ingredient_mapping.keys())
    )

    irritant_mapping = {
        "No Alcohol": ["alcohol denat", "ethanol"],
        "No Fragrance": ["fragrance", "parfum", "linalool", "limonene"],
        "No Essential Oils": ["essential oil"]
    }

    exclude_irritants = st.multiselect(
        "Exclude Irritants",
        list(irritant_mapping.keys())
    )

# Group sliders in another expander
with st.sidebar.expander("💶 Price & Rating"):
    min_price_val = float(df['Current Price'].min())
    max_price_val = float(df['Current Price'].max())
    price_range = st.slider("Price Range (€)", min_value=min_price_val, max_value=max_price_val, value=(0.0, 50.0))
    min_rating = st.slider("Minimum Rating", min_value=0.0, max_value=5.0, value=4.0, step=0.1)


# --- FILTERING LOGIC ---
filtered_df = df.copy()

if category != "All":
    filtered_df = filtered_df[filtered_df['Category_Standardized'] == category]

if skin_type != "All":
    col_name = f"Skin_Type_{skin_type}"
    if col_name in filtered_df.columns:
        filtered_df = filtered_df[filtered_df[col_name] == 1]

for concern in concerns:
    col_name = f"Concern_{concern}"
    if col_name in filtered_df.columns:
        filtered_df = filtered_df[filtered_df[col_name] == 1]

if hero_ingredient != "Any":
    target_col = ingredient_mapping[hero_ingredient]
    if target_col in filtered_df.columns:
        filtered_df = filtered_df[filtered_df[target_col] == 1]

if exclude_irritants and 'Ingredients' in filtered_df.columns:
    for irritant in exclude_irritants:
        patterns = irritant_mapping[irritant]
        regex_pattern = '|'.join(patterns)
        filtered_df = filtered_df[~filtered_df['Ingredients'].str.contains(regex_pattern, case=False, na=False)]

filtered_df = filtered_df[
    (filtered_df['Current Price'] >= price_range[0]) & 
    (filtered_df['Current Price'] <= price_range[1]) &
    (filtered_df['Rating'] >= min_rating)
]


# --- MAIN DASHBOARD AREA ---
st.markdown("---")

# Create 3 distinct tabs
tab1, tab2, tab3 = st.tabs(["🛍️ Product Matches", "📊 Market Insights", "🏆 Top Recommendations"])

with tab1:
    st.subheader(f"Product Results ({len(filtered_df)} matches)")
    
    # Added 'URL' to the display columns
    display_columns = ['Brand', 'Product Name', 'Category_Standardized', 'Current Price', 'Rating', 'Review_Count', 'URL']
    available_columns = [col for col in display_columns if col in filtered_df.columns]

    st.dataframe(
        filtered_df[available_columns], 
        use_container_width=True, 
        hide_index=True,
        height=800,
        column_config={
            "Brand": st.column_config.TextColumn("Brand 🏷️"),
            "Product Name": st.column_config.TextColumn("Product Name ✨"),
            "Category_Standardized": st.column_config.TextColumn("Category 📦"),
            "Current Price": st.column_config.NumberColumn(
                "Price 💶",
                help="Current retail price",
                format="€%.2f"
            ),
            "Rating": st.column_config.NumberColumn(
                "Rating ⭐",
                help="Average customer rating (0-5)",
                format="%.1f"
            ),
            "Review_Count": st.column_config.ProgressColumn(
                "Review Volume 📈",
                help="Total number of consumer reviews",
                format="%d",
                min_value=0,
                max_value=int(df['Review_Count'].max()) if not df.empty else 1000
            ),
            "URL": st.column_config.LinkColumn(
                "Store Link 🔗",
                display_text="View on Store"
            )
        } # <-- Make sure this closing brace is here!
    )     # <-- And this closing parenthesis is here!

with tab2:
    st.subheader("Market Insights for Your Selection")
    
    if not filtered_df.empty:
        col_metric1, col_metric3, col_metric2 = st.columns(3)
        
        with col_metric1:
            if 'Review_Count' in filtered_df.columns and 'Review_Count' in df.columns:
                filtered_reviews = filtered_df['Review_Count'].sum()
                total_all_reviews = df['Review_Count'].sum()
                
                if total_all_reviews > 0:
                    demand_pct = (filtered_reviews / total_all_reviews) * 100
                    st.metric("Share of Total Consumer Demand", f"{demand_pct:.1f}%")
                else:
                    st.metric("Share of Total Consumer Demand", "0.0%")
            else:
                st.metric("Share of Total Consumer Demand", "N/A")
                
        with col_metric3:
            if 'Current Price' in filtered_df.columns:
                avg_price = filtered_df['Current Price'].mean()
                st.metric("Average Price", f"€{avg_price:.2f}" if pd.notna(avg_price) else "N/A")
            else:
                st.metric("Average Price", "N/A")
            
        with col_metric2:
            if 'Discount (%)' in filtered_df.columns:
                avg_discount = filtered_df['Discount (%)'].mean()
                st.metric("Average Discount", f"{avg_discount:.1f}%" if pd.notna(avg_discount) else "0.0%")
            else:
                st.metric("Average Discount", "N/A")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Average Rating of the Top 5 Most Popular Brands (Current Selection)**")
        
        top_brands = filtered_df.groupby('Brand')['Review_Count'].sum().nlargest(5).index
        major_brands_df = filtered_df[filtered_df['Brand'].isin(top_brands)]
        brand_avg_rating = major_brands_df.groupby('Brand')['Rating'].mean().sort_values(ascending=False).reset_index()

        brand_colors = {
            "BEAUTY OF JOSEON": "#4B5D4E",
            "COSRX": "#686A47",
            "ANUA": "#555555",
            "SKIN1004": "#EEBDB2",
            "PYUNKANG YUL": "#BBC0B3",
            "IUNIK": "#C17A5D",
            "SOME BY MI": "#F2DDD4",
            "ISNTREE": "#CE9B3A",
            "PURITO SEOUL": "#90A086",
            "DR.ALTHEA": "#A88468"
        }

        brand_avg_rating['Chart_Color'] = brand_avg_rating['Brand'].map(brand_colors).fillna('#D3D3D3')

        custom_chart = alt.Chart(brand_avg_rating).mark_bar().encode(
            x=alt.X('Brand:N', sort='-y', title=None, axis=alt.Axis(labelAngle=-45)),
            y=alt.Y('Rating:Q', title="Average Rating", scale=alt.Scale(domain=[0, 5])),
            color=alt.Color('Chart_Color:N', scale=None, legend=None) 
        ).properties(
            width=600,   
            height=350   
        )
        
        st.altair_chart(custom_chart, use_container_width=False)
    else:
        st.info("Adjust your filters to see market insights.")

with tab3:
    st.subheader("Top 5 Products Based on Your Criteria")
    
    if not filtered_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Highest Rated (Verified Volume)**")
            top_rated_df = get_top_rated(filtered_df)
            if not top_rated_df.empty:
                st.dataframe(
                    top_rated_df[['Brand', 'Product Name', 'Rating', 'Review_Count', 'Product_Link']], 
                    column_config={
                        "Product_Link": st.column_config.LinkColumn("Link", display_text="View on Store")
                    },
                    use_container_width=True, 
                    hide_index=True
                )
            else:
                st.info("Not enough review volume to calculate top rated safely.")
            
        with col2:
            st.markdown("**Most Popular (Review Count)**")
            top_popular_df = get_top_popular(filtered_df)
            st.dataframe(
                top_popular_df[['Brand', 'Product Name', 'Review_Count', 'Rating', 'Product_Link']], 
                column_config={
                    "Product_Link": st.column_config.LinkColumn("Link", display_text="View on Store")
                },
                use_container_width=True, 
                hide_index=True
            )
    else:
        st.warning("No products match your current filters. Try adjusting your sliders or unchecking some boxes.")
