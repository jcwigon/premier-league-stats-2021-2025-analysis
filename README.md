# ⚽ Premier League Statistics Analysis 2021–2025

📌 **Project description:**  

This project presents a comprehensive analysis of data from the English Premier League for the 2021–2025 seasons. The aim was to go through the entire data workflow – from acquisition, through processing and analysis, to visualization of results – using modern programming tools and NoSQL solutions.

Key components of the project:

NoSQL database: I used MongoDB to store, efficiently search, and analyze match data. The project also demonstrates how to run queries on a NoSQL database and perform data analysis directly in MongoDB.
Python modules and classes: The codebase is structured as modular Python files and classes, ensuring a clear and easily expandable program architecture.
Data acquisition (Open Data): Match results and statistics were sourced from open data repositories.
Data analysis in Pandas: I performed data exploration, aggregation, and statistical calculations using the Pandas library.
Data visualization: Key findings and trends are presented as clear and informative charts generated in Python.
Through this project, I demonstrate in practice how to build custom Python modules, define classes, use NoSQL databases, acquire data from open sources, as well as analyze and search a MongoDB database, and present results in a clear visual form.

Additionally, as a football enthusiast, I have prepared interesting analyses that answer questions such as:

Do referees favor home teams?
Does home advantage really matter?
Which teams committed the most fouls in particular seasons?
Is the Premier League becoming more attacking-oriented each year?
Based on available data, I have also calculated a simplified, popular in modern football xG (Expected Goals) metric.

---

## 📊 Analyzed Statistics

The project analyzes key match indicators:

- ⚽ Number of goals (average per season, per team, season comparisons)
- 🎯 Shots (average, accuracy, home vs away)
- 📈 xG indicator (expected goals)
- 🚩 Cards (yellow, red)
- 🏆 Share of wins for home teams, away teams, and draws

---

## 🛠️ How to run the project

1. **Install the required libraries:**
   ```bash
   pip install -r requirements.txt
