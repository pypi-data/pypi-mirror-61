Summary Webpage
===============

Table Columns
+++++++++++++

Last Update
-----------

The time that the previous Consistency Check finished in EST.
If the time is within the past 24 hours, the cell is shaded green.
Clicking on the link will give a history of the site.

Site Name
---------

Name of the site as stored in dynamo.
The cell might be one of the following colors:

- **Blue** -- the site is queued to be listed.
- **Green** -- the site is in the process of being listed.
- **Yellow** -- the site has been in the process of being listed for over 24 hours.
- **Gray** -- the site listing has either been disabled for that site or
  the SAM tests of the last 24 hours have failed more than 15% of the time.
- **Red** -- none of the above conditions are met, and the previous listing returned zero files.
  The number of files cell will remain red regardless of its running status
  if it had a bad listing completed most recently.

Clicking on the link will display the latest log file of an attempted listing for the site.
This log file may not correspond to the summary entry if there was an error before the rest of the webpage was updated.

Time [min]
----------

The amount of time for the entire check to finish.
A check includes the following steps.

- Get the site contents according to dynamo database.
- Generate a listing of the site contents.
  For most sites, this takes the majority of the time.
- Hash the contents of both listings for speedy comparisons.
  This hashing takes a couple of minutes for each (remote and dynamo) directory tree.
- Compare the trees and enter inconsistencies into our registry.
- Create summary reports and files that are copied to the webpage directory.

Number Files
------------

This is the total number of files that were confirmed as existing at the site.
They were each successfully identified by a remote listing call.
The link points to a JSON file that summarizes confirmed disk usage within the different top-level directories.

Number Nodes
------------

This the total number of directories that were identified in the listing.

Unlisted
--------

This is the number of nodes that claim to be not successfully listed.
Some of these nodes are purposefully not listed.
In parentheses, the number of nodes that were not listed as a result of an error is given.
If the number in parentheses is not zero, the column is highlighted as a red cell.
The link gives a .txt file that lists the unlisted directories.

Empty Nodes
-----------

The number of directories that have no files in them or no files in any subdirectories.
(The number of files "in" a directory is determined by a recursive call to all subdirectories.)

Num Missing
-----------

Number of files that appear to be missing at the site.
The link displayed as a number links to a .txt file containing the missing LFNs.
The links labels "blocks" shows a summary of the number of files missing from each block containing missing files.

No Disk
-------

Number of missing files that are not supposed to be on disk at any other site, according to dynamo.
These files must be recovered using tape copies.
The link is a list of file LFNs that are missing.
The number in parenthesis gives the number of files that do not seem to be on tape either.
That link gives the corresponding list.

Num Orphan
----------

The number of files that exist at a site that dynamo does not know about.
These files can be deleted.
The link is a list of file LFNs that are orphans.

Size [TB]
---------

There are two columns with this heading.
The first time shows the reported collective size of files that are missing.
The second time shows the spaced used by orphan files that can be recovered through deletion.

Unmerged Cleaned
----------------

Gives the number of files that were marked for deletion in the site's /store/unmerged directory.
The link points to a list of these files.
The number in parentheses displayed the number of those files that were logs.

Table Tabs
++++++++++

There are three tabs on the webpage.
The default tab when first navigating the website is, on the left.
It shows all of the sites with results that are being acted on.
The middle tab displays the sites that are only doing dry runs.
The last tab, on the right show all of the sites.
