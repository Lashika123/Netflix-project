## 🔍 Project Overview

Netflix hosts a vast catalog of movies and TV shows across genres, countries, and languages.
This project analyzes Netflix content data to understand **content distribution, release trends, genre popularity, and regional patterns**.

The goal is to transform raw streaming data into **actionable insights** that support data-driven decisions in content planning and user engagement.

---

## 🎯 Project Objectives

* Analyze Netflix movies and TV shows catalog
* Identify trends in content type, genre, and ratings
* Study release patterns over time
* Understand country-wise and genre-wise content distribution
* Generate business insights for content strategy

---

## 🛠️ Tech Stack

* **Python**
* **Pandas & NumPy** – Data cleaning and analysis
* **Matplotlib & Seaborn** – Data visualization
* **Jupyter Notebook** – Exploratory data analysis

---

## 📂 Project Structure

```
├── netflix_data_analysis.ipynb     # Data cleaning & EDA
├── netflix_titles.csv              # Dataset
├── README.md
```

---

## 📊 Dataset Description

* **Source:** Netflix Movies and TV Shows dataset
* **Records:** Movies & TV shows available on Netflix
* **Key Columns:**

  * `type` (Movie / TV Show)
  * `title`
  * `director`
  * `cast`
  * `country`
  * `date_added`
  * `release_year`
  * `rating`
  * `duration`
  * `listed_in` (genres)
  * `description`

---

## 🧹 Data Cleaning & Preparation

Performed the following steps:

* Handled missing values in director, cast, and country
* Converted date fields to datetime format
* Extracted year, month, and duration features
* Split and standardized genre and country fields
* Prepared clean, analysis-ready data

---

## 📈 Exploratory Data Analysis (EDA)

### Key Analyses Performed

* Distribution of **Movies vs TV Shows**
* Content growth trend by year
* Top genres on Netflix
* Country-wise content contribution
* Rating-wise content distribution
* Duration analysis for movies and TV shows

---

## 🔍 Key Insights

* Movies dominate Netflix’s catalog compared to TV shows
* Significant growth in content addition after 2015
* Drama and International content are the most popular genres
* The United States contributes the highest volume of content
* Most movies fall within the 80–120 minute duration range

---

## 📌 Business Insights

* Netflix focuses heavily on **movie-based content expansion**
* Strong emphasis on **international and regional content**
* Opportunity to increase **TV show production** for long-term engagement
* Genre diversity supports global audience reach

---

## 🚀 How to Run the Project

1️⃣ Install required libraries:

```bash
pip install pandas numpy matplotlib seaborn
```

2️⃣ Open the notebook:

```bash
jupyter notebook netflix_data_analysis.ipynb
```

3️⃣ Run all cells to view analysis and visualizations

---

## 📌 Use Cases

* Content strategy planning
* Market and genre trend analysis
* Streaming platform analytics
* Data analysis portfolio project

---

## 🏁 Conclusion

This project demonstrates a **complete data analytics workflow**, including:

* Data cleaning and preprocessing
* Exploratory data analysis
* Insight generation and visualization



