# dendrogram-icebreaker

To use:

```
import sys
sys.path.append("dendrogram-icebreaker")
from main import *

activity_one('13YaIbVBifEURdT3lZkotSGmGEoi5xZGrXbmLydtpAv8', group=6)
activity_two(group=3, filepath='~/images/') # for example
omnigram()
```

When calling activity_one, be sure the sheet you are trying to fetch is the very first sheet in the document. Output is written to `activity1_fig[a,b,c]_group[group].png`

When calling activity_two for group `n`, a file will be written to the directory specified in `filepath` of the form `activity2_group[n]`.png

`omnigram` outputs `research.png`, `topics.png`, and `data.png`, barplots of the distribution of responses from the respective category - as well as `omnigram.png`, a dendrogram consisting of all the responses to activity 2 collectively. `omnigram` collates responses from all groups listed in `groups.json`. 
