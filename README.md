# dendrogram-icebreaker

To use:

```
from main import *

activity_one('13YaIbVBifEURdT3lZkotSGmGEoi5xZGrXbmLydtpAv8', group=6)
activity_two(group=3, filepath='~/images/) # for example
```

When calling activity_one, be sure the sheet you are trying to fetch is the very first sheet in the document.

When calling activity_two for group `n`, a file will be written to the directory specified in `filepath` of the form activity2_group`n`.png

omnigram functionality coming soon.
