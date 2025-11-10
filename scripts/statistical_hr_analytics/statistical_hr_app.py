"""
Statistical HR Compensation Analytics Platform

This Streamlit app applies advanced statistical methods to HR compensation scenarios,
leveraging extracted knowledge from statistics textbooks.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from subprocess import run, CalledProcessError
import os
import json
import logging
import shutil
from pathlib import Path
from datetime import datetime
import re

# Try to import streamlit-mermaid
try:
    from streamlit_mermaid import st_mermaid
    MERMAID_AVAILABLE = True
except ImportError:
    MERMAID_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page configuration
st.set_page_config(
    page_title="Statistical HR Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5em;
        font-weight: 600;
        background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .method-badge {
        background: #4ECDC4;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.85em;
        margin: 0.25rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📊 Statistical HR Analytics Platform</h1>', unsafe_allow_html=True)

# Initialize session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'current_data' not in st.session_state:
    st.session_state.current_data = None
if 'knowledge_base_path' not in st.session_state:
    st.session_state.knowledge_base_path = None
if 'column_mapping' not in st.session_state:
    st.session_state.column_mapping = {}

def load_statistics_knowledge(knowledge_path):
    """Load knowledge from multiple file formats: .md, .txt, .json"""
    knowledge_files = []

    if knowledge_path and os.path.exists(knowledge_path):
        # Supported file patterns and types
        file_patterns = [
            ("*.md", "Markdown"),
            ("*.txt", "Text"),
            ("*.json", "JSON")
        ]

        for pattern, file_type in file_patterns:
            for file in Path(knowledge_path).rglob(pattern):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()

                        # For JSON files, try to pretty-format
                        if file_type == "JSON":
                            try:
                                json_data = json.loads(content)
                                content = json.dumps(json_data, indent=2)
                            except json.JSONDecodeError:
                                # If invalid JSON, keep as plain text
                                pass

                        knowledge_files.append({
                            'filename': file.name,
                            'path': str(file),
                            'content': content,
                            'type': file_type,
                            'size': len(content)
                        })
                except Exception as e:
                    logger.error(f"Error loading {file}: {e}")

    # Sort by filename for consistent ordering
    knowledge_files.sort(key=lambda x: x['filename'])

    return knowledge_files

def find_fabric_executable():
    """Find the fabric executable in PATH or use local binary"""
    # First, try to find fabric in PATH
    fabric_path = shutil.which('fabric')

    if fabric_path:
        return fabric_path

    # If not in PATH, try the local repository fabric binary
    # Assuming the app is in scripts/statistical_hr_analytics/
    script_dir = Path(__file__).parent
    local_fabric = script_dir / '..' / '..' / 'fabric'

    if local_fabric.exists() and os.access(local_fabric, os.X_OK):
        return str(local_fabric.resolve())

    # Last resort: check if user has set FABRIC_PATH environment variable
    env_fabric = os.environ.get('FABRIC_PATH')
    if env_fabric and Path(env_fabric).exists():
        return env_fabric

    return None

def render_visual_output(output: str) -> None:
    """Render output with Mermaid diagram support"""
    mermaid_pattern = r'```mermaid\s*(.*?)```'
    mermaid_matches = re.findall(mermaid_pattern, output, re.DOTALL)

    if mermaid_matches:
        parts = re.split(mermaid_pattern, output, flags=re.DOTALL)
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part.strip():
                    st.markdown(part)
            else:
                st.markdown("### 📊 Analysis Flow")
                if MERMAID_AVAILABLE:
                    try:
                        st_mermaid(part.strip())
                    except Exception as e:
                        st.code(part.strip(), language="mermaid")
                else:
                    with st.expander("📊 Diagram Code", expanded=False):
                        st.code(part.strip(), language="mermaid")
    else:
        st.markdown(output)

def extract_and_run_code(output: str, data_context=None, auto_execute=False, column_mapping=None):
    """Extract Python code from output and optionally run it"""
    code_pattern = r'```python\s*(.*?)```'
    code_blocks = re.findall(code_pattern, output, re.DOTALL)

    if code_blocks:
        st.subheader("📝 Generated Analysis Code")

        for idx, code in enumerate(code_blocks, 1):
            # Apply column mapping if provided
            if column_mapping:
                for standard_name, actual_name in column_mapping.items():
                    # Replace column references in code
                    code = code.replace(f"'{standard_name}'", f"'{actual_name}'")
                    code = code.replace(f'"{standard_name}"', f'"{actual_name}"')
                    code = code.replace(f"['{standard_name}']", f"['{actual_name}']")
                    code = code.replace(f'["{standard_name}"]', f'["{actual_name}"]')

            with st.expander(f"Code Block {idx}", expanded=True):
                st.code(code, language='python')

                # Auto-execute or manual execute
                should_execute = auto_execute or st.button(f"▶️ Run Code Block {idx}", key=f"run_{idx}")

                if should_execute:
                    with st.spinner(f"Executing code block {idx}..."):
                        try:
                            # Create execution context with sample data
                            exec_globals = {
                                'pd': pd,
                                'np': np,
                                'plt': plt,
                                'sns': sns,
                                'stats': stats,
                                'sm': sm,
                                'st': st
                            }

                            if data_context is not None:
                                exec_globals['df'] = data_context

                            # Capture stdout for print statements
                            from io import StringIO
                            import sys
                            old_stdout = sys.stdout
                            sys.stdout = captured_output = StringIO()

                            # Execute code
                            exec(code, exec_globals)

                            # Restore stdout
                            sys.stdout = old_stdout
                            output_text = captured_output.getvalue()

                            # Show captured output
                            if output_text:
                                st.text(output_text)

                            # Show any generated plots
                            if plt.get_fignums():
                                st.pyplot(plt.gcf())
                                plt.clf()

                            st.success("✅ Code executed successfully!")

                        except Exception as e:
                            st.error(f"❌ Execution error: {str(e)}")
                            import traceback
                            st.code(traceback.format_exc())

def generate_sample_data(scenario_type):
    """Generate realistic sample HR compensation data"""
    np.random.seed(42)
    n = 500

    if scenario_type == "salary_analysis":
        data = pd.DataFrame({
            'employee_id': range(1, n+1),
            'salary': np.random.normal(85000, 25000, n).clip(45000, 200000),
            'years_experience': np.random.gamma(3, 2, n).clip(0, 30),
            'education': np.random.choice(['Bachelor', 'Master', 'PhD'], n, p=[0.5, 0.35, 0.15]),
            'department': np.random.choice(['Engineering', 'Sales', 'Marketing', 'Operations'], n),
            'performance_rating': np.random.normal(3.5, 0.8, n).clip(1, 5),
            'gender': np.random.choice(['Male', 'Female'], n),
            'age': np.random.normal(35, 8, n).clip(22, 65)
        })

    elif scenario_type == "retention":
        data = pd.DataFrame({
            'employee_id': range(1, n+1),
            'tenure_months': np.random.exponential(24, n).clip(1, 120),
            'left': np.random.choice([0, 1], n, p=[0.85, 0.15]),
            'salary': np.random.normal(80000, 20000, n).clip(45000, 150000),
            'satisfaction_score': np.random.normal(7, 2, n).clip(1, 10),
            'promotions': np.random.poisson(0.5, n),
            'department': np.random.choice(['Engineering', 'Sales', 'Marketing'], n)
        })

    elif scenario_type == "equity_analysis":
        data = pd.DataFrame({
            'employee_id': range(1, n+1),
            'salary': np.random.normal(90000, 30000, n).clip(50000, 200000),
            'gender': np.random.choice(['Male', 'Female'], n),
            'race': np.random.choice(['White', 'Asian', 'Black', 'Hispanic', 'Other'], n),
            'years_experience': np.random.gamma(3, 2, n).clip(0, 30),
            'education': np.random.choice(['Bachelor', 'Master', 'PhD'], n, p=[0.5, 0.35, 0.15]),
            'department': np.random.choice(['Engineering', 'Sales', 'Marketing'], n),
            'job_level': np.random.choice(['Junior', 'Mid', 'Senior', 'Lead'], n, p=[0.3, 0.4, 0.2, 0.1])
        })

    elif scenario_type == "promotion":
        data = pd.DataFrame({
            'employee_id': range(1, n+1),
            'promoted': np.random.choice([0, 1], n, p=[0.8, 0.2]),
            'performance_rating': np.random.normal(3.5, 0.8, n).clip(1, 5),
            'years_in_role': np.random.gamma(2, 1.5, n).clip(0.5, 15),
            'certifications': np.random.poisson(1, n),
            'projects_completed': np.random.poisson(8, n),
            'department': np.random.choice(['Engineering', 'Sales', 'Marketing'], n)
        })

    else:  # default
        data = pd.DataFrame({
            'employee_id': range(1, n+1),
            'salary': np.random.normal(80000, 25000, n).clip(45000, 200000),
            'years_experience': np.random.gamma(3, 2, n).clip(0, 30)
        })

    return data

# Sidebar
with st.sidebar:
    st.title("⚙️ Configuration")

    st.subheader("📚 Statistics Knowledge Base")
    knowledge_path = st.text_input(
        "Path to knowledge files",
        value=st.session_state.get('knowledge_base_path', '~/statistics_knowledge_base'),
        help="Path containing .md, .txt, or .json files with statistical knowledge"
    )
    st.caption("💡 Supports: Markdown (.md), Text (.txt), JSON (.json)")

    if st.button("🔄 Load Knowledge Base"):
        if knowledge_path:
            expanded_path = os.path.expanduser(knowledge_path)
            if os.path.exists(expanded_path):
                knowledge = load_statistics_knowledge(expanded_path)
                st.session_state.knowledge_files = knowledge
                st.session_state.knowledge_base_path = expanded_path
                st.success(f"✅ Loaded {len(knowledge)} knowledge files")
            else:
                st.error(f"❌ Path not found: {expanded_path}")
        else:
            st.error("❌ Please enter a path to your knowledge base")

    st.markdown("---")
    st.subheader("📊 Analysis Options")

    use_sample_data = st.checkbox("Use Sample Data", value=True,
                                   help="Generate sample data for demonstration")

    show_code = st.checkbox("Show Generated Code", value=True)
    execute_code = st.checkbox("Execute Code Automatically", value=False,
                                help="⚠️ Only enable if you trust the generated code")

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📊 Statistical Analysis", "📚 Knowledge Base", "📈 Analysis History", "🎓 Learning"])

with tab1:
    st.header("Statistical HR Compensation Analysis")

    st.markdown("""
    Apply rigorous statistical methods to HR compensation challenges. This platform uses
    statistical knowledge extracted from textbooks to guide analysis.
    """)

    # Scenario selection
    st.subheader("🎯 Select Analysis Scenario")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Salary Regression Analysis", use_container_width=True):
            st.session_state.scenario = "salary_regression"
            st.session_state.scenario_question = "Analyze salary determinants using multiple regression. Which factors significantly impact compensation?"

    with col2:
        if st.button("⚖️ Pay Equity Analysis", use_container_width=True):
            st.session_state.scenario = "pay_equity"
            st.session_state.scenario_question = "Conduct pay equity analysis to identify unexplained wage gaps controlling for legitimate factors."

    with col3:
        if st.button("📈 Retention Modeling", use_container_width=True):
            st.session_state.scenario = "retention"
            st.session_state.scenario_question = "Model employee retention using survival analysis. What factors predict attrition?"

    col4, col5, col6 = st.columns(3)

    with col4:
        if st.button("🎯 Promotion Probability", use_container_width=True):
            st.session_state.scenario = "promotion"
            st.session_state.scenario_question = "Use logistic regression to model promotion probability. What predicts career advancement?"

    with col5:
        if st.button("📊 Salary Band Design", use_container_width=True):
            st.session_state.scenario = "salary_bands"
            st.session_state.scenario_question = "Design data-driven salary bands using quantile regression. What are the 25th, 50th, 75th percentiles?"

    with col6:
        if st.button("📉 Compensation Trends", use_container_width=True):
            st.session_state.scenario = "trends"
            st.session_state.scenario_question = "Forecast compensation trends using time series analysis. What are expected salary increases?"

    st.markdown("---")

    # Custom question input
    st.subheader("💡 Or Ask Your Own Statistical Question")

    custom_question = st.text_area(
        "Describe your HR compensation problem:",
        value=st.session_state.get('scenario_question', ''),
        height=150,
        placeholder="Example: I want to determine if there's a significant gender pay gap in our engineering department after controlling for experience, education, and performance. Use appropriate statistical tests."
    )

    if custom_question:
        st.session_state.scenario_question = custom_question

    # Data upload or generation
    st.subheader("📂 Data")

    if use_sample_data:
        scenario_type = st.selectbox(
            "Sample data type:",
            ["salary_analysis", "retention", "equity_analysis", "promotion"],
            help="Choose the type of sample data to generate"
        )

        if st.button("🎲 Generate Sample Data"):
            sample_data = generate_sample_data(scenario_type)
            st.session_state.current_data = sample_data
            st.success(f"✅ Generated {len(sample_data)} sample records")

        if st.session_state.current_data is not None:
            with st.expander("👁️ Preview Data", expanded=False):
                st.dataframe(st.session_state.current_data.head(20))
                st.write("**Summary Statistics:**")
                st.dataframe(st.session_state.current_data.describe())
    else:
        uploaded_file = st.file_uploader("Upload your HR data (CSV)", type=['csv'])
        if uploaded_file:
            st.session_state.current_data = pd.read_csv(uploaded_file)
            st.success("✅ Data uploaded successfully!")
            with st.expander("👁️ Preview Data"):
                st.dataframe(st.session_state.current_data.head())

    # Column Mapping
    if st.session_state.current_data is not None:
        st.subheader("🔄 Column Mapping (Optional)")
        st.info("📋 Map your actual column names to standard variables. This makes the generated code work with YOUR data!")

        with st.expander("⚙️ Configure Column Mapping", expanded=False):
            st.markdown("**Your Columns:** " + ", ".join(st.session_state.current_data.columns.tolist()))

            standard_columns = {
                "salary": "Employee salary/compensation",
                "years_experience": "Years of work experience",
                "education": "Education level",
                "department": "Department/division",
                "performance_rating": "Performance score",
                "gender": "Gender",
                "age": "Age",
                "job_level": "Job level/grade",
                "race": "Race/ethnicity",
                "promoted": "Promotion status (0/1)",
                "left": "Attrition status (0/1)",
                "tenure_months": "Tenure in months"
            }

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Standard Variable**")
            with col2:
                st.markdown("**Your Column Name**")

            mapping = {}
            for std_col, description in standard_columns.items():
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**{std_col}**")
                    st.caption(description)
                with col2:
                    user_col = st.selectbox(
                        "Select column",
                        ["<not mapped>"] + st.session_state.current_data.columns.tolist(),
                        key=f"map_{std_col}",
                        label_visibility="collapsed"
                    )
                    if user_col != "<not mapped>":
                        mapping[std_col] = user_col

            if st.button("💾 Save Column Mapping"):
                st.session_state.column_mapping = mapping
                st.success(f"✅ Saved {len(mapping)} column mappings!")
                st.json(mapping)

            if st.session_state.column_mapping:
                st.markdown("**Current Mappings:**")
                st.json(st.session_state.column_mapping)

    # Run analysis
    st.markdown("---")

    if st.button("🚀 Run Statistical Analysis", type="primary", use_container_width=True):
        if not st.session_state.get('scenario_question'):
            st.warning("⚠️ Please select a scenario or enter a custom question")
        else:
            with st.spinner("🔬 Applying statistical methods..."):
                try:
                    # Find fabric executable
                    fabric_cmd = find_fabric_executable()

                    if not fabric_cmd:
                        st.error("❌ Fabric executable not found. Please install Fabric or set FABRIC_PATH environment variable.")
                        st.stop()

                    # Run the statistical analysis pattern
                    cmd = [fabric_cmd, "--pattern", "apply_statistics_to_hr_compensation"]

                    result = run(
                        cmd,
                        input=st.session_state.scenario_question,
                        capture_output=True,
                        text=True,
                        check=True
                    )

                    output = result.stdout.strip()

                    if output:
                        st.markdown("---")
                        st.markdown("## 📊 Statistical Analysis Results")

                        # Render the output with visual support
                        render_visual_output(output)

                        # Extract and show code
                        if show_code:
                            extract_and_run_code(
                                output,
                                st.session_state.current_data,
                                auto_execute=execute_code,
                                column_mapping=st.session_state.column_mapping
                            )

                        # Save to history
                        st.session_state.analysis_history.append({
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'question': st.session_state.scenario_question,
                            'output': output
                        })

                        st.success("✅ Analysis complete!")
                    else:
                        st.error("❌ No output generated")

                except CalledProcessError as e:
                    st.error(f"❌ Error: {e.stderr}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")

with tab2:
    st.header("📚 Statistics Knowledge Base")

    if 'knowledge_files' in st.session_state and st.session_state.knowledge_files:
        # Count files by type
        file_types = {}
        for kf in st.session_state.knowledge_files:
            file_type = kf.get('type', 'Unknown')
            file_types[file_type] = file_types.get(file_type, 0) + 1

        # Display summary
        type_summary = ", ".join([f"{count} {ftype}" for ftype, count in sorted(file_types.items())])
        st.success(f"✅ {len(st.session_state.knowledge_files)} knowledge files loaded ({type_summary})")

        st.subheader("Available Knowledge Sources:")

        # Group by file type
        for file_type in sorted(file_types.keys()):
            st.markdown(f"### {file_type} Files ({file_types[file_type]})")

            type_files = [kf for kf in st.session_state.knowledge_files if kf.get('type') == file_type]

            for kf in type_files:
                # Icon based on file type
                icon = {"Markdown": "📝", "Text": "📄", "JSON": "🔧"}.get(file_type, "📖")
                size_kb = kf.get('size', 0) / 1024

                with st.expander(f"{icon} {kf['filename']} ({size_kb:.1f} KB)", expanded=False):
                    # Show preview
                    preview_length = 2000 if file_type == "JSON" else 1000
                    content = kf['content']
                    if len(content) > preview_length:
                        st.markdown(content[:preview_length] + "\n\n**... (truncated)**")
                    else:
                        st.markdown(content)

                    # Show metadata
                    st.caption(f"**Type:** {file_type} | **Size:** {size_kb:.2f} KB")
                    st.caption(f"**Path:** {kf['path']}")
    else:
        st.info("📂 Load your statistics knowledge base using the sidebar configuration")

        st.markdown("""
        ### How to Set Up Your Knowledge Base

        1. **Process your statistics PDFs** using the batch processor:
           ```bash
           cd scripts/batch_pdf_processor
           python3 batch_processor.py /path/to/stats/pdfs -o ~/statistics_knowledge_base
           ```

        2. **Set the path** in the sidebar to your output directory

        3. **Load the knowledge** - The app will extract statistical methods from your processed textbooks
        """)

with tab3:
    st.header("📈 Analysis History")

    if st.session_state.analysis_history:
        for idx, analysis in enumerate(reversed(st.session_state.analysis_history)):
            with st.expander(f"Analysis #{len(st.session_state.analysis_history) - idx} - {analysis['timestamp']}", expanded=False):
                st.markdown("**Question:**")
                st.info(analysis['question'])
                st.markdown("**Results:**")
                render_visual_output(analysis['output'])
    else:
        st.info("No analysis history yet. Run some statistical analyses to see them here!")

with tab4:
    st.header("🎓 Statistical Methods for HR Compensation")

    st.markdown("""
    ## Common Statistical Techniques

    ### 1. Regression Analysis
    - **Linear Regression**: Predict salary based on continuous factors
    - **Multiple Regression**: Model salary with multiple predictors
    - **Logistic Regression**: Binary outcomes (promoted/not, left/stayed)
    - **Quantile Regression**: Salary bands at different percentiles

    ### 2. Hypothesis Testing
    - **t-tests**: Compare two groups (e.g., male vs female salaries)
    - **ANOVA**: Compare multiple groups (departments)
    - **Chi-square**: Test associations between categorical variables

    ### 3. Time Series
    - **Trend Analysis**: Identify salary growth patterns
    - **Forecasting**: Project future compensation needs
    - **ARIMA**: Model complex temporal patterns

    ### 4. Survival Analysis
    - **Kaplan-Meier**: Retention curves
    - **Cox Regression**: Factors affecting attrition timing

    ### 5. Causal Inference
    - **Propensity Scores**: Match employees for fair comparison
    - **Difference-in-Differences**: Measure policy impacts

    ### 6. Clustering & Segmentation
    - **K-means**: Group employees by compensation profile
    - **Hierarchical**: Discover natural groupings

    ## Example Scenarios

    **Scenario 1: Pay Equity Analysis**
    ```python
    # Multiple regression controlling for legitimate factors
    model = smf.ols('salary ~ experience + education + performance + department', data=df)
    # Then test for gender coefficient significance
    ```

    **Scenario 2: Retention Risk**
    ```python
    # Survival analysis for time-to-attrition
    from lifelines import KaplanMeierFitter
    kmf = KaplanMeierFitter()
    kmf.fit(df['tenure'], df['left'])
    ```

    **Scenario 3: Promotion Probability**
    ```python
    # Logistic regression
    model = smf.logit('promoted ~ performance + years_in_role + certifications', data=df)
    ```
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>📊 Statistical HR Analytics Platform</p>
    <p>Powered by Fabric AI + Extracted Statistics Knowledge</p>
    <p style='font-size: 0.8em;'>Apply rigorous statistical methods to HR compensation challenges</p>
</div>
""", unsafe_allow_html=True)
