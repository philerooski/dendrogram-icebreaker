import dendrogram
import binary_dendrogram
import omnigram as omni

def activity_one(g_id='13YaIbVBifEURdT3lZkotSGmGEoi5xZGrXbmLydtpAv8', group=None):
    dendrogram.no_cli_main(g_id, group)

def activity_two(group, filepath='.'):
    binary_dendrogram.no_cli_main(group, filepath)

def omnigram():
    omni.main()
