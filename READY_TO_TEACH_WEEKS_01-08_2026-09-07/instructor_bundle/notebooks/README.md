# Educational Notebooks

Download a notebook below, open [Google Colab](https://colab.research.google.com/),
and choose **File > Upload notebook**. This works without publishing this repository.
Run cells in order and read the Markdown between them. Never save a database
password in a cell or share outputs containing credentials.

| Notebook | Used for | Environment |
|---|---|---|
| [01: Relational and SQL review](01_relational_sql_review.ipynb) | Week 2 queries and relational operations | DuckDB, no cloud account |
| [02: Transactions and locks](02_postgres_transactions_locks.ipynb) | Week 5 competing writers | PostgreSQL connection; explicitly labeled static fallback |
| [03: Backup and restore](03_postgres_backup_restore.ipynb) | Week 8 real archive and separate restore | Disposable local PostgreSQL in the notebook runtime |

Use the corresponding lab for what to change and submit. Notebook 03's final
cell removes its own temporary databases and files. Local tests and a Linux
setup test do not guarantee a particular hosted Colab runtime or account.
