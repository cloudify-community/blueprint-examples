# blueprint-examples

**Download Cloudify to [get started](https://cloudify.co/download)!**

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

If you have a blueprint that you have written and would like to share with Cloudify's user community, follow these instructions:

Contribution steps:

1. [Fork this repository](https://help.github.com/articles/fork-a-repo/) to your Github account.
1. [Create a branch](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/) in your repository.
1. [Add your blueprint](https://help.github.com/articles/adding-a-file-to-a-repository/) to the forked repository. Make sure that it has its own folder like all the other blueprints (e.g. the aws-example-network).
1. [Create a Pull Request](https://help.github.com/articles/creating-a-pull-request-from-a-fork/) from the branch in your forked repository to the master branch in this repository (cloudify-community/blueprint-examples).

When you create your pull request, include the following information:

1. Provide us with the appropriate contact info, so that other users from the community can contact you for support questions related to your contribution.
1. Tell us who you are. Do you have permission to distribute this work?
1. Include a README.md file in your blueprint folder that describes what the blueprint does, what prerequisites are needed, including instructions to fulfill those prerequisites.
1. **With regards to testing**, these blueprints only need to pass regular DSL validation testing. However, in order to accept your PR, we will need to install your example blueprint and verify that the blueprint works as intended. Please include all necessary instructions and be prepared to answer additional questions.
1. Please feel free to email us at community@cloudify.co for further information.

# Support

1. We will support all of the examples that we wrote, and will do our best to answer questions on all community examples. However, in some cases, we may ask you to directly contact the contributor of the example in question.
1. Feel free to submit PRs to fix issues that you run into during deployment of any of the examples.
