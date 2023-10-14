# 2023 2024 FRC Season
All of our code for the 2023-2024 FIRST® Robotics Competition CRESCENDO, Presented by HAAS and projects in the offseason.

# Programming Convention
We use [Trunk Based Development](https://trunkbaseddevelopment.com/).

This repository includes the following:
+ [The Training Folder<sup>TM</sup>](https://github.com/SteelRidgeRobotics/2023-2024_FRC_Season/tree/main), which contains all the training projects our newest programmers coded and worked on to get familiar with our \*amazing\* workflow.
+ Our [Trunk or Treat Bot, Telepatata](https://github.com/SteelRidgeRobotics/2023-2024_FRC_Season/tree/main/TrunkOrTreatRobot), which (shockingly) is our robot code for Trunk or Treat.
+ Other stuff later, probably ;)

## The Basics
Trunk Based Development makes it easier to have a team of people working together on one project. It works by seperating everyone's work into seperate branches that can be committed and pushed to independently without having to update every change thats made in main.

As of 10/13/2023 we have <sub>around</sub> 6 programmers, which may not seem like a big deal, but it's literally double from how much we had last year. Because of this, we'll try and enforce Trunk Based more.

## The Art of Not Pissing Off The Other Programmers, by [Pickle_Face5](https://github.com/PickleFace5)
These are the 3 main ideas of Trunk Based programming that you need to follow. If you don't you'll likely be exiled from the Coding Plateau until you pay the hefty fine of 1 12-pack of coke.

### Rule #1: Don't Commit or Push to The Main Branch. Please.
***PLEASE PLEASE PLEASE*** don't do this. This ends up having everyone having to redo their branches to match the pushed code, which just slows us down. (and during build season, we NEED time)

Double check before commiting or pushing anything it's not going to main.

### Rule #2: Name Your Branches Something Good and Keep Them<sub>small.</sub>
When creating a feature branch (the branch that you write code on then later push everything to main), make sure you're being *specific, clear, and concise* what your branch will add. Being general and broad confuses other programmers and makes branches take longer to complete. (which we'll elaborate more on in Rule #3)

#### Example Branch Names (Featuring Palpatine)
| Good Branch Name | Bad Branch Name | Why That Branch Name Sucks<sup>TM</sup>
|------------------|------------------|---------------------------------------|
| `palpatine-guitar-controls` | `palpatine-guitar` | This branch name is too generic. What about the guitar are we adding to Palpatine? |
| `palpatine-comment-refactoring` | `comment-refactoring` | While this branch name tells us what it's doing, it doesn't tell us to *whom* it's comment refactoring to. |
| `palpatine-exploding-glitch-fix` | `palpatine-bug-fix` | This branch doesn't tell us what big fix it's fixing on Palpatine. |
| `palpatine-controller-drift-fix` | `palpatine-controller-fix-because-it-drifts-slightly-to-the-right` | "I ain't reading all that 🔥" - Me after seeing that branch name probably |
| `palpatine-back-flip-optimizing` | `code` | ...please don't do this. |

> [!NOTE]
> A basic branch should be something similar to `<robot-name>-<what-your-doing>`

Basically, when creating your branch, ask yourself the following:
+ "Can I tell what robot this is for?"
+ "Can I tell what I'm adding/fixing?"
+ "Is this a stupid idea?"
+ "Why the hell did I think I would enjoy this?"

### Rule #3: Merge Branches ASAP
Sitting on a branch for a month will probably be uncomfortable and cause issues when merging your branch. This is why we enforce Rule 2; to give your branch a small amount of time to finish.

Because the branch has been worked on for a month, lots of chances have (hopefully) been done to the main branch, meaning your amazing branch is now *completely outdated!* 🥳

To avoid this, finish your current branch before working on a new one. __DON'T MULTITASK__.

> [!NOTE]
> To keep branches from taking forever, give yourself a deadline; have your new features take ~1-2 weeks to finish.

### TL;DR
1. Don't push code to `main`, create a branch and merge it instead.
2. Name your branches something easy to understand.
3. Get your crap done on time.
