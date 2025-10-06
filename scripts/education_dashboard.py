"""
NYC Education Dashboard
Interactive Streamlit app for exploring school performance data

Created: October 6, 2025
Author: Data Analysis Project
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from scripts.utils import load_csv

# Page config
st.set_page_config(
    page_title="NYC Education Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    """Load all datasets"""
    try:
        # Load processed data if available
        analyzed = load_csv("nyc_education_analyzed.csv", subfolder="processed")
        return analyzed
    except:
        # Load raw data
        sat = load_csv("zt9s-n5aj_20251006_114228.csv")
        demo = load_csv("s3k6-pzi2_20251006_114239.csv")

        # Convert SAT scores
        for col in [
            "mathematics_mean",
            "critical_reading_mean",
            "writing_mean",
            "number_of_test_takers",
        ]:
            sat[col] = pd.to_numeric(sat[col], errors="coerce")
        sat["total_score"] = (
            sat["mathematics_mean"] + sat["critical_reading_mean"] + sat["writing_mean"]
        )

        # Merge
        merged = sat.merge(demo, on="dbn", how="left", suffixes=("", "_demo"))

        # Map borough codes
        borough_names = {
            "M": "Manhattan",
            "X": "Bronx",
            "K": "Brooklyn",
            "Q": "Queens",
            "R": "Staten Island",
        }
        if "boro" in merged.columns:
            merged["borough_name"] = merged["boro"].map(borough_names)

        return merged


# Load data
with st.spinner("Loading data..."):
    df = load_data()

# Sidebar
st.sidebar.title("🎓 NYC Education Dashboard")
st.sidebar.markdown("---")

# Filters
st.sidebar.header("📊 Filters")

# Borough filter
boroughs = ["All"] + sorted([b for b in df["borough_name"].unique() if pd.notna(b)])
selected_borough = st.sidebar.selectbox("Select Borough", boroughs)

# Score range filter
score_range = st.sidebar.slider(
    "SAT Score Range",
    int(df["total_score"].min()),
    int(df["total_score"].max()),
    (int(df["total_score"].min()), int(df["total_score"].max())),
)

# Test takers filter
min_test_takers = st.sidebar.number_input(
    "Min Test Takers",
    min_value=0,
    max_value=int(df["number_of_test_takers"].max()),
    value=0,
)

# Apply filters
filtered_df = df.copy()

if selected_borough != "All":
    filtered_df = filtered_df[filtered_df["borough_name"] == selected_borough]

filtered_df = filtered_df[
    (filtered_df["total_score"] >= score_range[0])
    & (filtered_df["total_score"] <= score_range[1])
    & (filtered_df["number_of_test_takers"] >= min_test_takers)
]

# Sidebar stats
st.sidebar.markdown("---")
st.sidebar.header("📈 Current Selection")
st.sidebar.metric("Schools", len(filtered_df))
st.sidebar.metric("Avg SAT Score", f"{filtered_df['total_score'].mean():.0f}")
st.sidebar.metric("Total Students", f"{filtered_df['number_of_test_takers'].sum():.0f}")

# Main content
st.title("🎓 NYC School Performance Dashboard")
st.markdown("### Explore SAT scores and demographics across NYC schools")

# Top metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Schools", len(filtered_df), f"{len(filtered_df)/len(df)*100:.1f}% of total"
    )

with col2:
    st.metric(
        "Average SAT",
        f"{filtered_df['total_score'].mean():.0f}",
        f"±{filtered_df['total_score'].std():.0f}",
    )

with col3:
    st.metric(
        "Highest Score",
        f"{filtered_df['total_score'].max():.0f}",
        filtered_df.loc[filtered_df["total_score"].idxmax(), "school_name"][:20],
    )

with col4:
    st.metric(
        "Total Test Takers",
        f"{filtered_df['number_of_test_takers'].sum():.0f}",
        f"Avg: {filtered_df['number_of_test_takers'].mean():.0f}",
    )

st.markdown("---")

# Tabs for different views
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 Overview",
        "🗽 Borough Analysis",
        "🏫 School Explorer",
        "📈 Score Distribution",
        "🔍 School Search",
    ]
)

with tab1:
    st.header("Overview")

    col1, col2 = st.columns(2)

    with col1:
        # Score distribution histogram
        fig = px.histogram(
            filtered_df,
            x="total_score",
            nbins=30,
            title="SAT Score Distribution",
            labels={"total_score": "Total SAT Score", "count": "Number of Schools"},
            color_discrete_sequence=["steelblue"],
        )
        fig.add_vline(
            x=filtered_df["total_score"].mean(),
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mean: {filtered_df['total_score'].mean():.0f}",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Score sections box plot
        score_data = pd.DataFrame(
            {
                "Section": ["Math"] * len(filtered_df)
                + ["Reading"] * len(filtered_df)
                + ["Writing"] * len(filtered_df),
                "Score": list(filtered_df["mathematics_mean"])
                + list(filtered_df["critical_reading_mean"])
                + list(filtered_df["writing_mean"]),
            }
        )

        fig = px.box(
            score_data,
            x="Section",
            y="Score",
            title="Score Comparison by Section",
            labels={"Score": "Score", "Section": "SAT Section"},
            color="Section",
            color_discrete_sequence=["green", "purple", "orange"],
        )
        st.plotly_chart(fig, use_container_width=True)

    # Scatter plot
    st.subheader("School Size vs Performance")
    fig = px.scatter(
        filtered_df,
        x="number_of_test_takers",
        y="total_score",
        color="borough_name" if "borough_name" in filtered_df.columns else None,
        hover_data=["school_name"],
        title="School Size vs SAT Performance",
        labels={
            "number_of_test_takers": "Number of Test Takers",
            "total_score": "Total SAT Score",
            "borough_name": "Borough",
        },
        size="total_score",
        size_max=15,
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Borough Analysis")

    if "borough_name" in filtered_df.columns:
        # Calculate borough stats
        borough_stats = (
            filtered_df.groupby("borough_name")
            .agg(
                {
                    "school_name": "count",
                    "total_score": ["mean", "median", "std"],
                    "mathematics_mean": "mean",
                    "critical_reading_mean": "mean",
                    "writing_mean": "mean",
                }
            )
            .round(0)
        )

        col1, col2 = st.columns(2)

        with col1:
            # Average SAT by borough
            borough_avg = (
                filtered_df.groupby("borough_name")["total_score"]
                .mean()
                .sort_values(ascending=False)
            )

            fig = px.bar(
                x=borough_avg.index,
                y=borough_avg.values,
                title="Average SAT Score by Borough",
                labels={"x": "Borough", "y": "Average SAT Score"},
                color=borough_avg.values,
                color_continuous_scale="Viridis",
            )
            fig.add_hline(
                y=filtered_df["total_score"].mean(),
                line_dash="dash",
                line_color="red",
                annotation_text="NYC Average",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # School count by borough
            borough_counts = filtered_df["borough_name"].value_counts()

            fig = px.pie(
                values=borough_counts.values,
                names=borough_counts.index,
                title="Schools by Borough",
                hole=0.4,
            )
            st.plotly_chart(fig, use_container_width=True)

        # Detailed borough stats table
        st.subheader("Detailed Borough Statistics")
        st.dataframe(borough_stats, use_container_width=True)

        # Borough box plot
        fig = px.box(
            filtered_df,
            x="borough_name",
            y="total_score",
            title="SAT Score Distribution by Borough",
            labels={"borough_name": "Borough", "total_score": "Total SAT Score"},
            color="borough_name",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Borough data not available")

with tab3:
    st.header("School Explorer")

    # Top performers
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏆 Top 10 Schools")
        top_schools = filtered_df.nlargest(10, "total_score")[
            [
                "school_name",
                "total_score",
                "mathematics_mean",
                "critical_reading_mean",
                "writing_mean",
            ]
        ].reset_index(drop=True)
        top_schools.index = top_schools.index + 1
        st.dataframe(top_schools, use_container_width=True)

    with col2:
        st.subheader("📉 Bottom 10 Schools")
        bottom_schools = filtered_df.nsmallest(10, "total_score")[
            [
                "school_name",
                "total_score",
                "mathematics_mean",
                "critical_reading_mean",
                "writing_mean",
            ]
        ].reset_index(drop=True)
        bottom_schools.index = bottom_schools.index + 1
        st.dataframe(bottom_schools, use_container_width=True)

    # Performance categories
    st.subheader("Performance Categories")

    def categorize_performance(score):
        if pd.isna(score):
            return "Unknown"
        elif score >= 1500:
            return "High (1500+)"
        elif score >= 1200:
            return "Above Average (1200-1499)"
        elif score >= 1000:
            return "Average (1000-1199)"
        else:
            return "Below Average (<1000)"

    filtered_df["performance_category"] = filtered_df["total_score"].apply(
        categorize_performance
    )
    category_counts = filtered_df["performance_category"].value_counts()

    fig = px.bar(
        x=category_counts.index,
        y=category_counts.values,
        title="Schools by Performance Category",
        labels={"x": "Category", "y": "Number of Schools"},
        color=category_counts.values,
        color_continuous_scale="RdYlGn",
    )
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("Score Distribution Analysis")

    # Detailed distribution
    col1, col2, col3 = st.columns(3)

    sections = ["mathematics_mean", "critical_reading_mean", "writing_mean"]
    section_names = ["Math", "Reading", "Writing"]
    colors = ["green", "purple", "orange"]

    for col, section, name, color in zip(
        [col1, col2, col3], sections, section_names, colors
    ):
        with col:
            fig = px.histogram(
                filtered_df,
                x=section,
                nbins=25,
                title=f"{name} Score Distribution",
                labels={section: f"{name} Score"},
                color_discrete_sequence=[color],
            )
            fig.add_vline(
                x=filtered_df[section].mean(), line_dash="dash", line_color="red"
            )
            st.plotly_chart(fig, use_container_width=True)

    # Correlation between sections
    st.subheader("Correlation Between SAT Sections")

    corr_data = filtered_df[
        ["mathematics_mean", "critical_reading_mean", "writing_mean"]
    ].corr()

    fig = px.imshow(
        corr_data,
        text_auto=".2f",
        title="Correlation Matrix",
        color_continuous_scale="RdBu_r",
        aspect="auto",
    )
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.header("🔍 School Search")

    # Search box
    search_term = st.text_input("Search for a school by name:")

    if search_term:
        search_results = filtered_df[
            filtered_df["school_name"].str.contains(search_term, case=False, na=False)
        ]

        st.write(f"Found {len(search_results)} school(s)")

        if len(search_results) > 0:
            # Select a school
            selected_school = st.selectbox(
                "Select a school:", search_results["school_name"].tolist()
            )

            if selected_school:
                school_data = search_results[
                    search_results["school_name"] == selected_school
                ].iloc[0]

                st.markdown(f"### {school_data['school_name']}")

                # Metrics
                col1, col2, col3, col4 = st.columns(4)

                col1.metric("Total SAT", f"{school_data['total_score']:.0f}")
                col2.metric("Math", f"{school_data['mathematics_mean']:.0f}")
                col3.metric("Reading", f"{school_data['critical_reading_mean']:.0f}")
                col4.metric("Writing", f"{school_data['writing_mean']:.0f}")

                col1, col2, col3 = st.columns(3)
                col1.metric(
                    "Test Takers", f"{school_data['number_of_test_takers']:.0f}"
                )
                if "borough_name" in school_data and pd.notna(
                    school_data["borough_name"]
                ):
                    col2.metric("Borough", school_data["borough_name"])
                col3.metric("DBN Code", school_data["dbn"])

                # Compare to averages
                st.subheader("Comparison to NYC Average")

                avg_total = df["total_score"].mean()
                avg_math = df["mathematics_mean"].mean()
                avg_reading = df["critical_reading_mean"].mean()
                avg_writing = df["writing_mean"].mean()

                comparison_data = pd.DataFrame(
                    {
                        "Section": ["Total SAT", "Math", "Reading", "Writing"],
                        "School": [
                            school_data["total_score"],
                            school_data["mathematics_mean"],
                            school_data["critical_reading_mean"],
                            school_data["writing_mean"],
                        ],
                        "NYC Average": [avg_total, avg_math, avg_reading, avg_writing],
                    }
                )

                fig = go.Figure()
                fig.add_trace(
                    go.Bar(
                        name="School",
                        x=comparison_data["Section"],
                        y=comparison_data["School"],
                        marker_color="steelblue",
                    )
                )
                fig.add_trace(
                    go.Bar(
                        name="NYC Average",
                        x=comparison_data["Section"],
                        y=comparison_data["NYC Average"],
                        marker_color="lightcoral",
                    )
                )
                fig.update_layout(
                    title="School vs NYC Average",
                    barmode="group",
                    xaxis_title="",
                    yaxis_title="Score",
                )
                st.plotly_chart(fig, use_container_width=True)

                # Percentile ranking
                percentile = (
                    (filtered_df["total_score"] < school_data["total_score"]).sum()
                    / len(filtered_df)
                    * 100
                )
                st.metric(
                    "Percentile Rank",
                    f"{percentile:.1f}%",
                    f"Better than {percentile:.1f}% of schools",
                )
    else:
        st.info("Enter a school name to search")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>📊 Data Source: NYC Open Data | 🎓 {len(df)} Schools Analyzed</p>
        <p>Built with Streamlit | Last Updated: October 6, 2025</p>
    </div>
    """.replace(
        "{len(df)}", str(len(df))
    ),
    unsafe_allow_html=True,
)
