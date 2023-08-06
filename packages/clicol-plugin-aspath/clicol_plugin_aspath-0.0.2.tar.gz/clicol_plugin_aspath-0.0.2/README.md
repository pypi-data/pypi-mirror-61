CLICOL PLUGIN ASPATH
====================
Plugin for [clicol](https://github.com/realvitya/clicol) which helps troubleshooting by resolving sitecodes for AS path.

### Example

	 Default append view:
	 * i  10.0.35.48/28    10.123.123.158           0    100      0 21302 13979 65120 64932 ? ATT ABC --- EFH
	 *>                    10.123.234.154                         0 21302 13979 65120 64932 ? ATT ABC --- EFH
	 Or the inline view:
	 * i  10.0.35.48/28    10.123.123.158           0    100      0 21302(ATT) 13979(ABC) 65120 64932(EFH) ?
	 *>                    10.123.234.154                         0 21302(ATT) 13979(ABC) 65120 64932(EFH) ?

### Configuration

In `~/.clicol/plugins.cfg` there must be a section for the plugin.

Example with defaults:

	 # AS Path resolver:
	 [aspath]
	 # disable until not configured
	 active=no
	 # view (append|inline)
	 #outtype=append
	 # database file default
	 #dbfile=~/.clicol/plugin-aspath.db
	 # what to print on unknown AS
	 #unknownstr=---
     # Force dotted format for 4bytes AS numbers (no need to reconfigure router!)
     #forcedotformat=no
	 
Format of database file:
`{ASNUM}\t{DESCRIPTION}\t{SITECODE}`

3 columns required, more columns are ok. Column separator is TAB!
Example:

	21302	AT&T EAME	ATT	-	Vendor
	13979	AT&T NA	ATT

### Thanks to
I was using [tbaschak](https://github.com/tbaschak)'s [asdot-asplain](https://github.com/tbaschak/asdot-asplain) library for 4byte AS number conversion. Thanks!

