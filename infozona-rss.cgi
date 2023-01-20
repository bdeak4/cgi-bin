#!/usr/bin/env bash

set -e

cat << EOF
Content-type: text/xml

<rss version="2.0">
<channel>
<title>Kalendar događanja u Splitu • Info zona</title>
<description>Infozona Kalendar Feed</description>
<link>https://kalendar.infozona.hr/</link>
<generator>infozona-rss</generator>
EOF

for i in {0..10}; do
	date=$(date -I -d "+$i day")
	curl -s "https://kalendar.infozona.hr/api/v1/events/$date" \
	| jq -r '.dayEvents[]|"\(.title.hr) (\(.category[0].title.hr))\thttps://kalendar.infozona.hr/event/\(.id)"' \
	| sed "s/^/$(date -R -d "$date")\t/"
done \
| awk -F"\t" '!_[$2]++' \
| awk -F"\t" '{print "<item><title><![CDATA["$2"]]></title><link>"$3"</link><pubDate>"$1"</pubDate></item>"}'

cat << EOF
</channel>
</rss>
EOF
