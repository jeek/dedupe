# dedupe
python script to hardlink duplicate files

Scan the path storing each file in a list, categorized by file size. Toss out all files under 20M.

Then process each element in the list with more than one file of the same size. For each pair, calculate the sha256 hash. If the hashes match, replace one of the pair with a hardlink to the other.
