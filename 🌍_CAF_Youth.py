import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="CAF U17/U20 Top Players", layout="wide", page_icon='🌍')

st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
        }
        .stDataFrame {
            border: 1px solid #c8102e !important;
        }
        .stButton > button {
            background-color: #c8102e !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)


st.sidebar.image("TAP Logo.png", width=300)
league_option = st.sidebar.selectbox("Select League", ["CAF U17", "CAF U20"])
apply_button = st.sidebar.button("Apply Filter")

# Mapping for file paths
file_map = {
    "CAF U17": "Player Season Stats - CAF U17.xlsx",
    "CAF U20": "Player Season Stats - CAF U20.xlsx"
}

@st.cache_data
def load_data(league_name):
    file_path = file_map[league_name]
    df = pd.read_excel(file_path)
    return df

def compute_weighted_stats(df):
    weight_cap = 450
    for col in df.columns:
        if col.endswith("p90") and df[col].dtype != 'O':
            weight = np.minimum(df['Time Played'] / weight_cap, 1.0)
            df[col + "_weighted"] = df[col] * weight
    return df

# Session state management
if "selected_league" not in st.session_state:
    st.session_state.selected_league = league_option
    st.session_state.df_loaded = False

if league_option != st.session_state.selected_league:
    st.session_state.selected_league = league_option
    st.session_state.df_loaded = False

if apply_button:
    df = load_data(league_option)
    df = compute_weighted_stats(df)
    st.session_state.df = df
    st.session_state.df_loaded = True

# Main app logic
if st.session_state.get("df_loaded", False):
    df = st.session_state.df
    st.markdown(f"<h1 style='color:white;'>⭐ Top Players by Position Group ({league_option})</h1>", unsafe_allow_html=True)

    position_group_weights = {
        'Goalkeepers': {
            'Saves Made p90': 0.2,
            'Goals Conceded p90': -0.15,
            'Saves Made from Outside Box p90' : 0.15,
            'Saves Made from Inside Box p90': 0.1,
            'Penalties Saved p90': 0.1,
            'GK Successful Distribution p90': 0.15,
            'Successful Launches p90': 0.05,
            'Catches p90': 0.05,
            'Punches p90': 0.05,
            'Recoveries p90': 0.05,
            'Aerial Duels Won p90': 0.05,
            'Goals Conceded Inside Box p90': -0.05
        },
        'Full Backs': {
            'Goal Assists p90': 0.1,
            'Chances Created p90': 0.1,
            'Successful Crosses open play p90': 0.1,
            'Successful Crosses & Corners p90': 0.1,
            'Through balls p90': 0.05,
            'ProgressivePasses p90': 0.1,
            'FinalThirdPasses p90': 0.05,
            'Tackles Won p90': 0.05,
            'Total Clearances p90': 0.05,
            'Interceptions p90': 0.05,
            'Recoveries p90': 0.05,
            'Blocks p90': 0.05,
            'Duels won % p90': 0.05,
            'Total Fouls Won p90': 0.02,
            'Touches p90': 0.02,
            'Total Fouls Conceded p90': -0.01,
            'Yellow Cards p90': -0.01,
            'Total Red Cards p90': -0.01
        },
        'Center Backs': {
            'Total Clearances p90': 0.1,
            'Interceptions p90': 0.1,
            'Recoveries p90': 0.1,
            'Tackles Won p90': 0.1,
            'Blocked Shots p90': 0.05,
            'Blocks p90': 0.05,
            'Aerial Duels won p90': 0.1,
            'Ground Duels won p90': 0.05,
            'Duels won % p90': 0.05,
            'Goals Conceded Inside Box p90': -0.05,
            'Goals Conceded p90': -0.05,
            'Open Play Pass Success % p90': 0.05,
            'ProgressivePasses p90': 0.05,
            'FinalThirdPasses p90': 0.02,
            'Successful Long Passes p90': 0.02,
            'Yellow Cards p90': -0.01,
            'Total Red Cards p90': -0.01,
            'Total Fouls Conceded p90': -0.01,
            'Set Pieces Goals p90': 0.02
        },
        'Midfielders': {
            'Goals p90': 0.15,
            'Attempts from Set Pieces p90': 0.05,
            'Goal Assists p90': 0.15,
            'Open Play Pass Success % p90': 0.1,
            'Through balls p90': 0.05,
            'FinalThirdPasses p90': 0.05,
            'ProgressivePasses p90': 0.1,
            'Chances Created p90': 0.1,
            'Successful Crosses & Corners p90': 0.05,
            'Touches p90': 0.05,
            'Dribbles success % p90': 0.05,
            'Dispossessed p90': -0.02,
            'Duels won % p90': 0.05,
            'Tackles Won p90': 0.05,
            'Recoveries p90': 0.05,
            'Times Tackled p90': -0.01,
            'Total Fouls Conceded p90': -0.01
        },
        'Wingers': {
            'Goals p90': 0.05,
            'Goal Assists p90': 0.1,
            'Chances Created p90': 0.15,
            'Successful Crosses & Corners p90': 0.1,
            'Successful Crosses open play p90': 0.1,
            'ProgressivePasses p90': 0.15,
            'FinalThirdPasses p90': 0.15,
            'Touches p90': 0.10,
            'Total Touches In Opposition Box p90': 0.05,
            'Dribbles success % p90': 0.1,
            'Overruns p90': -0.02,
            'Dispossessed p90': -0.02,
            'Total Fouls Won p90': 0.03,
            'Attempts from Set Pieces p90': 0.02,
            'Total Shots p90': 0.02,
            'Shots On Target ( inc goals ) p90': 0.05
        },
        'Strikers': {
            'Goals p90': 0.2,
            'Headed Goals p90': 0.05,
            'Goal Assists p90': 0.1,
            'Successful Lay-offs p90': 0.05,
            'Chances Created p90': 0.05,
            'ProgressivePasses p90': 0.05,
            'Total Shots p90': 0.1,
            'Shots On Target ( inc goals ) p90': 0.1,
            'Shots Per Goal p90': -0.05,
            'Conversion Rate p90': 0.05,
            'Set Pieces Goals p90': 0.03,
            'Minutes Per Goal p90': -0.03,
            'Winning Goal p90': 0.05,
            'Total Touches In Opposition Box p90': 0.05,
            'Aerial Duels won p90': 0.02,
            'Ground Duels won p90': 0.02,
            'Duels won % p90': 0.02,
            'Offsides p90': -0.02
        }
    }

    def rating_to_stars(value, mean, std):
        z = (value - mean) / std if std > 0 else 0
        if z >= 1.0:
            return "⭐⭐⭐⭐⭐"
        elif z >= 0.5:
            return "⭐⭐⭐⭐"
        elif z >= 0:
            return "⭐⭐⭐"
        elif z >= -0.5:
            return "⭐⭐"
        else:
            return "⭐"
    st.markdown("<i>Note: This Average Rating is calculated based on key stats specific to each position group.</i>", unsafe_allow_html=True)
    
    for group, stat_weights in position_group_weights.items():
        weighted_stats = {}
        for stat, weight in stat_weights.items():
            weighted_col = stat + '_weighted'
            if weighted_col in df.columns:
                weighted_stats[weighted_col] = weight

        if not weighted_stats:
            continue

        subset = df[df['Position Group'] == group].copy()
        subset['avg_rating'] = sum(
            subset[col] * weight for col, weight in weighted_stats.items()
        ) / sum(abs(w) for w in weighted_stats.values())

        subset['Most Played Position'] = subset['Most Played Position'].str.upper()
        subset.rename(columns={'shirt_number': 'Shirt Number', 'avg_rating': 'Average Rating'}, inplace=True)

        mean_rating = subset['Average Rating'].mean()
        std_rating = subset['Average Rating'].std()
        subset['Stars Rating'] = subset['Average Rating'].apply(lambda x: rating_to_stars(x, mean_rating, std_rating))

        top3 = subset.nlargest(3, 'Average Rating')[[
            "Match Name", 'Full Name', "Most Played Position", "Shirt Number", 'Team Name', 'Average Rating', 'Stars Rating'
        ]]
        top3.index = ["🥇 Rank 1", "🥈 Rank 2", "🥉 Rank 3"][:len(top3)]
        

        st.markdown(f"<h3 style='color:white;'>Top 3 {group}</h3>", unsafe_allow_html=True)
        
        st.dataframe(top3, use_container_width=True)
        
        #st.subheader(f"All Weighted Stats for {group}")
        #stat_cols = ['Full Name', 'Team Name'] + list(weighted_stats.keys()) + \
        #           [col.replace('_weighted', '') for col in weighted_stats.keys() if col.replace('_weighted', '') in subset.columns]
        #st.dataframe(subset[stat_cols])

        #st.subheader(f"All p90 Stats for {group}")
        #p90_cols = ['Most Played Position', 'Full Name', 'Team Name'] + \
        #          [stat for stat in stat_weights.keys() if stat in subset.columns]
        #st.dataframe(subset[p90_cols])


    with st.expander("📊 Show Full Position Group Weighting Details"):
        st.markdown("""
        ### 🧤 Goalkeepers
        - Saves Made 
        - Goals Conceded 
        - Saves Made from Outside Box   
        - Saves Made from Inside Box  
        - Penalties Saved   
        - GK Successful Distribution   
        - Successful Launches   
        - Catches 
        - Punches 
        - Recoveries  
        - Aerial Duels Won 
        - Goals Conceded Inside Box  

        ### 🛡️ Full Backs
        - Goal Assists 
        - Chances Created 
        - Successful Crosses open play 
        - Successful Crosses & Corners 
        - Through balls 
        - ProgressivePasses 
        - FinalThirdPasses 
        - Tackles Won 
        - Total Clearances 
        - Interceptions
        - Recoveries 
        - Blocks 
        - Duels won % 
        - Total Fouls Won 
        - Touches 
        - Total Fouls Conceded 
        - Yellow Cards
        - Total Red Cards 

        ### 🧱 Center Backs
        - Total Clearances 
        - Interceptions
        - Recoveries
        - Tackles Won 
        - Blocked Shots 
        - Blocks 
        - Aerial Duels won
        - Ground Duels won
        - Duels won % 
        - Goals Conceded Inside Box 
        - Goals Conceded   
        - Open Play Pass Success %  
        - ProgressivePasses 
        - FinalThirdPasses  
        - Successful Long Passes 
        - Yellow Cards 
        - Total Red Cards 
        - Total Fouls Conceded 
        - Set Pieces Goals 

        ### 🎯 Midfielders
        - Goals 
        - Attempts from Set Pieces 
        - Goal Assists 
        - Open Play Pass Success %
        - Through balls
        - FinalThirdPasses 
        - ProgressivePasses 
        - Chances Created 
        - Successful Crosses & Corners 
        - Touches
        - Dribbles success %
        - Dispossessed
        - Duels won %
        - Tackles Won   
        - Recoveries 
        - Times Tackled   
        - Total Fouls Conceded 

        ### 🌀 Wingers
        - Goals 
        - Goal Assists  
        - Chances Created 
        - Successful Crosses & Corners
        - Successful Crosses open play 
        - ProgressivePasses 
        - FinalThirdPasses 
        - Touches p90: 
        - Total Touches In Opposition Box  
        - Dribbles success % 
        - Overruns   
        - Dispossessed 
        - Total Fouls Won 
        - Attempts from Set Pieces 
        - Total Shots 
        - Shots On Target ( inc goals )

        ### 🎯 Strikers
        - Goals   
        - Headed Goals 
        - Goal Assists 
        - Successful Lay-offs 
        - Chances Created  
        - ProgressivePasses  
        - Total Shots 
        - Shots On Target ( inc goals )  
        - Shots Per Goal 
        - Conversion Rate 
        - Set Pieces Goals  
        - Minutes Per Goal 
        - Winning Goal
        - Total Touches In Opposition Box 
        - Aerial Duels won 
        - Ground Duels won  
        - Duels won % 
        - Offsides
        """)


else:
    st.info("👈 Please apply league selection from the sidebar to load data.")
