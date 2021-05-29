# Create the service account
resource "google_service_account" "service_account" {
    account_id = "${var.cluster_name_prefix}-sa"
    display_name = "GKE service account"
}

# Create role bindings
resource "google_project_iam_member" "role_bindings" {
  for_each = toset(var.gke_service_account_roles)
  member   = "serviceAccount:${google_service_account.service_account.email}"
  role     = "roles/${each.value}"
}