import streamlit as st
import pandas as pd
import ast

# Streamlit app title
st.title("Interactive Marketing Keyword Tagging App")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file with a 'Statement' column", type="csv")

# Dictionary editing section
st.sidebar.header("Edit Keyword Dictionaries")

# Default dictionaries
default_dictionaries = {
    'urgency_marketing': [
        'limited', 'limited time', 'limited run', 'limited edition', 'order now',
        'last chance', 'hurry', 'while supplies last', "before they're gone",
        'selling out', 'selling fast', 'act now', "don't wait", 'today only',
        'expires soon', 'final hours', 'almost gone'
    ],
    'exclusive_marketing': [
        'exclusive', 'exclusively', 'exclusive offer', 'exclusive deal',
        'members only', 'vip', 'special access', 'invitation only', 'premium',
        'privileged', 'limited access', 'select customers', 'insider',
        'private sale', 'early access'
    ]
}

dictionaries = {}
for dict_name, keywords in default_dictionaries.items():
    user_input = st.sidebar.text_area(f"{dict_name} (comma-separated)", ', '.join(keywords))
    try:
        keyword_list = [kw.strip() for kw in user_input.split(',') if kw.strip()]
        dictionaries[dict_name] = set(keyword_list)
    except Exception as e:
        st.sidebar.error(f"Error parsing {dict_name}: {e}")

# Function to find matches from dictionary
def find_matches(text, keyword_set):
    text_lower = text.lower()
    return [kw for kw in keyword_set if kw in text_lower]

# Process uploaded file
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if 'Statement' in df.columns:
        for dict_name, keyword_set in dictionaries.items():
            df[dict_name + '_matches'] = df['Statement'].astype(str).apply(lambda x: find_matches(x, keyword_set))

        st.write("Tagged Data:")
        st.dataframe(df)
    else:
        st.error("The uploaded file must contain a 'Statement' column.")
else:
    st.info("Please upload a CSV file to begin.")

