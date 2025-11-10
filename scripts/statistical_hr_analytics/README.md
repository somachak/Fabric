# 📊 Statistical HR Compensation Analytics Platform

A powerful Streamlit application that applies advanced statistical methods to HR compensation scenarios, leveraging extracted knowledge from statistics textbooks.

## 🎯 What It Does

This platform combines:
- **Statistical Rigor**: Applies methods from regression, hypothesis testing, survival analysis, and more
- **HR Domain Expertise**: Tailored specifically for compensation analysis
- **Visual Intelligence**: Interactive plots, diagrams, and visualizations
- **Extracted Knowledge**: Uses your processed statistics textbook content
- **Code Generation**: Produces ready-to-run Python analysis code

## 🚀 Quick Start

### Prerequisites

1. **Processed Statistics Knowledge Base** (from batch PDF processor)
2. **Fabric installed** with the `apply_statistics_to_hr_compensation` pattern
3. **Python 3.8+** with statistical libraries

### Installation

```bash
# Navigate to the app directory
cd scripts/statistical_hr_analytics

# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run statistical_hr_app.py
```

### First Time Setup

1. **Process your statistics PDFs** (if you haven't already):
   ```bash
   cd scripts/batch_pdf_processor
   python3 batch_processor.py ~/Desktop/Kindle\ Content/Stats/ -o ~/statistics_knowledge_base
   ```

2. **Configure in the app**:
   - Open the sidebar
   - Set "Path to processed PDFs" to your output directory (e.g., `~/statistics_knowledge_base`)
   - Click "🔄 Load Knowledge Base"

3. **Start analyzing**!

## 📊 Features

### 1. Pre-Built Statistical Scenarios

- **📊 Salary Regression Analysis**: Multiple regression for compensation determinants
- **⚖️ Pay Equity Analysis**: Identify unexplained wage gaps
- **📈 Retention Modeling**: Survival analysis for attrition prediction
- **🎯 Promotion Probability**: Logistic regression for career advancement
- **📊 Salary Band Design**: Quantile regression for data-driven bands
- **📉 Compensation Trends**: Time series forecasting

### 2. Custom Statistical Questions

Ask any HR compensation question and get:
- Appropriate statistical method selection
- Mathematical formulation (with LaTeX)
- Python implementation code
- Visualizations
- Business interpretation

**Example Questions**:
- "Is there a significant gender pay gap in our engineering department after controlling for experience?"
- "What factors predict employee retention using Cox regression?"
- "Design salary bands for software engineers using quantile regression"
- "Forecast next year's compensation budget using ARIMA time series"

### 3. Sample Data Generation

Built-in realistic sample datasets for:
- Salary analysis (with demographics, experience, education)
- Retention modeling (with tenure, satisfaction, promotions)
- Pay equity (with protected characteristics and controls)
- Promotion prediction (with performance and development metrics)

### 4. Interactive Code Execution

- **View Generated Code**: See the full Python analysis
- **Execute Interactively**: Run code directly in the app
- **Modify & Experiment**: Adjust parameters and re-run

### 5. Visual Intelligence

- **Statistical Plots**: Distribution plots, regression diagnostics, confidence intervals
- **Mermaid Diagrams**: Analysis workflow visualizations
- **Interactive Charts**: Explore results dynamically

## 🎓 Statistical Methods Covered

### Regression Analysis
- Simple & Multiple Linear Regression
- Logistic Regression (Binary outcomes)
- Quantile Regression (Salary bands)
- Polynomial & Non-linear Models

### Hypothesis Testing
- t-tests (Compare two groups)
- ANOVA (Compare multiple groups)
- Chi-square (Categorical associations)
- Non-parametric tests (Mann-Whitney, Kruskal-Wallis)

### Time Series
- Trend Analysis
- ARIMA Forecasting
- Exponential Smoothing

### Survival Analysis
- Kaplan-Meier Curves
- Cox Proportional Hazards
- Parametric Survival Models

### Multivariate Methods
- PCA (Dimensionality reduction)
- Clustering (Employee segmentation)
- Factor Analysis

### Causal Inference
- Propensity Score Matching
- Difference-in-Differences
- Instrumental Variables

## 📖 Usage Examples

### Example 1: Salary Regression Analysis

1. Click "📊 Salary Regression Analysis"
2. Click "🎲 Generate Sample Data"
3. Click "🚀 Run Statistical Analysis"
4. Get:
   - Multiple regression model
   - Coefficient interpretations
   - Diagnostic plots
   - Python code to reproduce

### Example 2: Pay Equity Analysis

```
Question: "Conduct a pay equity analysis for our tech department.
Control for years of experience, education level, and performance rating.
Test if there's a significant gender pay gap."
```

**Result**:
- Multiple regression with controls
- Statistical significance tests
- Effect size quantification
- Business recommendations

### Example 3: Custom Analysis

```
Question: "Model employee attrition using survival analysis.
Identify which factors (salary satisfaction, promotion history, commute time)
significantly predict time-to-departure."
```

**Result**:
- Cox regression model
- Hazard ratios for each factor
- Survival curves by group
- Interpretation for HR decision-making

## 🗂️ App Structure

```
statistical_hr_analytics/
├── statistical_hr_app.py      # Main Streamlit app
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── examples/                   # Example data (optional)
    ├── sample_salary_data.csv
    └── sample_retention_data.csv
```

## 📊 Working with Your Data

### Data Format

The app expects CSV files with appropriate column names:

**For Salary Analysis**:
```python
- employee_id
- salary
- years_experience
- education_level
- department
- performance_rating
- gender (if doing equity analysis)
```

**For Retention Modeling**:
```python
- employee_id
- tenure_months
- left (0/1)
- satisfaction_score
- promotions
- department
```

**For Promotion Analysis**:
```python
- employee_id
- promoted (0/1)
- performance_rating
- years_in_role
- certifications
- projects_completed
```

### Upload Your Own Data

1. Prepare CSV file with appropriate columns
2. Uncheck "Use Sample Data" in sidebar
3. Upload your CSV file
4. Run analysis

## 🎨 Customization

### Add New Scenarios

Edit `statistical_hr_app.py`:

```python
with col1:
    if st.button("🎯 Your Custom Scenario", use_container_width=True):
        st.session_state.scenario = "custom_scenario"
        st.session_state.scenario_question = "Your statistical question here"
```

### Modify Sample Data Generation

Update the `generate_sample_data()` function:

```python
elif scenario_type == "your_new_type":
    data = pd.DataFrame({
        # Your custom data structure
    })
```

### Integrate with Your Knowledge Base

The app automatically loads processed PDF content from your knowledge base path. To reference specific methods:

```python
knowledge = load_statistics_knowledge(knowledge_path)
# Use extracted statistical methods in analysis
```

## 🔬 Advanced Features

### Code Execution Safety

⚠️ **Important**: Only enable "Execute Code Automatically" if you trust the generated code.

The app can:
- Display generated Python code
- Execute code in a sandboxed environment
- Show plots and results inline
- Handle errors gracefully

### Knowledge Base Integration

The app integrates with your processed statistics PDFs:

1. **Loads extracted knowledge** from processed textbooks
2. **References methods** from your knowledge base
3. **Applies techniques** described in the source material
4. **Cites sources** when using specific methods

### Analysis History

Track all your analyses:
- View past questions
- Review results
- Re-run analyses
- Compare approaches

## 🎯 Real-World Applications

### HR Professionals
- Conduct pay equity audits
- Design data-driven compensation structures
- Analyze retention patterns
- Model promotion probabilities

### Data Scientists
- Apply statistical methods to HR problems
- Generate analysis code quickly
- Validate assumptions
- Communicate results to stakeholders

### Compensation Analysts
- Benchmark against market data
- Design salary bands
- Forecast budget needs
- Assess competitiveness

### People Analytics Teams
- Build predictive models
- Test hypotheses
- Quantify interventions
- Support evidence-based decisions

## 🐛 Troubleshooting

### "Pattern not found" Error

**Solution**: Ensure the `apply_statistics_to_hr_compensation` pattern exists:

```bash
ls ~/.config/fabric/patterns/apply_statistics_to_hr_compensation/
```

If missing, copy from the data/patterns directory.

### "Knowledge base empty"

**Solution**: Process your PDFs first:

```bash
cd scripts/batch_pdf_processor
python3 batch_processor.py /path/to/pdfs -o ~/statistics_knowledge_base
```

### "Module not found" Errors

**Solution**: Install all requirements:

```bash
pip install -r requirements.txt
```

### Mermaid Diagrams Not Rendering

**Solution**: Install streamlit-mermaid:

```bash
pip install streamlit-mermaid
```

## 📚 Integration with Fabric

This app works seamlessly with Fabric patterns:

1. **Uses** the `apply_statistics_to_hr_compensation` pattern
2. **Calls** fabric via subprocess
3. **Parses** output for visualization
4. **Executes** generated code

**Manual Pattern Usage**:

```bash
echo "Analyze salary equity using regression" | \
  fabric --pattern apply_statistics_to_hr_compensation
```

## 🚀 Next Steps

After using the app:

1. **Export analyses** to reports
2. **Refine generated code** for production use
3. **Build dashboards** with results
4. **Automate** recurring analyses
5. **Share insights** with stakeholders

## 🤝 Contributing

Ideas for enhancements:
- Add more pre-built scenarios
- Integrate with HR systems (Workday, BambooHR)
- Export to PowerPoint/PDF reports
- Real-time data connections
- A/B test simulators
- Interactive scenario builders

## 📖 Learning Resources

### In-App Learning

- Tab 4: "🎓 Learning" - Statistical methods overview
- Knowledge Base tab - Browse extracted textbook content
- Analysis History - Review past work

### External Resources

- Your processed statistics textbooks (in knowledge base)
- Fabric documentation: https://github.com/danielmiessler/fabric
- Statsmodels docs: https://www.statsmodels.org/
- Scikit-learn guide: https://scikit-learn.org/

## 💡 Tips for Best Results

1. **Start simple** - Use pre-built scenarios first
2. **Understand your data** - Check distributions and missing values
3. **Validate assumptions** - Review diagnostic plots
4. **Interpret carefully** - Statistical significance ≠ practical importance
5. **Iterate** - Try multiple approaches
6. **Document** - Save analyses to history
7. **Communicate** - Focus on business implications

## 📊 Example Workflow

```
1. Load Knowledge Base → Get statistical methods from textbooks
2. Select Scenario → Choose analysis type
3. Generate/Upload Data → Prepare dataset
4. Run Analysis → Apply statistical methods
5. Review Results → Interpret findings
6. Execute Code → Generate plots
7. Make Decisions → Use insights for action
8. Save Analysis → Document in history
```

---

**Built with ❤️ for HR Analytics**

Combining statistical rigor with HR domain expertise through AI-powered analysis.
