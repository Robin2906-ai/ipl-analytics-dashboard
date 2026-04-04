# 🏏 IPL Analytics Dashboard

An interactive data analytics dashboard exploring **17 seasons of IPL cricket** (2008–2024) with ball-by-ball granularity. Built to uncover patterns in batting, bowling, team performance, and match outcomes.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=flat&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=flat&logo=pandas&logoColor=white)

---

## 📊 What's Inside

| Tab | What You'll Find |
|-----|-----------------|
| **Overview** | Season trends, toss impact analysis, win type distribution |
| **Batting** | Top run-scorers, strike rate vs runs scatter, phase-wise scoring |
| **Bowling** | Top wicket-takers, economy analysis, dismissal types treemap |
| **Teams** | Win counts, title history, win percentage comparison |
| **Head to Head** | Pick any two teams — see their rivalry across seasons |

## 🔑 Key Insights

- **Average first innings scores** jumped from ~150 (2008) to ~190 (2024)
- Teams choosing to **field first win 54%** of the time vs 45% when batting first
- **Virat Kohli** leads all-time runs (8,000+), but **AB de Villiers** has a higher strike rate
- **Bumrah** uniquely combines high wickets with elite economy
- **CSK & MI** dominate titles and win percentage across all seasons

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/Robin2906-ai/ipl-analytics-dashboard.git
cd ipl-analytics-dashboard

# Install dependencies
pip install -r requirements.txt

# Launch the dashboard
streamlit run app.py
```

## 📁 Project Structure

```
ipl-analytics-dashboard/
├── data/
│   ├── matches.csv          # Match-level data (1,095 matches)
│   └── deliveries.csv       # Ball-by-ball data (260,920 deliveries)
├── app.py                   # Main Streamlit application
├── requirements.txt         # Python dependencies
└── README.md
```

## 🛠️ Tech Stack

- **Python** — core language
- **Pandas** — data cleaning, aggregation, feature engineering
- **Plotly** — interactive visualizations (bar, scatter, treemap, pie)
- **Streamlit** — web app framework with sidebar filters and tabs

## 📈 Data Source

[IPL Complete Dataset 2008–2024](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020) from Kaggle

## 📝 Skills Demonstrated

- Real-world **data cleaning** (team name standardization across seasons)
- Advanced **pandas** operations (groupby, merge, aggregation pipelines)
- Interactive **data visualization** with Plotly
- **Web app deployment** with Streamlit
- Deriving actionable **insights from data**

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/Robin2906-ai">Aryan</a>
</p>
