variable "project_id" {
    description = "The GCP project ID"
    type        = string
}

variable "zone" {
    description = "The zone for the cluster"
    type        = string
}

variable "region" {
    description = "The default region"
    type        = string
}

variable "cluster_name_prefix" {
    description = "The prefix of the Kubernetes cluster name"
    type        = string
}

variable "gpu_pool_node_count" {
    description = "The clusters' node count"
    default     = 1
}

variable "gpu_type" {
    description = "GPU type"
    type        = string
    default     = null
}

variable "gpu_count" {
    description = "GPU count"
    default     = 1
}

variable "gpu_machine_type" {
    description = "The machine type for a default node pool"
    type        = string
}

variable "gke_service_account_roles" {
  description = "The roles to assign to the GKE service account"
  default = [
    "logging.logWriter",
    "monitoring.metricWriter", 
    "monitoring.viewer", 
    "stackdriver.resourceMetadata.writer",
    "storage.objectViewer" 
    ] 
}

