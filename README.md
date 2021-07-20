# Toxic Comment Classification

Use Natural Language Processing to predict if the given text is toxic or 
not.

## Data

The data comes in two files. One file consists of toxicity comments 
which all reviewers gave and the other one consists of positive 
comments.



## Smoothing

Scoring a comment using Interpolation smoothing techniques :

𝑃(𝑤𝑖|𝑤𝑖−1) = 𝜆3𝑃(𝑤𝑖|𝑤𝑖−1) + 𝜆2𝑃(𝑤𝑖) + 𝜆1𝜖

𝜆3 + 𝜆2 + 𝜆1 = 1  
 0 < 𝜖 < 1
##

![github-octocat](https://github.com/sevdaimany/NLP-Toxic-Comment-Classification/blob/master/screenshot.png)


## Show your support

Give a ⭐️ if you like this project!
