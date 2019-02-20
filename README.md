# blueprint-examples

**Try out a [free lab](https://cloudify.co/HostedCloudify)!**


## User guide

Each of these blueprints is tested on the version of Cloudify and with the latest version of our official Cloudify plugins. If you have not installed the required plugins, you can do so now from the CLI, by running `cfy plugins bundle-upload`.

### Install

To install one of these blueprints, follow these steps:

1. Go to the [releases](https://github.com/cloudify-community/blueprint-examples/releases) page. Find the latest package for your version of Cloudify.
1. Copy the link to the zip file for the blueprint that you want to install.
1. On your Cloudify Manager, navigate to `Local Blueprints` and select `Upload`. Paste the link where it says `Enter blueprint url`. Provide a blueprint name, such as `aws-example-blueprint` in the field labeled `blueprint name`. Select `blueprint.yaml` from `Blueprint filename` menu.
1. After the new blueprint has been created, click the `Deploy` button.
1. Navigate to `Deployments`, find your new deployment, select `Install` from the `workflow`'s menu. _Reminder, at this stage, you may provide your own values for any of the default `deployment inputs`._


### Uninstall

Navigate to the deployment and select `Uninstall`. When the uninstall workflow is finished, select `Delete deployment`.


# Contribution guide

Do you have a blueprint that you have written and would like to share with Cloudify's user community? If so, follow these simple instructions:

Contribution steps:

1. [Fork this repository](https://help.github.com/articles/fork-a-repo/) to your Github account.
1. [Create a branch](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/) in your repository.
1. [Add your blueprint](https://help.github.com/articles/adding-a-file-to-a-repository/) to the forked repository. Make sure that it has its own folder like all the other blueprints (e.g. the aws-example-network).
1. [Create a Pull Request](https://help.github.com/articles/creating-a-pull-request-from-a-fork/) from the branch in your forked repository to the master branch in this repository (cloudify-community/blueprint-examples).

When you create your pull request, please give us the following information:

1. Include a README.md file in your blueprint folder that describes what the blueprint does, what prerequisites are needed, including steps to fulfill those prerequisites.
1. Tell us who you are - are you a student, an enthusiast, or an employee at your company. Do you have permission to distribute this work?
1. Please provide tests if there is complex logic in any of the scripts in the blueprint.
