# MarioKart DataDriven (*MKDD*)

## Problem formulation

In MarioKart 8 Deluxe (*MK8D*) game on switch, players compete in car races. To do this, each player chooses a combination of **driver**, **body**, **wheel** and **glider** $(d,b,t,g)$ which produces a final kart. Each component $d$,$b$,$t$,and $g$ has a set of respective integers features that each ranges from 0 to 10 : 
- ***Weight (wei)***
- ***Acceleration (acc)***
- ***Traction (trac)***
- ***Speed (spd)*** 
- ***Handling (han)***
- ***Invincibility (inv)***
- ***Mini-Turbo (mt)***

We imagine that each player has his own set of personal preferences for each single category, that represent **preference weights** :

$$w=(w_{wei},w_{acc},w_{trac},w_{spd},w_{han},w_{inv},w_{mt})$$

Ideally, the selected quadruplet $(d,b,t,g)$ maximizes the overall score given the preference parameters :

$$\max_{(d,b,t,g) \in \mathcal{P}}s(d,b,t,g|w)$$

where $\mathcal{P}$ is the set of possible combinations (drivers are grouped in categories that restrict their possible choices of body/tile/glider). 

Here the score function is represented as a simple normalized weighted sum of the features stats for the driver, body, tile, and glider : 

$$ s(d,b,t,g|w) = \frac{1}{4 \times 6} \sum_{c \in (d,b,t,g)} \sum_{w_s \in w} w_s \times s_c $$ 

where $s_c \in (0,...,10)$ represent the statistic value of component $c$.

## Data

## Ressources 

[MarioWiki](https://www.mariowiki.com/Mario_Kart_8_Deluxe_in-game_statistics) : in game statistics