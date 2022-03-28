#!/bin/bash

temp_dir=`mktemp -d`
git clone $app_git $temp_dir
cd "$temp_dir"
cp -rp * $app_path
rm -rf "$temp_dir"
