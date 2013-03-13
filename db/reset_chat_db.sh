#!/bin/sh

sqlite3 ccie.db <<EOF
.read ../sql/drop_chat_tables.sql
.read ../sql/create_phrases.sql
.read ../sql/create_convo_pair.sql
.read ../sql/create_phrase_stats.sql
.read ../sql/insert_seeds.sql
.read ../sql/insert_pairings.sql
.read ../sql/insert_usage.sql
.exit
EOF

cd ..
for i in training/logs/*.txt; do
    echo "$i"
    python testlogs.py "$i"
done