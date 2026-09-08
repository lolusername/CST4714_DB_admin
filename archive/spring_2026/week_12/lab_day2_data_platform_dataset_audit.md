# Week 12 Lab Day 2
## Data Platform and Dataset Audit

## Purpose
Today you will learn how to find, evaluate, and prepare a real dataset before putting it into a database.

The goal is not to build a full app today.
The goal is to practice thinking like a database administrator:
- Where did this data come from?
- Can I trust it?
- What format is it in?
- What does each row or document represent?
- Would it fit better in MongoDB Atlas, Postgres/Supabase, or both?
- What would I need to do before uploading it?

## Individual Work Only
This lab is individual.
There is no group work.

## Dataset Platforms Introduced Today

Choose one platform or source to analyze:

- [Kaggle Datasets](https://www.kaggle.com/datasets)
- [NYC Open Data](https://opendata.cityofnewyork.us/)
- [Socrata Open Data API documentation](https://dev.socrata.com/docs/endpoints.html)
- [scikit-learn dataset loading utilities](https://sklearn.org/stable/datasets.html)
- [UCI Machine Learning Repository](https://archive.ics.uci.edu/)
- [CISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [CISA KEV data files on GitHub](https://github.com/cisagov/kev-data)
- [GitHub Advisory Database](https://github.com/advisories)
- a public GitHub repository with CSV, JSON, or small structured data files

## Optional Class Notebook
If the instructor uses the live notebook demo, open it here:

[Week 12 Atlas + Supabase Dataset Demo](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_12/week12_atlas_supabase_dataset_demo.ipynb)

The notebook uses the local Week 12 sample file:

`sample_cisa_kev_vulnerabilities.csv`

## Security Dataset Warning
For this class, choose security datasets that are metadata, logs, advisories, vulnerabilities, or safely documented examples.

Do not download malware samples, exploit code, credential dumps, leaked data, or anything that looks like it could harm your computer or violate privacy.

## Good Beginner Dataset Targets

If you do not know where to start, look for one of these:

- Week 12 sample CSV: `sample_cisa_kev_vulnerabilities.csv`
- Kaggle: a small CSV about movies, sports, products, schools, books, music, games, or public health
- NYC Open Data: 311 service requests, restaurant inspections, building permits, parks, school, or transportation datasets
- scikit-learn: Iris, Digits, Diabetes, Breast Cancer, Wine, or another built-in teaching dataset
- UCI: Iris, Wine Quality, Heart Disease, Bank Marketing, Adult, or another dataset with a clear description
- Security: CISA KEV CSV/JSON files or GitHub Advisory Database records
- GitHub: a repository that clearly provides CSV or JSON files plus a README and license

## What To Do

### 1. Choose a Dataset
Pick one dataset that you can understand well enough to explain.

Good beginner choices have:
- a clear title
- a visible owner or publisher
- a clear file format such as CSV or JSON
- understandable columns or fields
- enough rows to be interesting but not so many that the file becomes hard to handle
- a license, terms of use, or source explanation

### 2. Analyze the Platform
Answer:

1. What platform or source did you use?
2. What kind of data does this platform usually host?
3. Who publishes or maintains the dataset you chose?
4. What signs make the dataset seem trustworthy or untrustworthy?
5. What would you need to check before using this data in a real project?

### 3. Analyze the Dataset
Answer:

1. What is the dataset about?
2. What format is it in: CSV, JSON, Excel, image files, text files, API response, or something else?
3. What does one row, record, or document represent?
4. Name 5-8 important fields or columns.
5. What field looks like a possible identifier?
6. What field might need cleaning, type conversion, or standardization?
7. What is one question this dataset could help answer?

### 4. Choose a Database Fit
Choose one:

- MongoDB Atlas
- Postgres/Supabase
- both

Explain your choice in 4-6 sentences.

Use this basic rule:
- choose Postgres/Supabase when the data is tabular, relational, and benefits from constraints or joins
- choose MongoDB Atlas when the data is document-shaped, nested, flexible, log-like, or changes shape across records
- choose both only if there is a simple reason to split structured core records from flexible documents or events

### 5. Upload Plan for MongoDB Atlas
If this dataset were going into MongoDB Atlas, explain the upload plan.

Useful references:
- [MongoDB Atlas `mongoimport`](https://www.mongodb.com/docs/atlas/import/mongoimport/)
- [MongoDB Compass import/export](https://www.mongodb.com/docs/compass/import-export/)

For a CSV file:

```bash
mongoimport \
  --uri "$MONGODB_URI" \
  --db datasets_lab \
  --collection your_collection_name \
  --type csv \
  --headerline \
  --file your_file.csv
```

For a JSON file:

```bash
mongoimport \
  --uri "$MONGODB_URI" \
  --db datasets_lab \
  --collection your_collection_name \
  --file your_file.json
```

You can also use MongoDB Compass to import JSON or CSV into a collection.

In your response, name:
- database name
- collection name
- whether the source file is CSV or JSON
- one field that should become an index later
- one field whose type you would check carefully

Do not submit your connection string or password.

### 6. Upload Plan for Postgres/Supabase
If this dataset were going into Postgres/Supabase, explain the upload plan.

Useful references:
- [Import data into Supabase](https://supabase.com/docs/guides/database/import-data)
- [PostgreSQL COPY](https://www.postgresql.org/docs/current/sql-copy.html)

For a small CSV file, Supabase can import CSV through the dashboard Table Editor.
For a larger or more controlled import, Postgres uses `COPY` or `\copy`.

Example table sketch:

```sql
create table dataset_records (
  id bigserial primary key,
  source_id text,
  title text,
  category text,
  created_at timestamptz
);
```

Example `\copy` pattern:

```sql
\copy dataset_records(source_id, title, category, created_at)
from 'your_file.csv'
with (format csv, header true);
```

In your response, name:
- table name
- 5-8 likely columns
- likely primary key
- one column that should be indexed later
- one data type you would need to choose carefully

## In-Class Checkpoint
Submit one Brightspace text response.

Include:

1. dataset link
2. platform/source name
3. dataset summary
4. platform analysis answers
5. dataset analysis answers
6. database fit explanation
7. MongoDB Atlas upload plan
8. Postgres/Supabase upload plan

You do not need to upload the full dataset today unless the instructor explicitly tells you to.

## Success Standard
You are successful if you can explain where a dataset came from, what shape it has, whether it fits MongoDB or Postgres better, and what the first safe upload steps would be.
