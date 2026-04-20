#!/usr/bin/env python
# coding: utf-8

# # Housing Instability: Trends, Risks, and Impacts📝
# 
# ![Banner](./assets/banner.jpeg)

# ## Topic
# *What problem are you (or your stakeholder) trying to address?*
# 📝 <!-- Answer Below -->
# A problem that I would like to explore this semester is the housing crisis/homelessness that is rampant right now in today's world. Housing insecurity includes unstable housing, overcrowding, frequent moves, and risk of eviction, while homelessness refers to people living in shelters, temporary spaces, or without shelter at all. Rising rents, stagnant wages, and limited affordable housing make this a major challenge in many U.S. cities. It affects health, employment, education, and long‑term stability. It's significant today because rent prices have increased faster than income in many regions and homelessness is rising among families, youth, and older adults.

# ## Project Question
# *What specific question are you seeking to answer with this project?*
# *This is not the same as the questions you ask to limit the scope of the project.*
# 📝 <!-- Answer Below -->
# How are rising housing costs and income trends contributing to housing insecurity and homelessness in U.S. cities today?

# ## What would an answer look like?
# *What is your hypothesized answer to your question?*
# 📝 <!-- Answer Below -->
# I expect the data to show that rising housing costs are outpacing income growth in many communities, creating a widening gap between what people earn and what they must pay for rent. As this gap grows, more households become rent‑burdened, which increases their risk of eviction, frequent moves, and ultimately homelessness.

# ## Data Sources
# *What 3 data sources have you identified for this project?*
# *How are you going to relate these datasets?*
# 📝 <!-- Answer Below -->
# 1. US Homelessness & Housing Data — Kaggle (File Download)  
# This dataset integrates HUD Point‑in‑Time homelessness counts with Census ACS indicators at the Continuum of Care (CoC) level. It allows me to directly analyze how changes in economic conditions, housing availability, and demographic factors relate to changes in homelessness over time.
# 
# 2. Rent as a Percentage of Household Income — Census API  
# This ACS table measures rent burden, one of the strongest predictors of housing instability and homelessness. I can compare rent‑burden rates across states, counties, or years, and join this dataset with my Kaggle homelessness dataset using shared geographic identifiers such as state, county FIPS, or CoC crosswalks.
# 
# 3. Zillow Observed Rent Index (ZORI) — Zillow (File Download)  
# ZORI provides monthly and annual trends in median asking rents across U.S. regions. By aligning ZORI with ACS rent‑burden indicators and HUD homelessness counts at the county or state level, I can analyze whether areas experiencing faster rent growth also show higher levels of housing insecurity and homelessness. ZORI offers a clear measure of affordability pressure, helping me examine rising rents as a key driver of housing instability.

# ## Approach and Analysis
# *What is your approach to answering your project question?*
# *How will you use the identified data to answer your project question?*
# 📝 <!-- Start Discussing the project here; you can add as many code cells as you need -->
# My approach to answering the project question is to combine homelessness counts, eviction activity, and housing‑cost indicators to understand how economic pressures contribute to housing insecurity over time. I will begin by exploring each dataset individually to understand trends in homelessness, rent burden, and eviction filings. I will also look for correlations, patterns, and trends across the 17‑year period to determine whether rising housing costs and increased eviction risk are associated with increases in homelessness. This combined approach allows me to evaluate not only the scale of homelessness but also the underlying economic and housing conditions that may be driving it.

# In[ ]:


# Start your code here

with zipfile.ZipFile("Homeless.zip", "r") as z:
    z.extractall("data")


# In[31]:


from scipy import stats
import numpy as np
import pandas as pd
import zipfile
import matplotlib.pyplot as plt
import seaborn as sns


# In[54]:


from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


# In[32]:


# Python ≥3.10 is required
import sys
assert sys.version_info >= (3, 10)

# Common imports
import numpy as np
import pandas as pd
import pandas_profiling
import os

# Scikit Learn imports
## For the pipeline
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
## For preprocessing
from sklearn.preprocessing import (
  OneHotEncoder,
  OrdinalEncoder,
  StandardScaler
)
from sklearn.impute import (
  SimpleImputer
)
## For model selection
from sklearn.model_selection import (
  StratifiedShuffleSplit,
  train_test_split,
  cross_val_score,
  KFold,
  GridSearchCV
)
# Classifier Algorithms
from sklearn import metrics
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier


# To save and load models
import pickle

# To plot pretty figures
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

mpl.rc('axes', labelsize=14)
mpl.rc('xtick', labelsize=12)
mpl.rc('ytick', labelsize=12)
plt.style.use("bmh")

# to make this notebook's output stable across runs
np.random.seed(42)


# In[33]:


df = pd.read_csv("data/Final_National_Dataset.csv")
df.head()



# In[34]:


df[['Homeless_Count', 'Poverty_Rate', 'Vacancy_Rate']].describe()


# In[40]:


df1 = pd.read_csv("data/Census.csv")
# 1. Clean column names
# -----------------------------
df1.columns = (
    df1.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
      .str.replace("(", "")
      .str.replace(")", "")
)

# -----------------------------
# 2. Remove commas and ± symbols, convert to numeric
# -----------------------------
df1['united_states!!estimate'] = (
    df1['united_states!!estimate']
      .astype(str)
      .str.replace(",", "", regex=False)
      .str.replace("±", "", regex=False)
      .str.strip()
      .astype(float)
)

df1['united_states!!margin_of_error'] = (
    df1['united_states!!margin_of_error']
      .astype(str)
      .str.replace(",", "", regex=False)
      .str.replace("±", "", regex=False)
      .str.strip()
      .astype(float)
)

# -----------------------------
# 3. Remove rows you don't want
# -----------------------------
rows_to_drop = ["Total:", "Not computed"]
df1 = df1[~df1['label_grouping'].isin(rows_to_drop)]

# -----------------------------
# 4. Optional: Clean category labels
# -----------------------------
df1['label_grouping'] = df1['label_grouping'].str.strip()

# -----------------------------
# 5. Reset index
# -----------------------------
df1 = df1.reset_index(drop=True)

df1.head()


# In[41]:


df2 = pd.read_csv("data/Zillow.csv")
 #Drop the national aggregate row
# -----------------------------
df2 = df2[df2['RegionName'] != 'United States'].reset_index(drop=True)

# -----------------------------
# 3. Identify date columns
# -----------------------------
date_cols = [col for col in df2.columns if col[:4].isdigit()]

# -----------------------------
# 4. Melt wide → long format
# -----------------------------
df2_long = df2.melt(
    id_vars=['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName'],
    value_vars=date_cols,
    var_name='Date',
    value_name='Price'
)

# -----------------------------
# 5. Convert Date column to datetime
# -----------------------------
df2_long['Date'] = pd.to_datetime(df2_long['Date'])

# -----------------------------
# 6. Optional: Filter to only MSAs
# -----------------------------
df2_long = df2_long[df2_long['RegionType'] == 'msa'].reset_index(drop=True)

# -----------------------------
# 7. Final cleaned dataset
# -----------------------------
df2_long.head()


# To prepare the datasets for analysis, I completed a structured cleaning process that ensured consistency, accuracy, and analytical readiness across three very different data sources. The Zillow rent dataset required the most transformation: I removed the national aggregate row to avoid skewing regional comparisons, identified all monthly date columns, and reshaped the data from a wide format into a long, tidy structure where each row represented a single region‑month observation. I then converted the date strings into proper datetime objects and filtered the dataset to include only metropolitan areas, since the analysis focuses on urban housing markets. The Census rent‑burden dataset needed formatting corrections, including standardizing column names, removing commas and special characters from numeric fields, and excluding non‑analytic rows such as “Total” and “Not computed.” I also cleaned and standardized the category labels to ensure they could be used reliably in visualizations. The national homelessness dataset was already well‑structured, but I validated it by checking for missing values, confirming that numeric and categorical fields were correctly typed, verifying that no duplicate CoC‑year combinations existed, and ensuring that key variables such as poverty rate and vacancy rate fell within realistic ranges. Together, these steps produced three clean, consistent, and analysis‑ready datasets that could be visualized, compared, and interpreted with confidence.

# In[42]:


cities = ["Cincinnati, OH", "New York, NY", "Los Angeles, CA"]
df_plot = df_long[df_long['RegionName'].isin(cities)]

plt.figure(figsize=(12,6))
for city in cities:
    subset = df_plot[df_plot['RegionName'] == city]
    plt.plot(subset['Date'], subset['Price'], label=city)

plt.title("Zillow Observed Rent Index Over Time")
plt.xlabel("Year")
plt.ylabel("Rent Price (ZORI)")
plt.legend()
plt.grid(True)
plt.show()


# This visualization shows how rent prices have steadily increased over time in three major U.S. cities, Cincinnati, New York, and Los Angeles using the Zillow Observed Rent Index (ZORI). Although each city starts at a different price level, all three lines move upward year after year, demonstrating a consistent rise in rental costs. The sharp jump around 2021 is especially notable, reflecting pandemic‑era pressures such as limited housing supply, increased demand, and inflation. New York remains the most expensive market throughout the entire period, followed by Los Angeles, while Cincinnati stays lower but still experiences meaningful growth. Overall, the chart illustrates that rising rents are a widespread, long‑term trend across diverse regions, reinforcing the idea that housing costs are climbing faster than many households can keep up with.

# In[51]:


plt.figure(figsize=(8,6))
sns.regplot(
    data=df,
    x='Rent_Burden_Rate',
    y='Homeless_Count',
    scatter_kws={'alpha':0.2, 's':10},
    line_kws={'color':'red'}
)
plt.title("Rent Burden vs Homelessness with Trendline")
plt.show()





# This visualization shows a clear, positive relationship between rent burden and homelessness. Each point represents a community, plotting its rent‑burden rate on the x‑axis and its homeless count on the y‑axis. Even though the points vary widely, the red trendline cuts through the noise and reveals the underlying pattern: as rent burden increases, homelessness tends to rise as well. Communities where a larger share of households spend an excessive portion of their income on rent are more likely to have higher levels of homelessness. The clustering of points at lower rent‑burden rates with lower homelessness, contrasted with the upward pull of points at higher rent‑burden rates, reinforces the idea that housing affordability pressures directly contribute to housing instability.

# In[50]:


plt.figure(figsize=(8,6))
sns.regplot(
    data=df,
    x='Vacancy_Rate',
    y='Homeless_Count',
    scatter_kws={'alpha':0.2, 's':10, 'color':'orange'},
    line_kws={'color':'red'}
)
plt.title("Vacancy Rate vs Homelessness with Trendline")
plt.show()



# This visualization illustrates how vacancy rates relate to homelessness across communities, and the trendline helps reveal the underlying pattern that individual points alone might obscure. Each dot represents a community’s vacancy rate on the x‑axis and its homeless count on the y‑axis. While the points are scattered widely, the red trendline slopes slightly downward, indicating a negative relationship: communities with lower vacancy rates—meaning tighter, more competitive housing markets—tend to have higher levels of homelessness. In contrast, places with somewhat higher vacancy rates generally show lower homeless counts. This pattern aligns with housing‑market research showing that when available units are scarce, rents rise faster, mobility becomes harder, and people facing financial strain have fewer options to relocate or stabilize their housing. Overall, the visualization reinforces the idea that tight housing supply is a structural risk factor that contributes to homelessness, especially when combined with rising rents and high rent‑burden rates.

# In[49]:


plt.figure(figsize=(10,6))
plt.hist(df['Poverty_Rate'], bins=30, color='#4C72B0', alpha=0.8)
plt.title("Distribution of Poverty Rates Across CoCs")
plt.xlabel("Poverty Rate (%)")
plt.ylabel("Number of CoCs")
plt.grid(axis='y', alpha=0.3)
plt.show()



# This histogram shows how poverty is distributed across Continuums of Care (CoCs), and the pattern is surprisingly concentrated. Most CoCs fall within a relatively narrow band of poverty rates—roughly between 10% and 20%—with the highest concentration around 13%. That tall central bar tells you that a large share of communities experience similar levels of poverty, rather than poverty being spread evenly or randomly across the country. As the bars move toward higher poverty rates, the number of CoCs drops off, meaning far fewer communities experience extremely high poverty. (might change this visual later on)

# 1.Machine Learning
# 
# I am doing a classification model to predict whether a community has a high unsheltered homelessness rate. 
# 
# Anticipated Challenges
# 1. Mixed Data Types
# The dataset contains both numeric features (e.g., Poverty_Rate, Vacancy_Rate, Rent_Burden_50_Plus) and categorical features (e.g., CoC_Code, State, Area_Name).
# Models cannot directly handle this mixture without preprocessing.
# 
# 2. Missing Values
# Some socioeconomic indicators include missing or margin‑of‑error values that must be handled consistently.
# 
# 3. Feature Scaling
# Many models (Logistic Regression, SVM, KNN) require standardized numeric features to perform correctly.
# 
# How I Plan to Address These Challenges
# 1. Use a ColumnTransformer for Proper Preprocessing
# I will build a preprocessing pipeline that:
# 
# -Imputes missing numeric values using median imputation
# 
# -Imputes missing categorical values using most frequent
# 
# -Scales numeric features using StandardScaler
# 
# -One‑hot encodes categorical variables
# 
# This ensures all models receive clean, consistent input.
# 
# 2. Remove Leakage‑Prone Features
# To avoid data leakage, I will exclude Unsheltered_Rate (the source of the target) from the feature set.
# 
# 3. Use Stratified Train/Test Split
# I will use stratify=y to preserve class balance in both training and testing sets.

# ### Ask

# In[46]:


print("DF columns:", df.columns.tolist())
print("DF1 columns:", df1.columns.tolist())
print("DF2 columns:", df2.columns.tolist())


# In[48]:


df = pd.read_csv("data/Final_National_Dataset.csv")
df1 = pd.read_csv("data/Census.csv")
df2 = pd.read_csv("data/Zillow.csv")


# In[47]:


df = pd.read_csv("data/Final_National_Dataset.csv")
df.columns.tolist()


# ### Prepare

# In[60]:


# Create unsheltered rate (severity indicator)
df['Unsheltered_Rate'] = df['Unsheltered_Count'] / df['Homeless_Count']

# Handle divide-by-zero cases (if any CoCs have Homeless_Count = 0)
df['Unsheltered_Rate'] = df['Unsheltered_Rate'].replace([np.inf, -np.inf], np.nan)
df['Unsheltered_Rate'] = df['Unsheltered_Rate'].fillna(0)

# Create binary classification label
median_unsheltered = df['Unsheltered_Rate'].median()
df['High_Unsheltered'] = (df['Unsheltered_Rate'] > median_unsheltered).astype(int)

# Define X and y
X = df.drop(columns=['High_Unsheltered', 'Unsheltered_Rate'])
y = df['High_Unsheltered']


# ### Process

# In[61]:


# TRAIN/TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# PREPROCESSING
numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns
categorical_cols = X.select_dtypes(include=['object']).columns

numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer([
    ('num', numeric_pipeline, numeric_cols),
    ('cat', categorical_pipeline, categorical_cols)
])

# MODELS
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight='balanced'),
    "Random Forest": RandomForestClassifier(class_weight='balanced'),
    "Gradient Boosting": GradientBoostingClassifier(),
    "KNN": KNeighborsClassifier(),
    "SVM": SVC(class_weight='balanced', probability=True)
}

# TRAIN + EVALUATE
results = []

for name, model in models.items():
    clf = Pipeline([
        ('preprocessor', preprocessor),
        ('model', model)
    ])

    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:,1] if hasattr(clf, "predict_proba") else None

    results.append([
        name,
        accuracy_score(y_test, y_pred),
        precision_score(y_test, y_pred),
        recall_score(y_test, y_pred),
        f1_score(y_test, y_pred),
        roc_auc_score(y_test, y_prob) if y_prob is not None else None
    ])

results_df = pd.DataFrame(results, columns=[
    "Model", "Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"
])

print(results_df.sort_values(by="F1 Score", ascending=False))



# ### Analyze

# In[62]:


# Fit your best model again
best_model = Pipeline([
    ('preprocessor', preprocessor),
    ('model', GradientBoostingClassifier())
])

best_model.fit(X_train, y_train)
y_pred = best_model.predict(X_test)

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Low Unsheltered', 'High Unsheltered'],
            yticklabels=['Low Unsheltered', 'High Unsheltered'])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix — High vs Low Unsheltered Rate")
plt.show()


# In[63]:


from sklearn.metrics import roc_curve, auc


# Predicted probabilities
y_prob = best_model.predict_proba(X_test)[:, 1]

# ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(7, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2,
         label=f'ROC curve (AUC = {roc_auc:.3f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve — High vs Low Unsheltered Rate')
plt.legend(loc="lower right")
plt.show()


# In[64]:


import numpy as np

# Fit model again to extract feature importances
best_model.fit(X_train, y_train)

model = best_model.named_steps['model']

# Extract feature names after preprocessing
encoded_features = best_model.named_steps['preprocessor'] \
    .transformers_[1][1].named_steps['encoder'] \
    .get_feature_names_out(categorical_cols)

numeric_features = numeric_cols  # now WITHOUT Unsheltered_Rate

all_features = np.concatenate([numeric_features, encoded_features])

importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 12))
plt.title("Top 20 Feature Importances — High vs Low Unsheltered Rate")
plt.barh(all_features[indices][:20][::-1], importances[indices][:20][::-1])
plt.xlabel("Importance Score")
plt.ylabel("Feature")
plt.show()


# To understand which factors most strongly predict whether a community experiences a high unsheltered homelessness rate, I implemented a set of supervised machine learning classification models. Each model was trained on the same preprocessed dataset and evaluated using a consistent set of performance metrics on the test set.
# 
# Models Implemented
# I trained and compared the following algorithms:
# 
# Logistic Regression (baseline linear classifier)
# 
# Random Forest Classifier (ensemble of decision trees)
# 
# Gradient Boosting Classifier (sequential boosting model)
# 
# Support Vector Machine (SVM) with probability estimates
# 
# K‑Nearest Neighbors (KNN)
# 
# These models were chosen to represent a mix of linear, nonlinear, ensemble, and distance‑based approaches, allowing for a comprehensive comparison of predictive performance.
# 
# Evaluation Metrics
# Because this is a binary classification problem, and because class balance is important, I evaluated each model using:
# 
# Accuracy – overall correctness
# 
# Precision – how often predicted “high unsheltered” cases were correct
# 
# Recall – how well the model identified actual high‑unsheltered communities
# 
# F1 Score – harmonic mean of precision and recall
# 
# ROC‑AUC – ability to separate the two classes across thresholds
# 
# These metrics were computed using predictions on the held‑out test set, ensuring an unbiased estimate of model performance.
# 
# Model Comparison
# After training, I compared all models based on their test‑set performance. Ensemble models — particularly Gradient Boosting and Random Forest — consistently outperformed the others. These models captured nonlinear relationships between socioeconomic factors (such as poverty rate, rent burden, and vacancy rate) and unsheltered homelessness severity.
# 
# Logistic Regression performed reasonably well but was limited by its linear decision boundary. SVM and KNN showed moderate performance, with KNN being the least effective due to sensitivity to feature scaling and high‑dimensional encoded data.
# 
# Key Findings
# Gradient Boosting emerged as the strongest model overall, achieving the highest F1 score and ROC‑AUC.
# 
# Random Forest performed similarly well, confirming that tree‑based ensemble methods are well‑suited for this dataset.
# 
# Models with linear assumptions (Logistic Regression) or distance‑based logic (KNN) were less effective at capturing the complex relationships in the data.
# 
# The ROC curves for the top models showed strong class separation, indicating reliable predictive power.
# 
# Confusion matrix analysis revealed that the best models maintained high recall for the “high unsheltered rate” class — an important outcome for identifying communities with the greatest need.
# 
# Conclusion
# By comparing multiple algorithms and evaluating them with robust classification metrics, I identified Gradient Boosting as the most effective model for predicting high unsheltered homelessness rates. This model will be used in the next stage of the project to interpret feature importance and understand which socioeconomic and housing factors contribute most strongly to severe homelessness conditions.

# ## Resources and References
# *What resources and references have you used for this project?*
# 📝 <!-- Answer Below -->
# I used kaggle and Census API datasets

# In[ ]:


# ⚠️ Make sure you run this cell at the end of your notebook before every submission!
get_ipython().system('jupyter nbconvert --to python source.ipynb')

