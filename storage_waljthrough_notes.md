This video provides a walkthrough of various storage formats used in data engineering, emphasizing how they impact storage efficiency and query performance.

### Overview of Storage Formats

Storage formats are categorized into three primary buckets:

1.  **Row-based Formats (e.g., CSV, JSON, Avro):**
      * Store entire records together on disk.
      * Optimized for data ingestion and moving data between services.
      * CSV is ideal for quick exports, while JSON is better for nested or flexible data.
2.  **Columnar Formats (e.g., Parquet, ORC):**
      * Store each column separately, which is optimized for read-heavy analytical queries.
      * Allows engines to read only required columns rather than scanning entire records, significantly improving performance.
3.  **Table Formats (e.g., Delta Lake, Iceberg):**
      * Frameworks built on top of columnar formats that add layers for ACID transactions, rollback/commit features, and schema evolution.
      * Highly suitable for lakehouse architectures.

### Deep Dive: Parquet

Parquet is a widely used columnar format that incorporates specific techniques to optimize storage and retrieval.

  * **Compression and Encoding:**
      * Parquet uses **dictionary encoding** (mapping values to smaller codes) and **run-length encoding** (storing consecutive values by frequency) to significantly reduce storage size.
      * These techniques are followed by compression algorithms such as Snappy (the default), Gzip, or Zstandard.
      * Compared to CSV, Parquet can reduce file size by approximately eight to nine times.
  * **Predicate Pushdown:**
      * This technique improves scanning speed by grouping data into chunks with associated min/max statistics.
      * Query engines use these statistics to skip irrelevant data chunks entirely, which is most efficient when data is sorted.

Parquet is not human-readable and is intended for machine processing; however, most big data tools (e.g., Spark, Athena, Presto) provide native support for reading it. The fundamental rule for selection is: use row-based formats for moving data and columnar formats for analyzing it.
