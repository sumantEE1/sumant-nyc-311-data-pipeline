terraform {
  required_providers {
    snowflake = {
      source = "snowflakedb/snowflake"
    }
  }
}

locals {
  organization_name = "GUSDATD"
  account_name      = "DAB70621"
  private_key_path  = "~/.ssh/snowflake_rsa_key.p8"
}

provider "snowflake" {
    organization_name = local.organization_name
    account_name      = local.account_name
    user              = "sumant.dey"
    role              = "SE_DE_PARTICIPANT"
    authenticator     = "SNOWFLAKE_JWT"
    private_key       = file(local.private_key_path)

    # Enable the preview table resource feature
    preview_features_enabled = ["snowflake_table_resource"]
}


# resource "snowflake_warehouse" "SNOWFLAKE_LEARNING_WH" {
#   name           = "SNOWFLAKE_LEARNING_WH"
#   warehouse_size = "X-SMALL"
#   auto_suspend   = 60
#   initially_suspended = true
# }


# resource "snowflake_database" "DE_CROSS_SKILLING_NYC_311" {
#   name    = "DE_CROSS_SKILLING_NYC_311"
#   comment = "Database storing raw, unprocessed source system data."
# }

# Define the RAW schema within that database
resource "snowflake_schema" "SUMANT_DEY_RAW" {
  database            = "DE_CROSS_SKILLING_NYC_311"
  name                = "SUMANT_DEY_RAW"
  comment             = "Schema for raw ingest layers managed by tools like Fivetran/Airbyte."
}

resource "snowflake_table" "sumant_dey_raw_nyc_311_data_table" {
  database = "DE_CROSS_SKILLING_NYC_311"
  schema   = "SUMANT_DEY_RAW"
  name     = "sumant_dey_raw_nyc_311_data_table"
  comment  = "A table to store nyc practise raw data"

  # Define columns inside the table block
  column {
        name     = "UNIQUE_KEY"
        type     = "NUMBER(38,0)"
        nullable = true
    }
    column {
        name     = "CREATED_DATE"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "CLOSED_DATE"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "AGENCY"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "AGENCY_NAME"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "COMPLAINT_TYPE"
        type     = "VARCHAR(16777216)"
        nullable = true
    }   
    column {
        name     = "DESCRIPTOR"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "LOCATION_TYPE"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "INCIDENT_ZIP"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "INCIDENT_ADDRESS"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "STREET_NAME"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "CROSS_STREET_1"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "CROSS_STREET_2"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "INTERSECTION_STREET_1"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "INTERSECTION_STREET_2"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "ADDRESS_TYPE"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "CITY"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "LANDMARK"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "FACILITY_TYPE"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "STATUS"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "DUE_DATE"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "RESOLUTION_DESCRIPTION"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "RESOLUTION_ACTION_UPDATED_DATE"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "COMMUNITY_BOARD"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "BOROUGH"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "X_COORDINATE"
        type     = "NUMBER(38,0)"
        nullable = true
    }
    column {
        name     = "Y_COORDINATE"
        type     = "NUMBER(38,0)"
        nullable = true
    }
    column {
        name     = "PARK_FACILITY_NAME"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "PARK_BOROUGH"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "BBL"
        type     = "NUMBER(38,0)"
        nullable = true
    }
    column {
        name     = "OPEN_DATA_CHANNEL_TYPE"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "VEHICLE_TYPE"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "TAXI_COMPANY_BOROUGH"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "TAXI_PICKUP_LOCATION"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "BRIDGE_HIGHWAY_NAME"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "BRIDGE_HIGHWAY_DIRECTION"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "ROAD_RAMP"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "BRIDGE_HIGHWAY_SEGMENT"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "LATITUDE"
        type     = "FLOAT"
        nullable = true
    }
    column {
        name     = "LONGITUDE"
        type     = "FLOAT"
        nullable = true
    }
    column {
        name     = "LOCATION"
        type     = "VARCHAR(16777216)"
        nullable = true
    }
    column {
        name     = "_loaded_at"
        type     = "TIMESTAMP_NTZ"
        default {
            constant = "CURRENT_TIMESTAMP()"
        }
    }
}
