# Generate a random suffix to prefix resources with
resource "random_id" "suffix" {
  byte_length = 4
}

resource "google_compute_instance" "example_instance" {
  name         = "${var.prefix}-instance-${random_id.suffix.hex}"
  machine_type = var.instance_type
  zone         = "${var.region}-a"

  metadata = {
    ssh-keys = "${var.admin_user}:${var.admin_key_public}"
  }

  boot_disk {
    initialize_params {
      image = "${var.image.project}/${var.image.family}"
    }
  }

  network_interface {
    network = var.network
    access_config {}
  }
}
