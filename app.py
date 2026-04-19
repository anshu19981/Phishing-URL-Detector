import streamlit as st
import joblib
import pandas as pd
import re
from urllib.parse import urlparse

# --- 1. Page Configuration ---
st.set_page_config(page_title="Phishing URL Detector", page_icon="🛡️", layout="centered")

# --- 2. Load Model ---
@st.cache_resource
def load_model():
    try:
        return joblib.load('phishing_detector_model.pkl')
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

# --- 3. Feature Extraction Function (PERMANENT FIX) ---
def get_features(url, model):
    parsed = urlparse(url)
    
    # Humare paas jo 15 features ka logic hai, wo yahan hai
    features_dict = {
        'url_length': len(url),
        'domain_length': len(parsed.netloc) if parsed.netloc else 0,
        'num_slash': url.count('/'),
        'has_ip_address': 1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url) else 0,
        'suspicious_keywords': 1 if any(word in url.lower() for word in ['login', 'verify', 'update', 'secure', 'bank', 'account']) else 0,
        'has_http': 1 if parsed.scheme == 'http' else 0,
        'has_https': 1 if parsed.scheme == 'https' else 0,
        'has_tinyurl': 1 if 'bit.ly' in url or 'tiny' in url else 0, 
        'num_ampersand': url.count('&'),
        'num_at': url.count('@'),
        'num_digits': sum(c.isdigit() for c in url),
        'num_dots': url.count('.'),
        'num_equals': url.count('='),
        'num_hyphens': url.count('-'),
        'num_percent': url.count('%')
    }
    
    # 🔥 THE PERMANENT FIX: Model se uske training columns directly nikalna
    if hasattr(model, 'feature_names_in_'):
        training_columns = model.feature_names_in_
    else:
        # Fallback in rare cases
        st.error("Model version purana hai, feature names nahi mil rahe.")
        return None, None

    # Ek blank dataframe banayenge jisme exactly wahi 20 columns honge jo model ko chahiye
    df = pd.DataFrame(columns=training_columns)
    
    # Ek row add karenge jisme sab default 0 honge
    df.loc[0] = 0 
    
    # Ab jo features humne calculate kiye hain, unki values is dataframe mein daal denge
    for col, val in features_dict.items():
        if col in df.columns:
            df.at[0, col] = val
            
    return df, features_dict

# --- 4. Sidebar Information ---
st.sidebar.title("ℹ️ Project Info")
st.sidebar.markdown("""
- **Model:** Random Forest
- **Accuracy:** 91.38%
- **ROC AUC:** 0.9691
- **Dataset:** 80k Balanced Samples
- **Features:** 20 Custom Lexical
- **Made by:** aj
""")

# --- 5. Main UI ---
st.title("🛡️ Phishing URL Detector AI")
st.markdown("Machine Learning ka use karke check karein ki URL **Safe** hai ya **Phishing**.")

url_input = st.text_input("Enter URL to analyze:", placeholder="https://example.com")

if st.button("Check URL", type="primary"):
    if url_input:
        if model is not None:
            with st.spinner("Analyzing URL..."):
                # Feature extraction me ab model bhi pass kar rahe hain
                features_df, raw_features = get_features(url_input, model)

                if features_df is not None:
                    try:
                        # Prediction logic
                        prediction = model.predict(features_df)[0]
                        proba = model.predict_proba(features_df)[0]
                        confidence = max(proba) * 100
                        
                        st.divider()
                        
                        # Assuming 1 = Phishing, 0 = Safe
                        if prediction == 1: 
                            st.error(f"🚨 **PHISHING DETECTED** | Confidence: {confidence:.2f}%")
                        else:
                            st.success(f"✅ **SAFE URL** | Confidence: {confidence:.2f}%")

                        # Display Key Reasons
                        st.subheader("🔍 Key Insights")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("URL Length", raw_features.get('url_length', 0))
                            st.metric("Domain Length", raw_features.get('domain_length', 0))
                        with col2:
                            st.metric("Suspicious Keywords", "Yes" if raw_features.get('suspicious_keywords', 0) else "No")
                            st.metric("IP Address in URL", "Yes" if raw_features.get('has_ip_address', 0) else "No")

                        # Debug info: Check which features were auto-filled
                        with st.expander("🛠️ Advanced: Model Features View"):
                            st.write("Is data par model ne predict kiya hai:")
                            st.dataframe(features_df)

                    except Exception as e:
                        st.error(f"⚠️ Unexpected Error: {e}")
        else:
            st.error("Model load nahi hua hai. Kripya file path check karein.")
    else:
        st.warning("Please ek URL enter karein.")
