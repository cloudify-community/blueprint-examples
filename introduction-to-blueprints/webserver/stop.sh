#!/bin/bash
#kill the webserver process and delete the temporary directory
kill `ctx instance runtime-properties pid` && rm -rf `ctx instance runtime-properties path`
