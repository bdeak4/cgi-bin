#!/usr/bin/env bash

set -e

wallet_address=$(echo "$QUERY_STRING" | sed -e 's/^.*=//')
wallet_addr=$(echo "$wallet_address" | cut -c1-6)

if [ -z "$wallet_address" ]; then
    echo "Content-type: text/html"
    echo
    echo "Please provide a wallet address"
    exit 1
fi

cat << EOF
Content-type: text/xml

<rss version="2.0">
<channel>
<title>Solana SPL balance</title>
<description>Solana SPL transfers feed</description>
<link>https://solscan.io/account/$wallet_address</link>
<generator>solana-spl-balance-rss</generator>
EOF

curl -s "https://api.solscan.io/account/token/txs?address=$wallet_address&offset=0&limit=25" \
| jq -r ".data.tx.transactions[].change
         | select(.changeAmount != \"0\")
         | [.blockTime, .changeAmount, .postBalance, .decimals, .tokenName, .signature[0]]
         | @tsv" \
| sort -rn \
| awk -F"\t" 'BEGIN {OFS=FS}; {
       "date -R -d @"$1 | getline x; $1=x;
       print $0}' \
| awk -F"\t" '{print "<item><title><![CDATA['"$wallet_addr"' wallet balance change " ($2>0 ? "+" : "") \
                      ($2!=0 ? $2/10^$4 : "0") " " $5 " (current balance: " ($3!=0 ? $3/10^$4 : "0") \
                      ")]]></title><link>https://solscan.io/tx/"$6"</link><pubDate>"$1"</pubDate></item>"}'

cat << EOF
</channel>
</rss>
EOF
