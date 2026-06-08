import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

def generate_and_save_visualizations(df: pd.DataFrame, output_dir: Path):
    """Generates a professional, publication-grade epidemiological graphics suite."""
    output_dir.mkdir(exist_ok=True)
    
    # Set global aesthetic configurations for professional reporting
    sns.set_theme(style="white", context="talk")
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'axes.edgecolor': '#D0D0D0',
        'axes.linewidth': 0.8,
        'grid.color': '#EAEAEA',
        'grid.alpha': 0.7
    })

    # ==================================================================
    # VISUAL 1: LONGITUDINAL EPIDEMIOLOGICAL TREND WITH CONFIDENCE RIBBONS
    # ==================================================================
    fig, ax = plt.subplots(figsize=(12, 7))
    sexes = df['Sex'].unique()
    # Base palette for commonly expected categories. Any missing categories
    # will be assigned colors from a seaborn palette so we never pass a
    # partial palette dict to plotting functions.
    base_colors = {'Male': '#1f77b4', 'Female': '#e377c2'}
    palette_map = dict()
    # Start by populating known mappings
    for k, v in base_colors.items():
        palette_map[k] = v

    # Identify missing categories and assign them colors from a safe palette
    missing = [s for s in sexes if s not in palette_map]
    if missing:
        generated = sns.color_palette('tab10', n_colors=len(missing))
        for m, col in zip(sorted(missing), generated):
            palette_map[m] = col
    
    for sex in sexes:
        sub_df = df[df['Sex'] == sex].sort_values('Year')
        color = palette_map.get(sex, '#7f7f7f')
        
        # Plot the main trajectory line
        ax.plot(sub_df['Year'], sub_df['Diagnosis Number'], label=f'{sex} Diagnosis Track', 
                color=color, linewidth=3, marker='o', markersize=6)
        
        # Fill statistical uncertainty envelope (Lower to Upper bounds)
        ax.fill_between(sub_df['Year'], sub_df['Lower Bound'], sub_df['Upper Bound'], 
                        color=color, alpha=0.15, label=f'{sex} 95% Confidence Interval')

    ax.set_title("Longitudinal HIV/AIDS Diagnoses in France (With Confidence Ribbons)", 
                 fontsize=18, fontweight='bold', pad=20, color='#333333')
    ax.set_xlabel("Observation Year", fontsize=14, labelpad=10)
    ax.set_ylabel("Annual Diagnoses Count", fontsize=14, labelpad=10)
    ax.grid(True, linestyle='--')
    ax.legend(frameon=True, facecolor='white', edgecolor='none', fontsize=12)
    sns.despine(trim=True)
    plt.tight_layout()
    plt.savefig(output_dir / "01_epidemiological_trends_ci.png", dpi=300)
    plt.close()

    # ==================================================================
    # VISUAL 2: FACETGRID SIDE-BY-SIDE DISTRIBUTION & DENSITY ANALYSIS
    # ==================================================================
    # Pass a mapping to `palette` so seaborn knows exact color for each hue level
    g = sns.FacetGrid(df, col="Sex", hue="Sex", palette=palette_map, height=5, aspect=1.3)
    g.map(sns.kdeplot, "Diagnosis Number", fill=True, alpha=0.4, linewidth=2.5)
    g.map(sns.rugplot, "Diagnosis Number", height=0.05)
    
    g.set_titles(col_template="{col_name} Distribution Profile", fontweight='bold', size=14)
    g.set_xlabels("Diagnosis Number Cases", size=12)
    g.set_ylabels("Density Estimation", size=12)
    
    for ax in g.axes.flat:
        ax.grid(True, linestyle=':', alpha=0.6)
    plt.subplots_adjust(top=0.8)
    g.fig.suptitle("Stratified Density & Volatility Profiles", fontsize=16, fontweight='bold', color='#333333')
    g.savefig(output_dir / "02_stratified_density_facets.png", dpi=300)
    plt.close()

    # ==================================================================
    # VISUAL 3: DEMOGRAPHIC PROFILE PROPORTIONAL SHIFT OVER TIME
    # ==================================================================
    pivot_df = df.pivot(index='Year', columns='Sex', values='Diagnosis Number').fillna(0)
    # Convert absolute raw counts into percentage matrices summing up to 100%
    pivot_perc = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=(12, 6))
    # Use the palette_map to build colors in the same order as the columns
    stack_colors = [palette_map.get(col, '#7f7f7f') for col in pivot_perc.columns]
    ax.stackplot(pivot_perc.index, pivot_perc.T, labels=pivot_perc.columns, 
                 colors=stack_colors, alpha=0.85)

    ax.set_title("Proportional Shift in Diagnosis Demographics Over Time", 
                 fontsize=18, fontweight='bold', pad=20, color='#333333')
    ax.set_xlabel("Year", fontsize=14)
    ax.set_ylabel("Percentage Share of Total Diagnoses (%)", fontsize=14)
    ax.set_ylim(0, 100)
    ax.set_xlim(pivot_perc.index.min(), pivot_perc.index.max())
    ax.legend(loc='lower left', frameon=True, facecolor='white', fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.5, axis='y')
    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.savefig(output_dir / "03_demographic_share_evolution.png", dpi=300)
    plt.close()

    # ==================================================================
    # VISUAL 4: VELOCITY ANALYSIS (YEAR-OVER-YEAR CHANGE BY SEX)
    # ==================================================================
    sorted_df = df.sort_values(['Sex', 'Year']).copy()
    sorted_df['YoY_Change'] = sorted_df.groupby('Sex')['Diagnosis Number'].diff()
    sorted_df = sorted_df.dropna(subset=['YoY_Change'])

    fig, ax = plt.subplots(figsize=(12, 6))
    # For categorical hue palettes, pass the mapping dictionary so all levels
    # are accounted for (prevents missing-key ValueError)
    sns.barplot(data=sorted_df, x='Year', y='YoY_Change', hue='Sex', palette=palette_map, ax=ax)
    
    ax.set_title("Velocity Analysis: Year-over-Year Change in Diagnoses", 
                 fontsize=18, fontweight='bold', pad=20, color='#333333')
    ax.set_xlabel("Year", fontsize=14)
    ax.set_ylabel("Net Shift in Cases (Compared to Previous Year)", fontsize=14)
    ax.axhline(0, color='black', linewidth=1, linestyle='-') # Base threshold line
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(frameon=True, facecolor='white', fontsize=12)
    sns.despine()
    plt.tight_layout()
    plt.savefig(output_dir / "04_velocity_yoy_changes.png", dpi=300)
    plt.close()