# Returns a dictionary of IDs and screen names
def get_follows_dict(follow_file):
    with open(follow_file, 'r') as infile:
        idvals = {}
        lines = infile.readlines()
        for line in lines:
            (id, screen_name) = (line.strip()).split('\t')
            idvals[id] = screen_name
    return idvals


# We're going to open the blocklist line by line and
# look for members in smaller file
def find_common(ids, larger_file):
    common_idvals = []
    with open(larger_file, 'r') as infile:
        for line in infile:
            if line.strip() in ids:
                common_idvals.append(line.strip())
    return common_idvals


if __name__ == '__main__':
    # Tab-delimited text file with files @unblock_list is following.
    # You can get this from my Github and I will try to keep it UTD
    follows_file = "junk/unblock_follows.txt"
    # Blocklist file of IDs to check.  Can be DL'd from blocklist.org list page
    blocklist_file = "junk/TERFblocklist-blocklist.csv"
    # File to save results to
    outfile = "junk/unblock_common.txt"

    # Generate dictionary from follows_file
    ids = get_follows_dict(follows_file)

    # Find the IDs on the blocklist that @unblock_list is also following
    common_ids = find_common(ids.keys(), blocklist_file)

    # Write out and display screen names (more user-friendly than IDs)
    with open(outfile, 'w') as ofile:
        for idx in common_ids:
            print(ids[idx])
            ofile.write(ids[idx] + '\n')
