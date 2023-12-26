#!/usr/bin/env bash

notion_site="superteam.fun"
notion_page="ideas-rfps"

set -e

cat << EOF
Content-type: text/xml

<rss version="2.0">
<channel>
<title>Superteam - Open RFPs</title>
<description>Complete open RFPs successfully and get paid!</description>
<link>https://$notion_site/$notion_page</link>
<generator>superteam-open-rfps-rss</generator>
EOF

build=$(curl -s https://$notion_site/$notion_page | grep -o '"buildId":\s*"[^"]*' | grep -o '[^"]*$')

curl -s https://$notion_site/_next/data/"$build"/$notion_page.json?page=$notion_page \
| jq -r ".pageProps.records.block
         | to_entries[]
         | .value
         | select(.title != null and .uri != \"/$notion_page\")
         | [.createdTime, .title[0][0], \"https://$notion_site\"+.uri]
         | @tsv" \
| sort -rn \
| awk -F"\t" 'BEGIN {OFS=FS}; {
       "date -R -d @"int($1/1000) | getline x; $1=x;
       print $0}' \
| awk -F"\t" '{print "<item><title><![CDATA["$2"]]></title><link>"$3"</link><pubDate>"$1"</pubDate></item>"}'

cat << EOF
</channel>
</rss>
EOF
