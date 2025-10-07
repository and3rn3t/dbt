# Deployment Script for NYC Education Dashboard
# Creates all necessary files for deployment

Write-Host "🚀 NYC Education Dashboard - Deployment Setup" -ForegroundColor Cyan
Write-Host "=" * 60
Write-Host ""

# Step 1: Create requirements.txt
Write-Host "📦 Step 1: Creating requirements.txt..." -ForegroundColor Yellow

$requirements = @"
# Core Data Science
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.14.0
scipy>=1.10.0

# Web & Visualization
streamlit>=1.28.0
folium>=0.14.0

# Machine Learning
scikit-learn>=1.3.0

# File Support
openpyxl>=3.1.0
pyarrow>=12.0.0

# Jupyter
ipykernel>=6.25.0
jupyter>=1.0.0
"@

Set-Content -Path "requirements.txt" -Value $requirements
Write-Host "   ✅ Created requirements.txt" -ForegroundColor Green

# Step 2: Create Streamlit config
Write-Host ""
Write-Host "⚙️  Step 2: Creating Streamlit configuration..." -ForegroundColor Yellow

if (!(Test-Path -Path ".streamlit")) {
    New-Item -ItemType Directory -Path ".streamlit" | Out-Null
}

$streamlitConfig = @"
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
enableXsrfProtection = false
"@

Set-Content -Path ".streamlit/config.toml" -Value $streamlitConfig
Write-Host "   ✅ Created .streamlit/config.toml" -ForegroundColor Green

# Step 3: Create Procfile for Heroku
Write-Host ""
Write-Host "📝 Step 3: Creating Heroku deployment files..." -ForegroundColor Yellow

$procfile = "web: streamlit run scripts/education_dashboard.py --server.port=`$PORT --server.address=0.0.0.0"
Set-Content -Path "Procfile" -Value $procfile
Write-Host "   ✅ Created Procfile" -ForegroundColor Green

$runtime = "python-3.11.9"
Set-Content -Path "runtime.txt" -Value $runtime
Write-Host "   ✅ Created runtime.txt" -ForegroundColor Green

# Step 4: Create GitHub Pages structure
Write-Host ""
Write-Host "🌐 Step 4: Setting up GitHub Pages..." -ForegroundColor Yellow

if (!(Test-Path -Path "docs/visualizations")) {
    New-Item -ItemType Directory -Path "docs/visualizations" -Force | Out-Null
}

# Copy maps if they exist
if (Test-Path -Path "data/processed/*.html") {
    Copy-Item -Path "data/processed/*.html" -Destination "docs/visualizations/" -ErrorAction SilentlyContinue
    Write-Host "   ✅ Copied HTML maps to docs/visualizations/" -ForegroundColor Green
}

# Copy images if they exist
if (Test-Path -Path "data/processed/*.png") {
    Copy-Item -Path "data/processed/*.png" -Destination "docs/visualizations/" -ErrorAction SilentlyContinue
    Write-Host "   ✅ Copied PNG images to docs/visualizations/" -ForegroundColor Green
}

# Step 5: Create simple index.html
$indexHtml = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NYC Education Analysis</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1f77b4;
            margin-top: 0;
            font-size: 2.5em;
        }
        .card {
            background: #f8f9fa;
            padding: 25px;
            margin: 20px 0;
            border-radius: 8px;
            border-left: 4px solid #1f77b4;
        }
        .card h2 {
            margin-top: 0;
            color: #333;
        }
        .btn {
            display: inline-block;
            padding: 12px 24px;
            background: #1f77b4;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            margin: 10px 10px 10px 0;
            transition: background 0.3s;
        }
        .btn:hover {
            background: #1557a0;
        }
        ul {
            line-height: 1.8;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .stat-box {
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #1f77b4;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 NYC School Performance Analysis</h1>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">460+</div>
                <div class="stat-label">Schools Analyzed</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">1,215</div>
                <div class="stat-label">Avg SAT Score</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">5</div>
                <div class="stat-label">Boroughs Covered</div>
            </div>
        </div>

        <div class="card">
            <h2>📊 Interactive Dashboard</h2>
            <p>Explore school performance with interactive filters, charts, and detailed analytics.</p>
            <a href="#" class="btn">🚀 Launch Dashboard</a>
            <p style="margin-top: 10px; color: #666; font-size: 0.9em;">
                <em>Note: Add your Streamlit app URL above after deployment</em>
            </p>
        </div>

        <div class="card">
            <h2>🗺️ Interactive Maps</h2>
            <p>Explore NYC schools geographically with interactive visualizations.</p>
            <a href="visualizations/nyc_schools_map.html" class="btn">School Map</a>
            <a href="visualizations/nyc_schools_heatmap.html" class="btn">Heat Map</a>
            <a href="visualizations/nyc_schools_clusters.html" class="btn">Cluster View</a>
        </div>

        <div class="card">
            <h2>🔍 Key Insights</h2>
            <ul>
                <li><strong>Top Performer:</strong> Stuyvesant High School (2,087 total SAT)</li>
                <li><strong>Borough Leaders:</strong> Manhattan schools show highest average performance</li>
                <li><strong>Score Correlation:</strong> Strong correlation between reading and writing sections</li>
                <li><strong>Test Participation:</strong> Analyzed data from thousands of test takers</li>
            </ul>
        </div>

        <div class="card">
            <h2>🛠️ Technologies Used</h2>
            <p><strong>Data Analysis:</strong> Python, Pandas, NumPy, Scikit-learn</p>
            <p><strong>Visualization:</strong> Streamlit, Plotly, Matplotlib, Seaborn, Folium</p>
            <p><strong>Data Source:</strong> NYC Open Data</p>
        </div>

        <div class="card">
            <h2>📂 Project Resources</h2>
            <a href="https://github.com/and3rn3t/dbt" class="btn">GitHub Repository</a>
            <a href="../README.md" class="btn">Documentation</a>
        </div>
    </div>
</body>
</html>
"@

Set-Content -Path "docs/index.html" -Value $indexHtml
Write-Host "   ✅ Created docs/index.html" -ForegroundColor Green

# Step 6: Create .gitignore if needed
Write-Host ""
Write-Host "🔒 Step 5: Checking .gitignore..." -ForegroundColor Yellow

$gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Virtual Environment
.venv/
venv/
ENV/

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# Data (large files)
*.csv
*.xlsx
*.parquet
!data/processed/sample*.csv

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# dbt
target/
dbt_packages/
"@

if (!(Test-Path -Path ".gitignore")) {
    Set-Content -Path ".gitignore" -Value $gitignoreContent
    Write-Host "   ✅ Created .gitignore" -ForegroundColor Green
}
else {
    Write-Host "   ℹ️  .gitignore already exists" -ForegroundColor Cyan
}

# Step 7: Summary
Write-Host ""
Write-Host "=" * 60
Write-Host "✅ Deployment setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 What was created:" -ForegroundColor Cyan
Write-Host "   • requirements.txt - Python dependencies"
Write-Host "   • .streamlit/config.toml - Streamlit configuration"
Write-Host "   • Procfile - Heroku deployment"
Write-Host "   • runtime.txt - Python version"
Write-Host "   • docs/index.html - GitHub Pages site"
Write-Host "   • docs/visualizations/ - Map visualizations"
Write-Host ""
Write-Host "🚀 Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   1. Test Dashboard Locally:" -ForegroundColor White
Write-Host "      streamlit run scripts/education_dashboard.py"
Write-Host ""
Write-Host "   2. Deploy to Streamlit Cloud:" -ForegroundColor White
Write-Host "      • Go to https://streamlit.io/cloud"
Write-Host "      • Connect your GitHub repository"
Write-Host "      • Select scripts/education_dashboard.py"
Write-Host ""
Write-Host "   3. Enable GitHub Pages:" -ForegroundColor White
Write-Host "      • Go to repo Settings → Pages"
Write-Host "      • Source: Deploy from branch 'main' /docs"
Write-Host ""
Write-Host "   4. Push to GitHub:" -ForegroundColor White
Write-Host "      git add ."
Write-Host "      git commit -m 'Add deployment configuration'"
Write-Host "      git push origin main"
Write-Host ""
Write-Host "📚 Documentation: See docs/DEPLOYMENT_GUIDE.md for full details"
Write-Host ""
Write-Host "=" * 60
Write-Host ""
