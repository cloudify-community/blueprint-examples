# Provisioning Infrastructure Examples

See [Infra Provisioning Basics](https://docs.cloudify.co/latest/trial_getting_started/examples/basic/) for the guide.

Also see [Use Automation Tools](https://docs.cloudify.co/latest/trial_getting_started/examples/automation_tools/) for the guide for Terraform, Cloud Formation, and Azure ARM.

Note about `ansible.yaml` example:
`selinux` is prerequisite for this example.
If using python 3 manager(5.1 and newer):
`yum install libselinux-python3`
If using python 2 manager(5.0.5 and older):
`yum install libselinux-python`