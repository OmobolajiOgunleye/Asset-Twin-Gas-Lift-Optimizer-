
import streamlit as st
import numpy as np
from scipy.optimize import minimize
import pandas as pd
import plotly.graph_objects as go

# --- PAGE CONFIGURATION & THEME ---
st.set_page_config(page_title="AssetTwin - Gas Lift Optimizer", layout="wide")

# Custom CSS styling for a highly polished, professional enterprise appearance
st.markdown("""
    <style>
    .reportview-container { background: #f5f7f9; }
    h1 { color: #0e2433; font-weight: 700; }
    h3 { color: #2c3e50; font-weight: 500; }
    
    /* This section fixes your invisible white boxes */
    .stMetric { 
        background-color: #ffffff !important; 
        padding: 15px; 
        border: 1px solid #e2e8f0;
        border-radius: 8px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); 
    }
    /* Explicitly forcing the text inside the boxes to be visible dark colors */
    .stMetric div {
        color: #0e2433 !important;
    }
    </style>
""", unsafe_allow_html=True)


# --- HEADERS ---
st.title("AssetTwin: Production Optimization Portal")
st.markdown("### Algorithmic Resource Allocation & Well Bottlenecking Engine")
st.write("This application wraps an industry-standard optimization algorithm around digital twins of live production wells to distribute constrained compressor gas automatically.")

# --- SIDEBAR INTERACTIVE CONTROLS ---
st.sidebar.header("Asset Constraints")

# Replacing your hardcoded TOTAL_GAS_LIMIT = 300.0 with a live user slider
TOTAL_GAS_LIMIT = st.sidebar.slider(
    "Total Field Gas Limit (MSCF/day)", 
    min_value=100.0, 
    max_value=500.0, 
    value=300.0, 
    step=10.0
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡This software maps physical production constraints to mathematical limits, eliminating the manual guesswork traditionally done by operations engineers."
)

# --- YOUR EXACT WELL PHYSICS MODEL ---
well_coefficients = {
    'Well_1': (-0.005, 1.2, 50),
    'Well_2': (-0.008, 1.5, 30),
    'Well_3': (-0.004, 0.9, 70),
    'Well_4': (-0.006, 1.1, 40),
    'Well_5': (-0.007, 1.3, 45)
}

def calculate_well_production(q_gl, a, b, c):
    if q_gl < 0:
        return 0
    prod = (a * (q_gl ** 2)) + (b * q_gl) + c
    return max(prod, 0)

# --- YOUR EXACT OPTIMIZATION ENGINE ---
def objective_function(gas_allocation):
    total_production = 0
    for i, (well_name, coeffs) in enumerate(well_coefficients.items()):
        a, b, c = coeffs
        total_production += calculate_well_production(gas_allocation[i], a, b, c)
    return -total_production

def gas_limit_constraint(gas_allocation):
    return TOTAL_GAS_LIMIT - np.sum(gas_allocation)

constraints = {'type': 'ineq', 'fun': gas_limit_constraint}
bounds = [(0, 100) for _ in range(5)]
initial_guess = [TOTAL_GAS_LIMIT / 5.0] * 5  # Dynamically adjusts based on slider value

# Execute Optimization
result = minimize(objective_function, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)

# --- STREAMLIT UI LAYOUT & GRAPHICS ---
if result.success:
    optimized_allocations = result.x
    total_oil_production = -result.fun
    actual_gas_used = np.sum(optimized_allocations)
    
    # 1. High-Level Performance Scorecard (KPI Cards)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Maximized Asset Output", f"{total_oil_production:.2f} STB/day")
    with col2:
        st.metric("Allocated Gas Capacity", f"{actual_gas_used:.2f} MSCF/day", f"Limit: {TOTAL_GAS_LIMIT} Max")
    with col3:
        efficiency = total_oil_production / actual_gas_used if actual_gas_used > 0 else 0
        st.metric("Gas Lift Efficiency Factor", f"{efficiency:.2f} bbl/MSCF")
        
    st.markdown("---")
    
    # 2. Interactive Charts Section
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("Optimal Gas Distribution (MSCF/day)")
        fig_bar = go.Figure(data=[
            go.Bar(
                x=list(well_coefficients.keys()), 
                y=optimized_allocations, 
                marker_color='#104f55',
                text=[f"{val:.2f}" for val in optimized_allocations], 
                textposition='auto'
            )
        ])
        fig_bar.update_layout(yaxis_title="Injection Rate", template="plotly_white", margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with chart_col2:
        st.subheader("Asset Breakdown Ledger")
        # Build out a clean analytical table matching your output loop
        ledger_data = []
        for i, (well_name, coeffs) in enumerate(well_coefficients.items()):
            well_prod = calculate_well_production(optimized_allocations[i], *coeffs)
            ledger_data.append({
                "Well Identity": well_name,
                "Gas Allocated (MSCF/d)": round(optimized_allocations[i], 2),
                "Oil Output (STB/d)": round(well_prod, 2)
            })
        st.table(pd.DataFrame(ledger_data))
        
else:
    st.error("Operational Optimization Failure: The algorithm failed to converge under current limits.")


