Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices

Run for snoflake injection in plugin list
```pipx inject dbt-core dbt-snowflake```

The file of token is exact path in profile.yml
The key is `private_key_path`
The account is orgname-account name in profile.yml
Added optional format 2nd argument "'YYYY-MM-DD HH24:MI:SS TZD'" for cast try_to_timestamp
Added INITCAP(TRIM(PARK_BOROUGH)) to standardise it
The updated column name is updated to snake case but it will appear in upper case in snoflake
In dbt, the file name of a model’s SQL file acts as the default name for the model and the resulting database relation (table or view)
The query to view model was 
    ```SELECT community_board,created_date,closed_date,due_date,resolution_action_updated_date,park_borough FROM SUMANT_DEY_RAW_staging.stg_311_service_requests```
    filename as model name and schema suffix from dbt_project.yml was created

Raws dbt seed table with schema name and model (file name) SUMANT_DEY_RAW.ticket_6_311

Cast to string stg_311_service_requests_incremental to resolve try to timestamp sql compilation error (It was a may be fix suggested by Claude)The table was created manually for ticket 6. It is a copy paste

```
 cat 311_service_requests_000000000049 | grep "Open" | tail -n 5 >> Open_requests.csv
```

The dbt was run with no incremental_strategy hence it was merge and status column was updated

Added seed yml in seed folder with column data types defined because of snowflake convert data type to integer automatically when all the row column is null


SQL Query returns two rows 
```
select * from SUMANT_DEY_RAW_staging.raw_311_service_requests_incremental where unique_key = 20406875
```

SQL Query returned 1 row
```
select * from SUMANT_DEY_RAW_CURATED.curated_311_service_requests_incremental where unique_key = 20406875
```

To avoid multiple row update the increment strategy (updated created_date to year 2026 )

Added unique query in dim 311 complaint sqlto generate unique surrogate/primary key bt generating unique key using unique complaint type and description