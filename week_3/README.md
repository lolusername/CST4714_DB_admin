# Week 3: PostgreSQL Architecture and Cloud Database Management

## Learning Objectives

By the end of this week, students will be able to:
- Understand PostgreSQL database architecture and components
- Explain the role of database administrators in cloud environments
- Design and implement database schemas using PostgreSQL
- Write and execute complex SQL queries
- Manage database objects (tables, indexes, constraints)
- Understand database backup and recovery concepts

## Topics Covered

### 1. PostgreSQL Architecture
- **Presentation**: `Postgres_architecture.pptx`
- Database server components
- Process architecture
- Memory management
- Storage systems
- Connection handling

### 2. Cloud Database Solutions
- **Presentation**: `Cloud.pptx`
- Cloud database services overview
- Database as a Service (DBaaS)
- Scalability and performance considerations
- Security in cloud environments
- Cost optimization strategies

### 3. Database Design and Schema Management
- Entity-Relationship modeling
- Normalization principles
- Table design and relationships
- Data types and constraints
- Indexing strategies

### 4. SQL Fundamentals and Advanced Queries
- **Practice Database**: `review.sql`
- Database schema includes:
  - `bookings` table (facility bookings)
  - `facilities` table (recreation facilities)
  - `members` table (club members)
- Query optimization techniques
- Joins and subqueries
- Aggregation functions
- Data manipulation operations

## Materials

### Presentations
- `Postgres_architecture.pptx` - PostgreSQL architecture overview
- `Cloud.pptx` - Cloud database management concepts

### Hands-on Practice
- `review.sql` - Complete database dump with sample data for practice
  - Contains a country club database with bookings, facilities, and members
  - Includes sample data for realistic query practice
  - Suitable for learning joins, aggregations, and complex queries

## Activities

### Lab Exercise 1: PostgreSQL Installation and Setup
1. Install PostgreSQL on your local machine
2. Create a new database
3. Import the `review.sql` file
4. Verify the database structure

**Alternative Setup for Supabase Users:**
1. Create a new Supabase project
2. Open the SQL Editor in Supabase
3. Run the `review.sql` file to create the database schema
4. Verify the tables and data are created correctly

### Lab Exercise 2: Database Schema Analysis
1. Examine the three main tables in the review database
2. Identify relationships between tables
3. Document the schema design
4. Suggest potential improvements

### Lab Exercise 3: Query Practice
1. Write queries to answer business questions about the country club
2. Practice different types of joins
3. Use aggregation functions effectively
4. Optimize query performance

### Lab Exercise 4: PostgreSQL Exercises on Supabase
- **Platform**: [pgexercises.com](https://pgexercises.com/gettingstarted.html)
- **Environment**: Supabase SQL Editor
- **Setup**: First, run the `review.sql` file in Supabase SQL Editor to create the database schema
- Complete the PostgreSQL exercises using the Supabase SQL editor
- Practice with the country club database schema provided by pgexercises
- Focus on:
  - Basic SELECT queries
  - JOINs and relationships
  - Aggregation and grouping
  - Subqueries and advanced techniques

## Assignments

### Assignment 1: Architecture Analysis
- Analyze the PostgreSQL architecture presentation
- Compare with other database systems
- Submit a 2-page analysis of key architectural components

### Assignment 2: Cloud Database Research
- Research different cloud database providers
- Compare features, pricing, and use cases
- Create a comparison matrix

### Assignment 3: SQL Query Challenge
- Complete 10 complex queries using the review database
- Include queries with joins, subqueries, and aggregations
- Document your approach and results

## Resources

### Documentation
- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)

### Practice Exercises
- **[pgexercises.com](https://pgexercises.com/gettingstarted.html)** - Interactive PostgreSQL exercises
  - Use Supabase SQL Editor to complete exercises
  - Practice with country club database schema
  - Progressive difficulty levels

### Cloud Database Services
- AWS RDS
- Google Cloud SQL
- Azure Database for PostgreSQL
- Heroku Postgres
- **Supabase** (for pgexercises practice)

### Tools
- pgAdmin (PostgreSQL administration tool)
- DBeaver (Universal database tool)
- psql (command-line interface)
- **Supabase SQL Editor** (for pgexercises)

## Assessment

- **Participation**: 20% (lab exercises and discussions)
- **Assignments**: 40% (three assignments as listed above)
- **Final Project**: 40% (database design and implementation project)

---

*Note: The review.sql file contains a complete database dump from PostgreSQL version 9.2.0. While this is an older version, the concepts and SQL syntax remain relevant for learning purposes.*
