# 🚀 Deployment Guide

**Complete guide to deploying your NYC Education Analysis project**

**Created:** October 6, 2025

---

## 📋 Table of Contents

1. [Dashboard Deployment (Streamlit Cloud)](#1-dashboard-deployment)
2. [GitHub Pages Deployment](#2-github-pages-deployment)
3. [Docker Deployment](#3-docker-deployment)
4. [Heroku Deployment](#4-heroku-deployment)
5. [Sharing Your Work](#5-sharing-your-work)

---

## 1. Dashboard Deployment (Streamlit Cloud)

### Prerequisites

- GitHub account
- Streamlit Cloud account (free at streamlit.io)
- Code pushed to GitHub

### Step-by-Step

#### 1.1 Prepare Your Repository

Create a `requirements.txt` for deployment:

```bash
# Generate from your current environment
pip freeze > requirements.txt
```

Or create a minimal one:

```text
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.14.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

#### 1.2 Create Streamlit Config

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
```

#### 1.3 Add Data Files

Ensure your processed data is in the repo:

- `data/processed/nyc_education_analyzed.csv`
- Or commit raw data files

#### 1.4 Deploy to Streamlit Cloud

1. Go to <https://streamlit.io/cloud>
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Main file: `scripts/education_dashboard.py`
6. Click "Deploy"

**URL:** Your app will be at `https://[your-username]-[repo-name].streamlit.app`

---

## 2. GitHub Pages Deployment

Deploy your interactive maps and visualizations.

### 2.1 Create HTML Export Notebook

Run your notebooks to generate HTML files:

- `nyc_schools_map.html`
- `nyc_schools_heatmap.html`
- `borough_geographic_analysis.png`

### 2.2 Create GitHub Pages Site

```bash
# Create docs directory for GitHub Pages
mkdir -p docs/visualizations

# Copy HTML maps
cp data/processed/*.html docs/visualizations/

# Copy images
cp data/processed/*.png docs/visualizations/
```

### 2.3 Create Index Page

Create `docs/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>NYC Education Analysis</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        background-color: #f5f5f5;
      }
      h1 {
        color: #1f77b4;
      }
      .card {
        background: white;
        padding: 20px;
        margin: 20px 0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }
      .btn {
        display: inline-block;
        padding: 10px 20px;
        background: #1f77b4;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        margin: 10px 10px 10px 0;
      }
      .btn:hover {
        background: #1557a0;
      }
    </style>
  </head>
  <body>
    <h1>🎓 NYC School Performance Analysis</h1>

    <div class="card">
      <h2>Interactive Maps</h2>
      <p>Explore NYC schools geographically with interactive visualizations.</p>
      <a href="visualizations/nyc_schools_map.html" class="btn"
        >🗺️ School Map</a
      >
      <a href="visualizations/nyc_schools_heatmap.html" class="btn"
        >🔥 Heat Map</a
      >
      <a href="visualizations/nyc_schools_clusters.html" class="btn"
        >📍 Cluster View</a
      >
    </div>

    <div class="card">
      <h2>Data Insights</h2>
      <p>Analysis of 460+ NYC schools with SAT scores and demographics.</p>
      <ul>
        <li>Average SAT Score: ~1,215 points</li>
        <li>Top School: Stuyvesant High School</li>
        <li>5 Boroughs Analyzed</li>
      </ul>
    </div>

    <div class="card">
      <h2>Project Links</h2>
      <a href="https://github.com/[your-username]/[repo-name]" class="btn"
        >GitHub Repository</a
      >
      <a href="[streamlit-url]" class="btn">Live Dashboard</a>
    </div>
  </body>
</html>
```

### 2.4 Enable GitHub Pages

1. Go to repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main`, folder: `/docs`
4. Save

**URL:** `https://[username].github.io/[repo-name]/`

---

## 3. Docker Deployment

Run your dashboard in a container.

### 3.1 Update Dockerfile

Your existing `Dockerfile` should work. Verify it has:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements-datascience.txt .
RUN pip install --no-cache-dir -r requirements-datascience.txt
RUN pip install streamlit folium geopandas

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "scripts/education_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 3.2 Build and Run

```bash
# Build image
docker build -t nyc-education-dashboard .

# Run container
docker run -p 8501:8501 nyc-education-dashboard

# Access at http://localhost:8501
```

### 3.3 Docker Compose

Update `docker-compose.yml`:

```yaml
version: "3.8"

services:
  dashboard:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./notebooks:/app/notebooks
    environment:
      - PYTHONUNBUFFERED=1
```

Run with: `docker-compose up`

---

## 4. Heroku Deployment

### 4.1 Create Heroku Files

Create `Procfile`:

```
web: streamlit run scripts/education_dashboard.py --server.port=$PORT --server.address=0.0.0.0
```

Create `runtime.txt`:

```
python-3.11.9
```

Create `setup.sh`:

```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

### 4.2 Deploy

```bash
# Install Heroku CLI first (https://devcenter.heroku.com/articles/heroku-cli)

# Login
heroku login

# Create app
heroku create nyc-education-dashboard

# Push to Heroku
git push heroku main

# Open app
heroku open
```

---

## 5. Sharing Your Work

### 5.1 Create a README

Enhance your `README.md`:

```markdown
# 🎓 NYC School Performance Analysis

Analysis of 460+ NYC schools with SAT scores, demographics, and predictive modeling.

## 🌟 Features

- **Interactive Dashboard**: Explore school performance with filters and visualizations
- **Geographic Analysis**: Interactive maps showing school locations and performance
- **Time Series Analysis**: Track trends and changes over time
- **Predictive Modeling**: ML models to identify success factors

## 🚀 Live Demo

- **Dashboard**: [Streamlit URL]
- **Maps**: [GitHub Pages URL]

## 📊 Key Findings

- Average SAT: 1,215 points
- Top School: Stuyvesant High School (2,087)
- Manhattan leads in average performance
- Strong correlation between reading and writing scores

## 🛠️ Technologies

- Python, Pandas, NumPy
- Streamlit, Plotly, Folium
- Scikit-learn for ML
- Jupyter for analysis

## 📷 Screenshots

![Dashboard](docs/images/dashboard-screenshot.png)
![Map](docs/images/map-screenshot.png)

## 🏃 Quick Start

\`\`\`bash

# Clone repository

git clone https://github.com/[username]/[repo].git

# Install dependencies

pip install -r requirements.txt

# Run dashboard

streamlit run scripts/education_dashboard.py
\`\`\`

## 📁 Project Structure

\`\`\`
├── data/ # Data files
├── notebooks/ # Jupyter analysis
├── scripts/ # Python scripts
└── docs/ # Documentation
\`\`\`

## 📝 License

MIT License

## 👤 Author

[Your Name] - [Your LinkedIn/GitHub]
```

### 5.2 Create Screenshots

Run your dashboard and take screenshots:

```bash
mkdir -p docs/images

# Run dashboard
streamlit run scripts/education_dashboard.py

# Take screenshots and save to docs/images/
```

### 5.3 Write a Blog Post

Structure:

1. **Introduction**: What problem you solved
2. **Data**: Where you got it, how much
3. **Analysis**: Key insights and methods
4. **Visualizations**: Maps, charts, dashboard
5. **Results**: Findings and conclusions
6. **Technical Details**: Tools and techniques
7. **Lessons Learned**: What you discovered

Platforms:

- Medium
- Dev.to
- Personal blog
- LinkedIn article

### 5.4 Create a Portfolio Page

Include:

- Project description
- Live demo links
- Screenshots/GIFs
- Code highlights
- Key findings
- Technologies used
- GitHub link

---

## 📦 Pre-Deployment Checklist

- [ ] All data files included or accessible
- [ ] `requirements.txt` is complete
- [ ] Secrets/credentials removed (no API keys in code)
- [ ] `.gitignore` configured properly
- [ ] README.md is comprehensive
- [ ] Code is documented
- [ ] Tests pass
- [ ] Dashboard runs locally
- [ ] Maps generate successfully
- [ ] No hardcoded paths (use `Path` objects)
- [ ] License added
- [ ] Screenshots taken

---

## 🔧 Troubleshooting

### Streamlit Issues

**Problem:** App won't start

```bash
# Check logs in Streamlit Cloud
# Verify requirements.txt has all dependencies
# Ensure data files are accessible
```

**Problem:** Data not loading

```bash
# Check file paths (use relative paths)
# Verify data files are in repo
# Check file size limits (Streamlit Cloud: 200MB)
```

### GitHub Pages Issues

**Problem:** Maps not displaying

```bash
# Ensure HTML files are in /docs
# Check file names in index.html match actual files
# Verify GitHub Pages is enabled
```

### Docker Issues

**Problem:** Build fails

```bash
# Check Dockerfile syntax
# Verify base image availability
# Test locally first
```

---

## 🎉 You're Ready

Your project is now:

- ✅ Production-ready
- ✅ Shareable
- ✅ Portfolio-worthy
- ✅ Deployable

**Next Steps:**

1. Choose a deployment method
2. Follow the steps above
3. Share your work!
4. Add to resume/portfolio

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [GitHub Pages Guide](https://pages.github.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Heroku Python Guide](https://devcenter.heroku.com/articles/python-support)

---

**Questions?** Check the docs or create an issue on GitHub!

**Good luck with your deployment! 🚀**
