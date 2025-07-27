===============   
   Use Cases
===============
1. Update the index when there are git changes.
1. Based on a tree + blob index. Suggest changes to my current code that I might have missed.
    - Store semantic changes in a database and query to suggest ones of similar nature.
    - Use `git diff` to compare the current state of the code with previous commits.
    - Submit the diff output into a context window for further analysis.
1. See how a file changed over time.
    - Use `git log -p <file>` to see the commit history and changes made to the file.
    - Submit the changes into a context window for further analysis.
1. Compare a change against another repo.
    - Similar to above but since we track multiple repos we can compare changes across them.
    - 
