# Commit Guide

- Have a short, but on point title
- tell us what was changed
- tell us why it was changed
- use as much words as you need, but as littel as you can.


## Why having a meaningful and short title matters
A good title not only matters as a quick summary of the changes made, more importantly it helps you to reason about
the changes you made and serves as a good test if your changes are all going in the same direction,
or if you have changed things everywher a bit without a common goal / theme.

If you struggle finding a good, on point title this might be an indicator that you changed too many things at once
and should split up your commit into smaller ones.

## Why a good commit message matters
When committing it is essential to write a meningful message for others to easierly understand the changes you 
employed and why they were necessary. And again, tests the changes you made agains common-sense.

### Test yourself
When writing the commit message, you are no longer thinking in code but about putting your changes into words. This 
change in thinking helps you to see the changes you made in a different light. Use this to your advantage!

When writing the part about **what** has changed in your commit, I like to have `git diff` showing me the changes 
I made. Firstly, this helps me remeber places in the code I forgot to adapt. And secondly, I can make sure to address
every change that I made.

When writing the **why** part, challenge the idea you had, when you were working on your code. Sometimes I start out
with an idea. But later, when writing the commit message and struggling to find the right justification for the change,
I sometimes realize that the changes were not necessary at all.
But that is not everything. The **why** part is the most important part of your message. This part can help and other
later on when they need to understand the changes you made. Especially with working in a team where others read your
code, they might understand it, but they might not immediately see why your code was written the way it was. They might
think to themselves that they can do this more efficient, easier to read and with fewer lines of code. What they do not
know however is, that you yourself maybe tried all those other more efficient more readable ways but coudln't get them
to work. This is your chance to make history not repeat itself. Write your experiences down in the message and make
clear what you tried and why this specific bit of code needs to be just the way it is.
