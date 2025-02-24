# Contributing

> [!IMPORTANT]
> We welcome all potential contributors regardless of their skill level :)

Thanks for taking the time to contribute to ZestCode! ZestCode is written and maintained by the community, and relies on people like you to stay up to date and bug-free.
We highly recommend you join our [Discord Server](https://discord.gg/vNMXCvVwdY) so you can talk to other contributors, ask questions, and join discussion in development discussion.

## Submitting a bug, feature request, or task

Simply open a [new issue](https://github.com/ZestCommunity/ZestCode/issues/new)

## Finding Stuff to Work On

We use GitHub projects to keep track of what needs to be worked on. Take a quick look:

- [PROS Refactor](https://github.com/orgs/ZestCommunity/projects/8)
- [Build System Overhaul](https://github.com/orgs/ZestCommunity/projects/1)
- [FreeRTOS decoupling](https://github.com/orgs/ZestCommunity/projects/5)

Additional tasks which may not be grouped in one of these projects may be found in the [issues tab](https://github.com/ZestCommunity/ZestCode/issues)

There are 5 categories these items may be group in:
- Backlog
  - need other items to be completed first before we can start working on them
- Ready
  - these items can be worked on, and no-one is currently working on them
- In progress
  - these items are currently being worked on
- In review
  - these items are almost done, and are currently being reviewed
- Done
  - these items have been completed

## Your First Pull Request (PR)

### Development Environment

First, you need to get a development environment set up. Below is a list of software you'll need:

- Python
- Visual Studio Code with these extensions
  - clangd
  - PROS

### Creating a fork

> [!IMPORTANT] you'll need a [GitHub account](https://github.com/) for this step

In order to propose changes to ZestCode, you'll need your own copy of ZestCode with version tracking. This is called a "fork". [Click Here](https://github.com/ZestCommunity/ZestCode/fork) to create your fork, and then press the green button. Now, clone your fork.

### Opening a Draft Pull Request

Next, open a draft pull request to let everyone know you are working on an issue. [Click Here](https://github.com/ZestCommunity/ZestCode0/compare/main...ZestCommunity:ZestCode:main), then click on head repository on the right, then click on your fork.

### Building

The first thing you'll need to do is run the following command in the PROS integrated terminal:

```
make clean; pros build-compile-commands
```

This will download the VEX SDK, set up clangd (the linting tool), and of course build ZestCode. When you want to build ZestCode again after making changes, simply run

```
make -j
```

in the PROS integrated terminal.