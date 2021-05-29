
resource "google_container_cluster" "gpu-cluster" {
  name                     = "${var.cluster_name_prefix}-cluster"
  location                 = var.zone
  project                  = module.project-services.project_id
  remove_default_node_pool = true
  initial_node_count       = 1
  networking_mode          = "VPC_NATIVE"

  ip_allocation_policy {
    cluster_ipv4_cidr_block  = "/16"
    services_ipv4_cidr_block = "/16"
  }

}

resource "google_container_node_pool" "gpu_node_pool" {
  name       = "${var.cluster_name_prefix}-pool"
  cluster    = google_container_cluster.gpu-cluster.name
  location   = var.zone
  node_count = var.gpu_pool_node_count

  node_config {
    
    machine_type = var.gpu_machine_type

    service_account = google_service_account.service_account.email

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    dynamic guest_accelerator {
        for_each = var.gpu_type != null ? [1]: []
        content {
            type  = var.gpu_type
            count = var.gpu_count
        }
    }
  }
}





