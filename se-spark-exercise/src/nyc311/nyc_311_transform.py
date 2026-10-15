from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,StringType, IntegerType, TimestampNTZType, ArrayType
from pyspark.sql import functions as F
from pyspark.sql.functions import udf, col



SLA_HOURS = 72
spark = SparkSession.builder.appName("DECrossSkiling").master("local[4]").config("spark.driver.memory", "4g").getOrCreate()

schema = StructType([
    StructField("Unique Key", IntegerType(), nullable=False),
    StructField("Created Date", TimestampNTZType(), nullable=True),
    StructField("Closed Date", TimestampNTZType(), nullable=True),
    StructField("Agency", StringType(), nullable=True),
    StructField("Agency Name", StringType(), nullable=True),
    StructField("Complaint Type", StringType(), nullable=True),
    StructField("Descriptor", StringType(), nullable=True),
    StructField("Location Type", StringType(), nullable=True),
    StructField("Incident Zip", StringType(), nullable=True),
    StructField("Incident Address", StringType(), nullable=True),
    StructField("Street Name", StringType(), nullable=True),
    StructField("Cross Street 1", StringType(), nullable=True),
    StructField("Cross Street 2", StringType(), nullable=True),
    StructField("Intersection Street 1", StringType(), nullable=True),
    StructField("Intersection Street 2", StringType(), nullable=True),
    StructField("Address Type", StringType(), nullable=True),
    StructField("City", StringType(), nullable=True),
    StructField("Landmark", StringType(), nullable=True),
    StructField("Facility Type", StringType(), nullable=True),
    StructField("Status", StringType(), nullable=True),
    StructField("Due Date", StringType(), nullable=True),
    StructField("Resolution Description", StringType(), nullable=True),
    StructField("Resolution Action Updated Date", StringType(), nullable=True),
    StructField("Community Board", StringType(), nullable=True),
    StructField("BBL", StringType(), nullable=True),
    StructField("Borough", StringType(), nullable=True),
    StructField("X Coordinate (State Plane)", StringType(), nullable=True),
    StructField("Y Coordinate (State Plane)", StringType(), nullable=True),
    StructField("Open Data Channel Type", StringType(), nullable=True),
    StructField("Park Facility Name", StringType(), nullable=True),
    StructField("Park Borough", StringType(), nullable=True),
    StructField("Vehicle Type", StringType(), nullable=True),
    StructField("Taxi Company Borough", StringType(), nullable=True),
    StructField("Taxi Pick Up Location", StringType(), nullable=True),
    StructField("Bridge Highway Name", StringType(), nullable=True),
    StructField("Bridge Highway Direction", StringType(), nullable=True),
    StructField("Road Ramp", StringType(), nullable=True),
    StructField("Bridge Highway Segment", StringType(), nullable=True),
    StructField("Latitude", StringType(), nullable=True),
    StructField("Longitude", StringType(), nullable=True),
    StructField("Location", StringType(), nullable=True),
    StructField("Zip Codes", StringType(), nullable=True),
    StructField("Community Districts", StringType(), nullable=True),
    StructField("Borough Boundaries", StringType(), nullable=True),
    StructField("City Council Districts", StringType(), nullable=True),
    StructField("Police Precincts", StringType(), nullable=True)

])

service_requests_df_json = (spark.read
                            .schema(schema)
                           .json("/Users/sumant/workspace/learning/DE_Practise/sumant-nyc-311-data-pipeline/se-spark-exercise/data/archive/socrata_metadata_311-service-requests-from-2010-to-present.json"))

service_requests_df_csv = (spark.read
                            .schema(schema)
                           .csv("/Users/sumant/workspace/learning/DE_Practise/sumant-nyc-311-data-pipeline/se-spark-exercise/data/archive/311-service-requests-from-2010-to-present.csv"))

service_requests_df_parquet = (spark.read
                            .schema(schema)
                           .parquet("/Users/sumant/workspace/learning/DE_Practise/sumant-nyc-311-data-pipeline/se-spark-exercise/data/archive/311-service-requests-from-2010-to-present.parquet/"))

service_requests_df_text = (spark.read
                            # .schema(schema)
                            .text("/Users/sumant/workspace/learning/DE_Practise/sumant-nyc-311-data-pipeline/se-spark-exercise/data/archive/311_sample_json.txt"))

combined = service_requests_df_parquet.unionByName(service_requests_df_csv, allowMissingColumns=True)
combined_text = combined.unionByName(service_requests_df_text, allowMissingColumns=True)
combined_df = combined_text.unionByName(service_requests_df_json, allowMissingColumns=True)


combined_df_ren = (combined_df
                              .withColumnRenamed("Unique Key", "unique_key")
                              .withColumnRenamed("Created Date", "created_date")
                              .withColumnRenamed("Closed Date", "closed_date")
                              .withColumnRenamed("Complaint Type", "complaint_type")
                              .withColumnRenamed("Borough", "borough")
                              .withColumnRenamed("Agency", "agency")
                              .withColumnRenamed("Agency Name", "agency_name")
                              .withColumnRenamed("Status", "status")
                              .withColumnRenamed("Descriptor", "descriptor")
                              .withColumnRenamed("Location Type", "location_type")
                              .withColumnRenamed("Incident Zip", "incident_zip")
                              .withColumnRenamed("Incident Address", "incident_address")
                              .withColumnRenamed("Street Name", "street_name")
                              .withColumnRenamed("Cross Street 1", "cross_street_1")
                              .withColumnRenamed("Cross Street 2", "cross_street_2")
                              .withColumnRenamed("Intersection Street 1", "intersection_street_1")
                              .withColumnRenamed("Intersection Street 2", "intersection_street_2")
                              .withColumnRenamed("Address Type", "address_type")
                              .withColumnRenamed("City", "city")
                              .withColumnRenamed("Landmark", "landmark")
                              .withColumnRenamed("Facility Type", "facility_type")
                              .withColumnRenamed("Due Date", "due_date")
                              .withColumnRenamed("Resolution Description", "resolution_description")
                              .withColumnRenamed("Resolution Action Updated Date", "resolution_action_updated_date")
                              .withColumnRenamed("Community Board", "community_board")
                              .withColumnRenamed("BBL", "bbl")
                              .withColumnRenamed("X Coordinate (State Plane)", "x_coordinate_state_plane")
                              .withColumnRenamed("Y Coordinate (State Plane)", "y_coordinate_state_plane")
                              .withColumnRenamed("Open Data Channel Type", "open_data_channel_type")
                              .withColumnRenamed("Park Facility Name", "park_facility_name")
                              .withColumnRenamed("Park Borough", "park_borough")
                              .withColumnRenamed("Vehicle Type", "vehicle_type")
                              .withColumnRenamed("Taxi Company Borough", "taxi_company_borough")
                              .withColumnRenamed("Taxi Pick Up Location", "taxi_pick_up_location")
                              .withColumnRenamed("Bridge Highway Name", "bridge_highway_name")
                              .withColumnRenamed("Bridge Highway Direction", "bridge_highway_direction")
                              .withColumnRenamed("Road Ramp", "road_ramp")
                              .withColumnRenamed("Bridge Highway Segment", "bridge_highway_segment")
                              .withColumnRenamed("Latitude", "latitude")
                              .withColumnRenamed("Longitude", "longitude")
                              .withColumnRenamed("Location", "location")
                              .withColumnRenamed("Zip Codes", "zip_codes")
                              .withColumnRenamed("Community Districts", "community_districts")
                              .withColumnRenamed("Borough Boundaries", "borough_boundaries")
                              .withColumnRenamed("City Council Districts", "city_council_districts")
                              .withColumnRenamed("Police Precincts", "police_precincts")
                              )



null_count_threshold = 80  # percent
total_row = combined_df_ren.count()

# One aggregate per column: number of nulls
null_counts = combined_df_ren.select([
    F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(c)
    for c in combined_df_ren.columns
])

# Convert the single result row to a dict, then compute null percentages
null_row = null_counts.first().asDict()
null_pct = {c: (n / total_row) * 100 for c, n in null_row.items()}

# Columns whose null percentage exceeds the threshold
cols_to_drop = [c for c, pct in null_pct.items() if pct > null_count_threshold]


dropped_coln_dff = combined_df_ren.drop(*cols_to_drop)
 

df_sla_fin = (
    dropped_coln_dff
    # 1. Resolution time in hours (null while closed_date is null)
    .withColumn("is_open", F.col("closed_date").isNull())
    .withColumn(
        "effective_closed_date",
        F.coalesce(F.col("closed_date"), F.current_timestamp())
    )

    # 1. Resolution time in hours (open requests = elapsed time so far)
    .withColumn(
        "resolution_hours",
        (F.unix_timestamp(F.col("effective_closed_date")) - F.unix_timestamp(F.col("created_date"))) / 3600
    )

    # 2. Within SLA? (null only if the data is invalid)
    .withColumn(
        "within_sla",
        F.when(F.col("resolution_hours").isNull() | (F.col("resolution_hours") < 0), F.lit(None).cast("boolean"))
         .when(F.col("resolution_hours") <= F.lit(SLA_HOURS), F.lit(True))
         .otherwise(F.lit(False))
    )
)

dropped_dup = df_sla_fin.dropDuplicates(['unique_key'])

desc_re_hr_df = dropped_dup.orderBy("resolution_hours", ascending=False)

# desc_re_hr_df.show(10, truncate=False)

desc_re_hr_df_year = desc_re_hr_df.withColumn("year", F.year(F.col("created_date")))
#############################


# 2. Define your Python enrichment function
def analyze_resolution(description):
    """
    Parses free-text resolution descriptions for key taxi service metrics.
    Handles None/Null values safely.
    """
    if not description:
        return ("UNKNOWN", "NO_ACTION", [])
    
    desc_lower = description.lower()
    
    # Determine the status/outcome
    if "repair" in desc_lower :
        outcome = "REPAIR"
    elif "" == desc_lower :
        outcome = "UNKNOWN"
    elif "police" in desc_lower :
        outcome = "POLICE ACTION"
    elif "Police Department reviewed your complaint" in desc_lower :
        outcome = "POLICE REVIEW PENDING"
    elif "insufficient contact information" in desc_lower or "no contact information" in desc_lower or "could not find the individual" in desc_lower:
        outcome = "INSUFFICIENT_CONTACT"
    elif "conducted or attempted to conduct an inspection" in desc_lower:
        outcome = "INSPECTION_ATTEMPTED"
    elif "duplicate" in desc_lower or "duplicate complaint" in desc_lower:
        outcome = "DUPLICATE"
    elif "status for this request is available" in desc_lower:
        outcome = "STATUS_AVAILABLE"
    elif "verify the correction of the condition" in desc_lower :
        outcome = "VERIFICATION PENDING"
    elif "could not be located" in desc_lower or "unable to locate" in desc_lower:
        outcome = "UNRESOLVED"
    else:
        outcome = "CLOSED"

    # Determine responsible entity or action category
    if "tlc" in desc_lower or "taxi and limousine commission" in desc_lower:
        agency_action = "TLC_ENFORCEMENT"
    elif "nypd" in desc_lower or "police" in desc_lower:
        agency_action = "POLICE_INTERVENTION"
    else:
        agency_action = "STANDARD_PROCEDURE"

    # Extract dynamic tags/keywords found in text
    tags = []
    if "overcharge" in desc_lower: tags.append("Billing")
    if "refused" in desc_lower: tags.append("Refusal of Service")
    if "rude" in desc_lower or "behavior" in desc_lower: tags.append("Driver Conduct")
    if "reckless" in desc_lower or "speeding" in desc_lower: tags.append("Safety")

    return (outcome, agency_action, tags)

# 3. Define the explicit schema for the UDF output
# This avoids PyArrow serialization dependencies
enrichment_schema = StructType([
    StructField("resolution_outcome", StringType(), True),
    StructField("agency_action_type", StringType(), True),
    StructField("extracted_tags", ArrayType(StringType()), True)
])

# 4. Register the UDF
# Explicitly declaring the returnType ensures PySpark serializes via standard Pickle
enrich_resolution_udf = udf(analyze_resolution, enrichment_schema)

# 6. Apply the UDF to enrich the DataFrame
enriched_df = desc_re_hr_df_year.withColumn("enrichment_data", enrich_resolution_udf(col("resolution_description")))

# 7. Flatten the structured result into individual columns
final_df = enriched_df.select(
    col("unique_key"),
    col("resolution_description"),
    col("borough"),
    col("complaint_type"),
    col("enrichment_data.resolution_outcome").alias("resolution_outcome"),
    col("enrichment_data.agency_action_type").alias("agency_action_type"),
    col("enrichment_data.extracted_tags").alias("extracted_tags"), 
    col("year")
)

final_df_fixed_extracted_tags = final_df.withColumn("extracted_tags", F.concat_ws(",", F.col("extracted_tags")))



# Show the results
# final_df.show(50)

final_df_fixed_extracted_tags.write \
    .format("csv") \
    .mode("overwrite") \
    .partitionBy("borough") \
    .partitionBy("complaint_type") \
    .partitionBy("year") \
    .save("/Users/sumant/workspace/learning/DE_Practise/sumant-nyc-311-data-pipeline/se-spark-exercise/output")

