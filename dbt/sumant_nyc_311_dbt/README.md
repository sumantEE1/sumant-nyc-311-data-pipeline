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