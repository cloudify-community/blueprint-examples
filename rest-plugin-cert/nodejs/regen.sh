#!/bin/bash
rm *.pem
openssl req -x509 -newkey rsa:4096 -keyout server_key.pem -out server_cert.pem -nodes -days 365 -subj "/CN=localhost/O=Client\ Certificate\ Demo"
openssl req -newkey rsa:4096 -keyout alice_key.pem -out alice_csr.pem -nodes -days 365 -subj "/CN=Alice"
openssl req -newkey rsa:4096 -keyout bob_key.pem -out bob_csr.pem -nodes -days 365 -subj "/CN=Bob"
openssl x509 -req -in alice_csr.pem -CA server_cert.pem -CAkey server_key.pem -out alice_cert.pem -set_serial 01 -days 365
openssl x509 -req -in bob_csr.pem -signkey bob_key.pem -out bob_cert.pem -days 365
cat alice_cert.pem alice_key.pem > alice.pem
cat bob_cert.pem bob_key.pem > bob.pem
