import dendrogram
import binary_dendrogram
import omnigram

def activity_one(g_id, group=None):
    dendrogram.no_cli_main(g_id, group)

def activity_two(group, filepath='.'):
    binary_dendrogram.no_cli_main(group, filepath)
