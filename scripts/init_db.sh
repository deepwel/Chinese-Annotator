#!/bin/bash

mongo ca -eval "db.dropDatabase()"
mongo ca -eval "db.createUser({user:\"anno_admin\", pwd:\"123\", roles:[\"readWrite\", \"dbAdmin\"]})"

mongo ca -eval "db.user.insert({_id: ObjectId(\"5a683cadfe61a3fe9262a310\"), user_name:\"booker\"})"
mongo ca -eval "db.dataset.insert({_id:ObjectId(\"5a6840b28831a3e06abbbcc9\"), dataset_name: \"test\", user_uuid: \"5a683cadfe61a3fe9262a310\", timestamp: new Date()})"
insert_neg_str="{text: \"我是青铜##！\", labeled: true, predicted: true, dataset_uuid: \"5a6840b28831a3e06abbbcc9\"}"
insert_pos_str="{text: \"我是王者##！\", labeled: true, predicted: true, dataset_uuid: \"5a6840b28831a3e06abbbcc9\"}"
insert_no_predict1="{text: \"我是big old##！\", labeled: false, predicted: false, dataset_uuid: \"5a6840b28831a3e06abbbcc9\"}"
insert_no_predict2="{text: \"我是simple young##！\", labeled: false, predicted: false, dataset_uuid: \"5a6840b28831a3e06abbbcc9\"}"

max_sample=10
for i in $(seq 1 $max_sample); do
    insert_str_new=$(echo $insert_neg_str | sed -n "s/##/$i/"p)
    mongo ca -eval "db.annotation_raw_data.insert($insert_str_new)"
    insert_str_new=$(echo $insert_pos_str | sed -n "s/##/$i/"p)
    mongo ca -eval "db.annotation_raw_data.insert($insert_str_new)"

    insert_str_new=$(echo $insert_no_predict1 | sed -n "s/##/$i/"p)
    echo $insert_str_new
    mongo ca -eval "db.annotation_raw_data.insert($insert_str_new)"

    insert_str_new=$(echo $insert_no_predict2 | sed -n "s/##/$i/"p)
    mongo ca -eval "db.annotation_raw_data.insert($insert_str_new)"
done

insert_neg_str="{text: \"我是个青铜##！\", label: \"bad\", dataset_uuid: \"5a6840b28831a3e06abbbcc9\", user_uuid: \"5a683cadfe61a3fe9262a310\", timestamp: new Date()}"
insert_pos_str="{text: \"我是王者##！\", label: \"good\", dataset_uuid: \"5a6840b28831a3e06abbbcc9\", user_uuid: \"5a683cadfe61a3fe9262a310\", timestamp: new Date()}"
max_sample=10
for i in $(seq 1 $max_sample); do
    insert_str_new=$(echo $insert_neg_str | sed -n "s/##/$i/"p)
    mongo ca -eval "db.annotation_data.insert($insert_str_new)"
    insert_str_new=$(echo $insert_pos_str | sed -n "s/##/$i/"p)
    mongo ca -eval "db.annotation_data.insert($insert_str_new)"
done
