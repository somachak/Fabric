# 📊 Example Statistical HR Compensation Scenarios

This document provides detailed examples of statistical analyses you can run using the platform.

---

## Scenario 1: Salary Regression Analysis

### Business Question
"What factors drive salary differences in our engineering department, and by how much?"

### Statistical Approach
**Multiple Linear Regression**

### Input to App
```
Analyze salary determinants using multiple regression for our engineering department.
Include: years of experience, education level, programming languages known,
GitHub contributions, and performance rating.

Provide:
- Regression coefficients with confidence intervals
- R-squared and model diagnostics
- Interpretation for each significant predictor
- Predicted salary for typical profiles
```

### Expected Output
- Mathematical model: `Salary = β₀ + β₁·Experience + β₂·Education + ...`
- Coefficient interpretations (e.g., "Each additional year of experience = $3,500 ± $800")
- R² value showing model fit
- Residual plots for assumption checking
- Python code to reproduce analysis

### Sample Results Interpretation
```
Model Results:
- R² = 0.72 (model explains 72% of salary variation)
- Experience coefficient: $3,500 per year (p < 0.001) ***
- Master's degree: +$12,000 vs Bachelor's (p < 0.01) **
- Python proficiency: +$8,500 (p < 0.05) *
- Performance rating: +$6,200 per point (p < 0.001) ***
```

---

## Scenario 2: Pay Equity Analysis

### Business Question
"Is there a gender pay gap after controlling for legitimate factors?"

### Statistical Approach
**Multiple Regression with Demographic Variables**

### Input to App
```
Conduct a pay equity analysis to identify unexplained gender wage gaps.

Control for:
- Years of experience
- Education level
- Department
- Job level
- Performance rating
- Geographic location

Test if gender coefficient is statistically significant after controls.
Provide effect size and confidence intervals.
```

### Expected Output
- Regression model with controls
- Gender coefficient (adjusted pay gap)
- Statistical significance test
- Effect size quantification
- Recommendations for remediation

### Sample Results Interpretation
```
Adjusted Gender Pay Gap Analysis:

Unadjusted gap: Women earn $8,500 less (p < 0.001)
After controlling for legitimate factors: $2,100 less (p = 0.08)

Interpretation:
- 74% of gap ($6,400) explained by factors like experience, level
- Remaining $2,100 gap not statistically significant (p > 0.05)
- However, still represents 2.5% of average salary
- Recommendation: Monitor and address through transparent criteria
```

---

## Scenario 3: Retention Modeling (Survival Analysis)

### Business Question
"What factors predict employee attrition, and when are employees most likely to leave?"

### Statistical Approach
**Cox Proportional Hazards / Kaplan-Meier**

### Input to App
```
Model employee retention using survival analysis.

Include:
- Tenure (time variable)
- Left company (event variable)
- Salary satisfaction (1-10 scale)
- Promotion history (number of promotions)
- Commute time (minutes)
- Manager rating
- Department

Provide:
- Survival curves
- Hazard ratios for each factor
- Median retention time
- High-risk employee profiles
```

### Expected Output
- Kaplan-Meier survival curves
- Cox regression hazard ratios
- Interpretation of retention predictors
- Risk stratification

### Sample Results Interpretation
```
Retention Analysis Results:

Median Time to Departure: 36 months

Hazard Ratios (Risk of Leaving):
- Low salary satisfaction (<5): HR = 3.2 (p < 0.001) ***
  → 3.2x more likely to leave than satisfied employees
- No promotions in 3 years: HR = 2.1 (p < 0.01) **
- Long commute (>60 min): HR = 1.6 (p < 0.05) *
- Department - Sales: HR = 1.4 vs Engineering (p = 0.03) *

High-Risk Profile:
Employees with low satisfaction + no recent promotion + long commute
→ 5.8x higher attrition risk (leave within 18 months)
```

---

## Scenario 4: Promotion Probability Modeling

### Business Question
"What predicts promotion success? Can we quantify the odds?"

### Statistical Approach
**Logistic Regression**

### Input to App
```
Use logistic regression to model promotion probability.

Predictors:
- Performance rating (1-5)
- Years in current role
- Certifications obtained
- Projects completed
- Visibility score (manager assessment)
- Education level

Outcome: Promoted (Yes/No) in past year

Provide:
- Odds ratios for each factor
- ROC curve and AUC
- Probability predictions for typical profiles
- Decision threshold recommendations
```

### Expected Output
- Logistic regression coefficients
- Odds ratios with confidence intervals
- Model accuracy metrics (AUC, accuracy, precision, recall)
- Predicted probabilities

### Sample Results Interpretation
```
Promotion Prediction Model:

AUC = 0.81 (Good discrimination)

Odds Ratios:
- Performance 5 vs 3: OR = 6.2 (p < 0.001)
  → 520% higher odds of promotion
- Certification: OR = 2.3 per cert (p < 0.01)
- Projects completed: OR = 1.15 per project (p < 0.05)
- Visibility high vs low: OR = 3.8 (p < 0.001)

Probability Examples:
- High performer (5), 2 certs, 10 projects, high visibility: 78% chance
- Average performer (3), no certs, 5 projects, medium vis: 22% chance
```

---

## Scenario 5: Salary Band Design

### Business Question
"Design data-driven salary bands based on our actual compensation distribution"

### Statistical Approach
**Quantile Regression**

### Input to App
```
Design salary bands using quantile regression at 25th, 50th, and 75th percentiles.

For: Software Engineers (all levels)

Model percentiles as function of:
- Years of experience
- Technical skills score
- Leadership scope (IC vs Manager)

Provide:
- Percentile curves over experience range
- Band widths and overlap
- Entry/mid/senior level band recommendations
```

### Expected Output
- Quantile regression models (3 models for 3 percentiles)
- Salary band curves
- Recommended band structure
- Comparison to current bands

### Sample Results Interpretation
```
Recommended Salary Bands for Software Engineers:

Entry Level (0-2 years):
- 25th percentile: $75,000
- 50th percentile: $85,000
- 75th percentile: $95,000
- Range: $75K - $95K (27% spread)

Mid Level (3-5 years):
- 25th percentile: $95,000
- 50th percentile: $110,000
- 75th percentile: $125,000
- Range: $95K - $125K (32% spread)

Senior Level (6+ years):
- 25th percentile: $125,000
- 50th percentile: $145,000
- 75th percentile: $170,000
- Range: $125K - $170K (36% spread)

Overlap: Mid-Senior overlap at $125K allows for growth within level
```

---

## Scenario 6: Compensation Trend Forecasting

### Business Question
"What should we budget for salary increases next year based on historical trends?"

### Statistical Approach
**Time Series Analysis (ARIMA)**

### Input to App
```
Forecast compensation trends using time series analysis.

Historical data: Monthly average salaries for past 5 years
Include:
- Seasonal components (annual review cycles)
- Trend component
- Market adjustment events

Provide:
- 12-month forecast
- Confidence intervals (80% and 95%)
- Expected year-over-year increase
- Budget recommendations
```

### Expected Output
- ARIMA model specification
- Trend decomposition
- Forecast with uncertainty bands
- Budget recommendations

### Sample Results Interpretation
```
Salary Trend Forecast:

Model: ARIMA(1,1,1) with seasonal component

Historical Trend: +3.2% annual increase (inflation-adjusted)

12-Month Forecast:
- Point estimate: +4.1% increase
- 80% confidence: 3.5% - 4.7%
- 95% confidence: 3.0% - 5.2%

Budget Recommendation:
- Conservative: Plan for +3.5% (lower 80% CI)
- Expected: +4.1% (point estimate)
- Contingency: Reserve for up to +5.2% (upper 95% CI)

For $50M total compensation:
- Conservative budget: +$1.75M
- Expected budget: +$2.05M
- Contingency: +$2.60M
```

---

## Scenario 7: Departmental Salary Comparison

### Business Question
"Are salary differences across departments justified by role differences?"

### Statistical Approach
**ANOVA / Multiple Comparisons**

### Input to App
```
Compare salaries across departments using ANOVA.

Departments: Engineering, Sales, Marketing, Operations

Control for:
- Job level (IC1-IC5, M1-M3)
- Years of experience
- Performance rating

Test:
1. Overall department effect
2. Pairwise comparisons (with Bonferroni correction)
3. Effect sizes
```

### Expected Output
- ANOVA F-test
- Pairwise comparison table
- Effect sizes (Cohen's d)
- Adjusted salary means by department

### Sample Results Interpretation
```
Departmental Salary Analysis:

Overall ANOVA: F(3, 496) = 12.4, p < 0.001 ***
→ Significant differences exist across departments

Adjusted Mean Salaries (controlling for level, experience, performance):
- Engineering: $95,000
- Sales: $88,000 (-$7,000 vs Eng)
- Marketing: $90,000 (-$5,000 vs Eng)
- Operations: $82,000 (-$13,000 vs Eng)

Pairwise Comparisons (Bonferroni adjusted):
- Eng vs Sales: p = 0.002 ** (significant, -7.3%)
- Eng vs Marketing: p = 0.08 (marginally significant)
- Eng vs Operations: p < 0.001 *** (significant, -13.7%)
- Sales vs Operations: p = 0.01 * (significant)

Interpretation:
Engineering premium appears justified by market demand and scarcity.
Operations department may need market adjustment.
```

---

## Scenario 8: Bonus Distribution Analysis

### Business Question
"Is our bonus distribution fair and aligned with performance?"

### Statistical Approach
**Correlation Analysis + Regression Diagnostics**

### Input to App
```
Analyze bonus distribution for fairness and performance alignment.

Variables:
- Bonus amount (% of salary)
- Performance rating (1-5)
- Department
- Tenure
- Salary level

Tests:
1. Correlation between performance and bonus
2. Distribution analysis (check for outliers, skewness)
3. Regression: Bonus ~ Performance + Department + Tenure
4. Residual analysis for fairness
```

### Expected Output
- Correlation coefficients
- Distribution plots
- Regression model
- Fairness diagnostics

### Sample Results Interpretation
```
Bonus Analysis Results:

Performance-Bonus Correlation: r = 0.64 (p < 0.001)
→ Moderate positive correlation (good alignment)

Distribution:
- Mean bonus: 12.3% of salary
- Median: 11.5% (slightly left-skewed)
- Range: 0% - 25%
- Top performers (rating 5): Average 18.5%
- Low performers (rating 2): Average 4.2%

Regression Results:
- Performance coefficient: +3.8% per rating point (p < 0.001)
- Rating 5 vs 3: +7.6% bonus (highly significant)
- Department effects: Not significant (good - no bias)
- Tenure: +0.2% per year (p = 0.03) - slight seniority effect

Fairness Check:
- No significant residual patterns by department ✓
- No gender bias in residuals (p = 0.62) ✓
- Outliers: 3 employees with bonuses >2 SD (investigate individually)

Recommendation: System appears fair and performance-aligned.
Consider tightening outlier policy.
```

---

## Tips for Using These Scenarios

1. **Copy the "Input to App" text** directly into the custom question field
2. **Modify for your context** - adjust variables, departments, specific requirements
3. **Generate or upload matching data** - use sample data or your own CSV
4. **Review the statistical approach** - ensure it matches your assumptions
5. **Interpret results** - focus on practical significance, not just p-values
6. **Iterate** - try different model specifications and controls

---

## Combining Multiple Analyses

For comprehensive compensation reviews, combine scenarios:

**Complete Equity Audit**:
1. Scenario 2 (Pay Equity) → Identify gaps
2. Scenario 7 (Departmental Comparison) → Context across org
3. Scenario 8 (Bonus Analysis) → Check variable pay
4. Scenario 3 (Retention) → Assess impact on attrition

**Strategic Compensation Planning**:
1. Scenario 6 (Trends) → Forecast budget needs
2. Scenario 5 (Salary Bands) → Design structure
3. Scenario 1 (Regression) → Understand drivers
4. Scenario 4 (Promotion) → Model career progression

---

## Next Steps After Analysis

1. **Validate findings** with HR stakeholders
2. **Check assumptions** using diagnostic plots
3. **Consider confounders** - are there unmeasured factors?
4. **Assess practical significance** - is it meaningful, not just statistically significant?
5. **Make recommendations** - translate stats to action
6. **Monitor over time** - track changes after interventions

---

**Remember**: Statistical analysis informs decisions but doesn't make them.
Always combine quantitative insights with qualitative judgment and organizational context.
