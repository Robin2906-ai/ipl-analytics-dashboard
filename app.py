import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── Page Config ───
st.set_page_config(page_title="IPL Analytics Dashboard", page_icon="🏏", layout="wide")

# ─── Custom CSS ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
    
    .stApp { font-family: 'DM Sans', sans-serif; }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        border: 1px solid #2a2a4a;
    }
    .metric-value {
        font-size: 36px;
        font-weight: 700;
        color: #00d4ff;
    }
    .metric-label {
        font-size: 13px;
        color: #8892b0;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 4px;
    }
    
    .header-title {
        font-size: 48px;
        font-weight: 700;
        background: linear-gradient(135deg, #00d4ff, #7b2dce, #ff6f00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }
    .header-sub {
        text-align: center;
        color: #8892b0;
        font-size: 16px;
        margin-bottom: 32px;
    }
    
    .insight-box {
        background: #0d1117;
        border-left: 4px solid #00d4ff;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin: 12px 0;
        color: #c9d1d9;
        font-size: 14px;
        line-height: 1.6;
    }
    
    .section-header {
        font-size: 24px;
        font-weight: 700;
        color: #e6e6e6;
        margin: 32px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #2a2a4a;
    }
</style>
""", unsafe_allow_html=True)

# ─── Load & Clean Data ───
@st.cache_data
def load_data():
    matches = pd.read_csv("data/matches.csv")
    deliveries = pd.read_csv("data/deliveries.csv")
    
    # Standardize team names
    team_map = {
        'Delhi Daredevils': 'Delhi Capitals',
        'Kings XI Punjab': 'Punjab Kings',
        'Rising Pune Supergiant': 'Rising Pune Supergiants',
        'Royal Challengers Bengaluru': 'Royal Challengers Bangalore',
        'Deccan Chargers': 'Sunrisers Hyderabad',
    }
    for col in ['team1', 'team2', 'toss_winner', 'winner']:
        matches[col] = matches[col].replace(team_map)
    for col in ['batting_team', 'bowling_team']:
        deliveries[col] = deliveries[col].replace(team_map)
    
    matches['date'] = pd.to_datetime(matches['date'])
    return matches, deliveries

matches, deliveries = load_data()

# ─── Team Colors ───
TEAM_COLORS = {
    'Chennai Super Kings': '#FBBF24',
    'Mumbai Indians': '#1D4ED8',
    'Royal Challengers Bangalore': '#DC2626',
    'Kolkata Knight Riders': '#7C3AED',
    'Delhi Capitals': '#2563EB',
    'Punjab Kings': '#EF4444',
    'Rajasthan Royals': '#EC4899',
    'Sunrisers Hyderabad': '#F97316',
    'Gujarat Titans': '#1E3A5F',
    'Lucknow Super Giants': '#0891B2',
    'Rising Pune Supergiants': '#8B5CF6',
    'Kochi Tuskers Kerala': '#7C3AED',
    'Gujarat Lions': '#F59E0B',
    'Pune Warriors': '#6366F1',
}

PLOTLY_TEMPLATE = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {'color': '#c9d1d9', 'family': 'DM Sans'},
    'xaxis': {'gridcolor': '#2a2a4a', 'zerolinecolor': '#2a2a4a'},
    'yaxis': {'gridcolor': '#2a2a4a', 'zerolinecolor': '#2a2a4a'},
}

def style_fig(fig, height=450):
    fig.update_layout(**PLOTLY_TEMPLATE, height=height, margin=dict(l=40, r=40, t=50, b=40))
    return fig

# ─── Header ───
st.markdown('<div class="header-title">🏏 IPL Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="header-sub">Ball-by-ball insights from 17 seasons of IPL (2008–2024) • 1,095 matches • 260,920 deliveries</div>', unsafe_allow_html=True)

# ─── Sidebar Filters ───
st.sidebar.markdown("### 🎯 Filters")
all_seasons = sorted(matches['season'].unique())
selected_seasons = st.sidebar.multiselect("Seasons", all_seasons, default=all_seasons)

all_teams = sorted(set(matches['team1'].unique()) | set(matches['team2'].unique()))
selected_teams = st.sidebar.multiselect("Teams", all_teams, default=all_teams)

# Filter data
m = matches[
    (matches['season'].isin(selected_seasons)) &
    ((matches['team1'].isin(selected_teams)) | (matches['team2'].isin(selected_teams)))
]
d = deliveries[deliveries['match_id'].isin(m['id'])]

# ─── Key Metrics ───
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'''<div class="metric-card">
        <div class="metric-value">{len(m):,}</div>
        <div class="metric-label">Total Matches</div>
    </div>''', unsafe_allow_html=True)

with col2:
    total_runs = d['total_runs'].sum()
    st.markdown(f'''<div class="metric-card">
        <div class="metric-value">{total_runs:,}</div>
        <div class="metric-label">Total Runs Scored</div>
    </div>''', unsafe_allow_html=True)

with col3:
    total_wickets = d['is_wicket'].sum()
    st.markdown(f'''<div class="metric-card">
        <div class="metric-value">{total_wickets:,}</div>
        <div class="metric-label">Total Wickets</div>
    </div>''', unsafe_allow_html=True)

with col4:
    total_sixes = len(d[d['batsman_runs'] == 6])
    st.markdown(f'''<div class="metric-card">
        <div class="metric-value">{total_sixes:,}</div>
        <div class="metric-label">Sixes Hit</div>
    </div>''', unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════
# TAB LAYOUT
# ═══════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "🏏 Batting", "🎳 Bowling", "🏟️ Teams", "🔍 Head to Head"])

# ═══════════════════════════════════════════════
# TAB 1: OVERVIEW
# ═══════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">Average First Innings Score by Season</div>', unsafe_allow_html=True)
    
    merged = d.merge(m[['id', 'season']], left_on='match_id', right_on='id')
    inn_scores = merged.groupby(['match_id', 'season', 'inning'])['total_runs'].sum().reset_index()
    first_inn = inn_scores[inn_scores['inning'] == 1]
    avg_season = first_inn.groupby('season')['total_runs'].mean().reset_index()
    avg_season.columns = ['Season', 'Avg Score']
    
    fig = px.bar(avg_season, x='Season', y='Avg Score',
                 color='Avg Score', color_continuous_scale=['#1a1a2e', '#00d4ff', '#7b2dce'],
                 text=avg_season['Avg Score'].round(1))
    fig.update_traces(textposition='outside', textfont_size=11)
    fig = style_fig(fig, 420)
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('''<div class="insight-box">
        💡 <strong>Insight:</strong> Average first innings scores have risen sharply — from ~150 in early seasons to nearly 190 in 2024. 
        Impact player rule, flatter pitches, and aggressive batting have transformed the game.
    </div>''', unsafe_allow_html=True)

    # Toss Analysis
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown('<div class="section-header">Toss Decision Trend</div>', unsafe_allow_html=True)
        toss_trend = m.groupby(['season', 'toss_decision']).size().reset_index(name='count')
        fig = px.bar(toss_trend, x='season', y='count', color='toss_decision',
                     barmode='group', color_discrete_map={'bat': '#FBBF24', 'field': '#00d4ff'})
        fig = style_fig(fig, 380)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_b:
        st.markdown('<div class="section-header">Does Toss Matter?</div>', unsafe_allow_html=True)
        toss_data = m[m['winner'].notna()].copy()
        toss_data['toss_won_match'] = toss_data['toss_winner'] == toss_data['winner']
        toss_by_dec = toss_data.groupby('toss_decision')['toss_won_match'].mean().reset_index()
        toss_by_dec.columns = ['Decision', 'Win %']
        toss_by_dec['Win %'] = (toss_by_dec['Win %'] * 100).round(1)
        
        fig = px.bar(toss_by_dec, x='Decision', y='Win %',
                     color='Decision', color_discrete_map={'bat': '#FBBF24', 'field': '#00d4ff'},
                     text='Win %')
        fig.update_traces(textposition='outside', textfont_size=14)
        fig.add_hline(y=50, line_dash="dash", line_color="#555", annotation_text="50% baseline")
        fig = style_fig(fig, 380)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('''<div class="insight-box">
        💡 <strong>Insight:</strong> Teams choosing to field after winning toss win ~54% of the time vs ~45% when choosing to bat.
        Chasing under lights with dew factor gives a measurable advantage.
    </div>''', unsafe_allow_html=True)

    # Win by type
    st.markdown('<div class="section-header">How Matches Are Won</div>', unsafe_allow_html=True)
    win_type = m[m['result'].notna()]['result'].value_counts().reset_index()
    win_type.columns = ['Result', 'Count']
    fig = px.pie(win_type, names='Result', values='Count',
                 color_discrete_sequence=['#00d4ff', '#7b2dce', '#FBBF24', '#ff6f00'],
                 hole=0.45)
    fig = style_fig(fig, 380)
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════
# TAB 2: BATTING
# ═══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">Top 15 Run Scorers (All Time)</div>', unsafe_allow_html=True)
    
    top_bat = d.groupby('batter').agg(
        runs=('batsman_runs', 'sum'),
        balls=('batsman_runs', 'count'),
        fours=('batsman_runs', lambda x: (x == 4).sum()),
        sixes=('batsman_runs', lambda x: (x == 6).sum()),
    ).reset_index()
    top_bat['strike_rate'] = (top_bat['runs'] / top_bat['balls'] * 100).round(1)
    top_bat = top_bat.sort_values('runs', ascending=False).head(15)
    
    fig = px.bar(top_bat, x='runs', y='batter', orientation='h',
                 color='strike_rate', color_continuous_scale=['#1a1a2e', '#00d4ff', '#ff6f00'],
                 text='runs', hover_data=['strike_rate', 'fours', 'sixes'])
    fig.update_traces(textposition='outside', textfont_size=12)
    fig = style_fig(fig, 550)
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, coloraxis_colorbar_title='SR')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('''<div class="insight-box">
        💡 <strong>Insight:</strong> Virat Kohli leads with 8,000+ runs. Notice how players like AB de Villiers and Chris Gayle 
        have significantly higher strike rates despite fewer matches — the color gradient reveals who scores fastest.
    </div>''', unsafe_allow_html=True)

    # Strike Rate vs Runs scatter
    st.markdown('<div class="section-header">Strike Rate vs Runs (min 1000 runs)</div>', unsafe_allow_html=True)
    
    qualified = d.groupby('batter').agg(
        runs=('batsman_runs', 'sum'),
        balls=('batsman_runs', 'count'),
        sixes=('batsman_runs', lambda x: (x == 6).sum()),
    ).reset_index()
    qualified['strike_rate'] = (qualified['runs'] / qualified['balls'] * 100).round(1)
    qualified = qualified[qualified['runs'] >= 1000]
    
    fig = px.scatter(qualified, x='runs', y='strike_rate', size='sixes',
                     hover_name='batter', color='strike_rate',
                     color_continuous_scale=['#1a1a2e', '#00d4ff', '#7b2dce'],
                     size_max=30)
    fig.add_hline(y=qualified['strike_rate'].median(), line_dash="dash", line_color="#555",
                  annotation_text=f"Median SR: {qualified['strike_rate'].median():.1f}")
    fig.add_vline(x=qualified['runs'].median(), line_dash="dash", line_color="#555")
    fig = style_fig(fig, 500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('''<div class="insight-box">
        💡 <strong>Insight:</strong> The top-right quadrant shows the elite — high runs AND high strike rate. 
        Bubble size = number of sixes. Players like Gayle dominate the "six-hitting" metric despite fewer total runs.
    </div>''', unsafe_allow_html=True)

    # Runs by over phase
    st.markdown('<div class="section-header">Run Scoring by Phase</div>', unsafe_allow_html=True)
    
    phase_d = d.copy()
    phase_d['phase'] = pd.cut(phase_d['over'], bins=[-1, 5, 14, 20],
                               labels=['Powerplay (1-6)', 'Middle (7-15)', 'Death (16-20)'])
    phase_runs = phase_d.groupby('phase')['total_runs'].mean().reset_index()
    phase_runs.columns = ['Phase', 'Avg Runs/Ball']
    
    fig = px.bar(phase_runs, x='Phase', y='Avg Runs/Ball',
                 color='Phase', color_discrete_sequence=['#00d4ff', '#7b2dce', '#ff6f00'],
                 text=phase_runs['Avg Runs/Ball'].round(3))
    fig.update_traces(textposition='outside', textfont_size=14)
    fig = style_fig(fig, 380)
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════
# TAB 3: BOWLING
# ═══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Top 15 Wicket Takers (All Time)</div>', unsafe_allow_html=True)
    
    wickets = d[d['is_wicket'] == 1]
    top_bowl = wickets.groupby('bowler').size().reset_index(name='wickets')
    
    # Economy rate
    bowl_stats = d.groupby('bowler').agg(
        runs_conceded=('total_runs', 'sum'),
        balls=('total_runs', 'count'),
    ).reset_index()
    bowl_stats['economy'] = (bowl_stats['runs_conceded'] / (bowl_stats['balls'] / 6)).round(2)
    
    top_bowl = top_bowl.merge(bowl_stats[['bowler', 'economy']], on='bowler')
    top_bowl = top_bowl.sort_values('wickets', ascending=False).head(15)
    
    fig = px.bar(top_bowl, x='wickets', y='bowler', orientation='h',
                 color='economy', color_continuous_scale=['#00d4ff', '#1a1a2e', '#DC2626'],
                 text='wickets', hover_data=['economy'])
    fig.update_traces(textposition='outside', textfont_size=12)
    fig = style_fig(fig, 550)
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, coloraxis_colorbar_title='Econ')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('''<div class="insight-box">
        💡 <strong>Insight:</strong> Yuzvendra Chahal leads the wicket charts. The color gradient shows economy rate —
        bluer = more economical. Bumrah stands out with both high wickets AND excellent economy.
    </div>''', unsafe_allow_html=True)

    # Dismissal types
    st.markdown('<div class="section-header">How Batsmen Get Out</div>', unsafe_allow_html=True)
    
    dismissals = d[d['dismissal_kind'].notna() & (d['dismissal_kind'] != 'NA')]
    dismiss_counts = dismissals['dismissal_kind'].value_counts().reset_index()
    dismiss_counts.columns = ['Type', 'Count']
    
    fig = px.treemap(dismiss_counts, path=['Type'], values='Count',
                     color='Count', color_continuous_scale=['#1a1a2e', '#00d4ff', '#7b2dce'])
    fig = style_fig(fig, 420)
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    # Economy by over phase
    st.markdown('<div class="section-header">Economy Rate by Phase</div>', unsafe_allow_html=True)
    
    bowl_phase = d.copy()
    bowl_phase['phase'] = pd.cut(bowl_phase['over'], bins=[-1, 5, 14, 20],
                                  labels=['Powerplay (1-6)', 'Middle (7-15)', 'Death (16-20)'])
    phase_econ = bowl_phase.groupby('phase').agg(
        runs=('total_runs', 'sum'),
        balls=('total_runs', 'count')
    ).reset_index()
    phase_econ['economy'] = (phase_econ['runs'] / (phase_econ['balls'] / 6)).round(2)
    
    fig = px.bar(phase_econ, x='phase', y='economy',
                 color='phase', color_discrete_sequence=['#00d4ff', '#7b2dce', '#ff6f00'],
                 text='economy')
    fig.update_traces(textposition='outside', textfont_size=14)
    fig = style_fig(fig, 380)
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════
# TAB 4: TEAMS
# ═══════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Win Count by Team</div>', unsafe_allow_html=True)
    
    wins = m[m['winner'].notna()]['winner'].value_counts().reset_index()
    wins.columns = ['Team', 'Wins']
    wins['Color'] = wins['Team'].map(TEAM_COLORS).fillna('#666')
    
    fig = px.bar(wins, x='Wins', y='Team', orientation='h', text='Wins',
                 color='Team', color_discrete_map=TEAM_COLORS)
    fig.update_traces(textposition='outside', textfont_size=12)
    fig = style_fig(fig, 550)
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Titles
    col_x, col_y = st.columns(2)
    
    with col_x:
        st.markdown('<div class="section-header">🏆 IPL Titles</div>', unsafe_allow_html=True)
        finals = m[m['match_type'].str.contains('Final', case=False, na=False)]
        titles = finals['winner'].value_counts().reset_index()
        titles.columns = ['Team', 'Titles']
        
        fig = px.bar(titles, x='Team', y='Titles', color='Team',
                     color_discrete_map=TEAM_COLORS, text='Titles')
        fig.update_traces(textposition='outside', textfont_size=14)
        fig = style_fig(fig, 400)
        fig.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_y:
        st.markdown('<div class="section-header">Win % by Team</div>', unsafe_allow_html=True)
        
        team_matches = {}
        for _, row in m[m['winner'].notna()].iterrows():
            for t in [row['team1'], row['team2']]:
                if t not in team_matches:
                    team_matches[t] = {'played': 0, 'won': 0}
                team_matches[t]['played'] += 1
                if t == row['winner']:
                    team_matches[t]['won'] += 1
        
        win_pct = pd.DataFrame([
            {'Team': t, 'Played': v['played'], 'Won': v['won'],
             'Win %': round(v['won'] / v['played'] * 100, 1)}
            for t, v in team_matches.items()
        ]).sort_values('Win %', ascending=False)
        
        # Only teams with 30+ matches
        win_pct = win_pct[win_pct['Played'] >= 30]
        
        fig = px.bar(win_pct, x='Win %', y='Team', orientation='h',
                     color='Team', color_discrete_map=TEAM_COLORS,
                     text='Win %', hover_data=['Played', 'Won'])
        fig.update_traces(textposition='outside', textfont_size=12)
        fig.add_vline(x=50, line_dash="dash", line_color="#555")
        fig = style_fig(fig, 400)
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('''<div class="insight-box">
        💡 <strong>Insight:</strong> CSK and MI dominate both titles and win percentage. Gujarat Titans have an impressive 
        win rate despite being a newer franchise. RCB's high match count but zero titles (until 2024) tells its own story.
    </div>''', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# TAB 5: HEAD TO HEAD
# ═══════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">Head-to-Head Comparison</div>', unsafe_allow_html=True)
    
    active_teams = sorted([t for t in all_teams if t in m['winner'].values])
    
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        team_a = st.selectbox("Team 1", active_teams, index=active_teams.index('Mumbai Indians') if 'Mumbai Indians' in active_teams else 0)
    with col_h2:
        team_b = st.selectbox("Team 2", [t for t in active_teams if t != team_a],
                              index=0)
    
    h2h = m[
        ((m['team1'] == team_a) & (m['team2'] == team_b)) |
        ((m['team1'] == team_b) & (m['team2'] == team_a))
    ]
    
    if len(h2h) > 0:
        wins_a = len(h2h[h2h['winner'] == team_a])
        wins_b = len(h2h[h2h['winner'] == team_b])
        no_result = len(h2h) - wins_a - wins_b
        
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            color_a = TEAM_COLORS.get(team_a, '#00d4ff')
            st.markdown(f'''<div class="metric-card">
                <div class="metric-value" style="color: {color_a}">{wins_a}</div>
                <div class="metric-label">{team_a}</div>
            </div>''', unsafe_allow_html=True)
        with col_s2:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-value" style="color: #888">{len(h2h)}</div>
                <div class="metric-label">Total Matches</div>
            </div>''', unsafe_allow_html=True)
        with col_s3:
            color_b = TEAM_COLORS.get(team_b, '#7b2dce')
            st.markdown(f'''<div class="metric-card">
                <div class="metric-value" style="color: {color_b}">{wins_b}</div>
                <div class="metric-label">{team_b}</div>
            </div>''', unsafe_allow_html=True)
        
        # H2H over seasons
        st.markdown("", unsafe_allow_html=True)
        h2h_season = h2h.groupby(['season', 'winner']).size().reset_index(name='wins')
        h2h_season = h2h_season[h2h_season['winner'].isin([team_a, team_b])]
        
        fig = px.bar(h2h_season, x='season', y='wins', color='winner',
                     barmode='group',
                     color_discrete_map={team_a: color_a, team_b: color_b})
        fig = style_fig(fig, 380)
        fig.update_layout(legend_title='')
        st.plotly_chart(fig, use_container_width=True)
        
        # Recent results
        st.markdown('<div class="section-header">Recent Matches</div>', unsafe_allow_html=True)
        recent = h2h.sort_values('date', ascending=False).head(8)[['date', 'team1', 'team2', 'winner', 'result', 'result_margin', 'venue']]
        recent['date'] = recent['date'].dt.strftime('%d %b %Y')
        st.dataframe(recent, use_container_width=True, hide_index=True)
    else:
        st.info("These two teams haven't played each other in the selected filters.")

# ─── Footer ───
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #555; font-size: 13px; padding: 16px 0;">
    Built with ❤️ using Python, Pandas & Plotly • Data: IPL Ball-by-Ball Dataset (2008–2024)
    <br>
    <a href="https://github.com/Robin2906-ai" style="color: #00d4ff; text-decoration: none;">GitHub</a> • 
    Made by Aryan
</div>
""", unsafe_allow_html=True)
