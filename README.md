# Space Exploration Data Analysis

A SQL project analyzing 4,324 space missions from 1957 to 2020 using the Kaggle dataset "All Space Missions from 1957" (https://www.kaggle.com/datasets/agirlcoding/all-space-missions-from-1957).

## Dataset
- Source: Kaggle, 4,324 missions, 71 agencies.
- Columns: Company Name, Location, Datum, Detail, Status Rocket, Rocket (cost), Status Mission.

## Schema
- **agencies**: agency_id, name, country.
- **missions**: mission_id, name, launch_date, agency_id, success, destination, mission_type, cost.

## Data Cleaning
- Handled missing costs in `Rocket` by converting to `NULL`.
- Mapped countries and destinations from `Location` and `Detail` using Python.
- Fixed orphaned `agency_id` values and incorrect join in Query 2 to resolve inflated mission counts.

## Queries
1. List missions with agency names (first 20, ordered by launch date).
2. Count missions by agency (top 10).
3. Calculate success rates by agency (for agencies with >10 missions).
4. Group missions by decade.

## Setup
1. Create MySQL database: `space_exploration`.
2. Run `schema.sql`.
3. Run `import_csv.py`.
4. Run `queries.sql`.

## Results
- Sample missions: First 20 missions (1957–1958) listed in [results/results_query1.csv](results/results_query1.csv).
- Top agency: RVSN USSR with 1,777 missions (Query 2, [results/results_query2.csv](results/results_query2.csv)).
- Highest success rate: Blue Origin with 100% (12/12 missions), followed by ULA with 99.29% (139/140 missions) (Query 3, [results/results_query3.csv](results/results_query3.csv)).
- Mission peaks: 1970s with 1,012 missions, followed by 1960s with 774 missions (Query 4, [results/results_query5.csv](results/results_query5.csv)).

## Challenges Overcome
- Resolved foreign key constraint error during table truncation.
- Fixed syntax error in SQL queries (missing semicolons).
- Corrected join condition in Query 2 causing inflated counts (8648 per agency).
- Handled data integrity issues with orphaned `agency_id` values.

## Future Work
- Refine destination mapping (many early missions classified as `Other`).
- Visualize trends with Python (e.g., Matplotlib for mission counts by decade).
- Analyze mission costs by agency or mission type.

## Files
- `schema.sql`: Database schema.
- `import_csv.py`: Data import script.
- `queries.sql`: Analysis queries.
- `results/*.csv`: Query outputs.
- `LICENSE`: MIT License.

## License
This project is licensed under the MIT License

## Visualization
- Bar chart of missions by decade: [results/missions_by_decade.png](results/missions_by_decade.png)