provider "google" {
  project     = var.project_id
  region      = var.location
}

resource "google_storage_bucket" "state_bucket" {
    name          = var.bucket
    location      = var.location
    project       = var.project_id
    storage_class = "STANDARD"
    force_destroy = true

    uniform_bucket_level_access = true

    # Enable Object Versioning
    versioning {
        enabled = true
    }

    lifecycle_rule {
        action {
            type = "Delete"
        }
        condition {
            age = 30
        }
    }
    labels = {
        env = "decrossskilling"
        time = "sep26"
    }
}

resource "google_storage_bucket_iam_member" "extract_sa_read" {
  bucket = google_storage_bucket.state_bucket.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:k4if00000@va3-22da.iam.gserviceaccount.com"
}