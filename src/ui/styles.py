"""
Custom CSS styles for Streamlit application.
"""

import streamlit as st


def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit application."""
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
            background-color: #FF9800;
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            border: none;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #F57C00;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .traffic-light-red {
            background: linear-gradient(135deg, #ff5252 0%, #f44336 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .traffic-light-yellow {
            background: linear-gradient(135deg, #ffeb3b 0%, #ffc107 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: #333;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .traffic-light-green {
            background: linear-gradient(135deg, #66bb6a 0%, #4caf50 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .metric-container {
            background-color: #f5f5f5;
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
